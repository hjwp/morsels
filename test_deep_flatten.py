import atexit
from collections import deque
from functools import wraps
import multiprocessing
import sys
import unittest


from deep_flatten import deep_flatten


class DeepFlattenTests(unittest.TestCase):
    """Tests for deep_flatten."""

    def assertIterableEqual(self, iterable1, iterable2):
        self.assertEqual(list(iterable1), list(iterable2))

    def test_deep_lists(self):
        inputs = [0, [1, [2, 3]], [4]]
        outputs = [0, 1, 2, 3, 4]
        self.assertIterableEqual(deep_flatten(inputs), outputs)

    def test_tuples(self):
        inputs = (0, (1, (2, 3)), [4])
        outputs = [0, 1, 2, 3, 4]
        self.assertIterableEqual(deep_flatten(inputs), outputs)

    def test_deep_empty_list_with_tuple(self):
        self.assertIterableEqual(deep_flatten([[()]]), [])

    # To test bonus 1, comment out the next line

    def test_other_iterables(self):
        self.assertIterableEqual(
            deep_flatten((n, (n**3, n**2)) for n in [2, 3]),
            [2, 8, 4, 3, 27, 9],
        )
        self.assertIterableEqual(deep_flatten([(1, 2), deque([3])]), [1, 2, 3])
        self.assertIterableEqual(deep_flatten(iter([n]) for n in [1, 2, 3]), [1, 2, 3])

    # To test bonus 2, comment out the next line

    @unittest.expectedFailure
    def test_returns_iterator(self):
        self.assertEqual(next(deep_flatten([0, [1, [2, 3]]])), 0)
        squares = (n**2 for n in [1, 2, 3])
        self.assertEqual(next(deep_flatten(squares)), 1)

        # The below lines test that the incoming generator isn't exhausted.
        # It may look odd to test the squares input, but this is correct
        # because after 1 item has been consumed from the deep_flatten
        # iterator, squares should also only have 1 item consumed from it.

        try:
            self.assertEqual(next(squares), 4, "squares is partially consumed")

        except StopIteration:
            self.fail("The incoming squares iterator was fully consumed!")

        # When we consume another item from deep_flatten, it'll skip over 4!
        self.assertEqual(next(deep_flatten(squares)), 9)
        # If the above didn't work, this would really break

        from itertools import count
        squares = (n**2 for n in count())
        self.assertEqual(next(deep_flatten(squares)), 0)
        self.assertEqual(next(squares), 1)
        self.assertEqual(next(deep_flatten(squares)), 4)

    # To test bonus 3, comment out the next line

    def test_flatten_with_strings(self):
        inputs = [
            ["cats", ["carl", "cate"]],
            ["dogs", ["darlene", "doug"]],
        ]
        outputs = ["cats", "carl", "cate", "dogs", "darlene", "doug"]
        timeouts = {
            "win32": 1.2,
            "darwin": 1,
            "linux": 0.5,
        }

        timeout = timeouts.get(sys.platform, 0.5)
        timeout_deep_flatten = with_timeout(list_deep_flatten, timeout)
        self.assertEqual(timeout_deep_flatten(inputs), outputs)


class AllowUnexpectedSuccessRunner(unittest.TextTestRunner):

    """Custom test runner to avoid FAILED message on unexpected successes."""

    class resultclass(unittest.TextTestResult):
        def wasSuccessful(self):

            return not (self.failures or self.errors)


def worker(function, args, kwargs, sender, receiver):

    """Send return value of function call through given pipe."""

    receiver.close()  # We're only sending

    try:

        sender.send([function(*args, **kwargs), None])

    except BaseException as exc:

        sender.send([None, exc])

    sender.close()  # Done sending


def with_timeout(function, timeout):

    """Return function to call the given function with timeout (in seconds)."""

    @wraps(function)
    def wrapper(*args, **kwargs):

        # AWS Lambda doesn't support Pool or Queue

        receiver, sender = multiprocessing.Pipe()

        process = multiprocessing.Process(
            target=worker,
            args=(function, args, kwargs, sender, receiver),
        )

        process.start()

        sender.close()  # We're only receiving

        atexit.register(terminate_process, process)  # Make sure to terminate

        try:

            if receiver.poll(timeout):

                return_value, exception = receiver.recv()

                if exception is None:

                    return return_value

                else:

                    raise exception

            else:

                raise TimeoutError("Took too long (infinite loop?)")

        finally:

            receiver.close()  # We're done receiving

            process.terminate()

    return wrapper


def terminate_process(process):

    process.terminate()


def list_deep_flatten(*args, **kwargs):

    return list(deep_flatten(*args, **kwargs))


if __name__ == "__main__":

    from platform import python_version

    if sys.version_info < (3, 6):

        sys.exit("Running {}.  Python 3.6 required.".format(python_version()))

    unittest.main(verbosity=2, testRunner=AllowUnexpectedSuccessRunner)
