def parse_ranges(range_string):
    for s in range_string.split(","):
        if "-" in s:
            start, end = s.split("-")
            subrange = range(int(start), int(end) + 1)
            for item in subrange:
                yield item

        else:
            yield int(s)

