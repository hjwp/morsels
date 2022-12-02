from __future__ import annotations

class FuzzyString(str):

    def __eq__(self, other: object) -> bool:
        # TODO: look into casefold
        return self.casefold() == other.casefold()

    def __ne__(self, other: object) -> bool:
        return self.casefold() != other.casefold()

    def __repr__(self) -> str:
        return repr(str(self))

    def __gt__(self, other: object) -> bool:
        return self.casefold() > other
    
    def __ge__(self, other: object) -> bool:
        return self.casefold() >= other

    def __lt__(self, other: object) -> bool:
        return self.casefold() < other

    def __le__(self, other: object) -> bool:
        return self.casefold() <= other

    def __add__(self, other: object) -> FuzzyString:
        return FuzzyString(str(self) + other)

    def __contains__(self, needle: object) -> bool:
        return needle.casefold() in self.casefold()
