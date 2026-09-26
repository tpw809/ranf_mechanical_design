"""Interval arithmetic?

Existing Python Packages:

- IntervalArithmetic
- PyIA
- python-intervals
- pyball
- PyInterval
"""


class TrackedVariable:
    """
    Represents a variable with a min/max range and supports interval arithmetic.
    """

    def __init__(self, min_val, max_val=None):
        if max_val is None:
            max_val = min_val
        self.min = float(min_val)
        self.max = float(max_val)

    def __repr__(self):
        return f"TrackedVariable(min={self.min}, max={self.max})"

    def _extract(self, other):
        if isinstance(other, TrackedVariable):
            return other.min, other.max
        else:
            return float(other), float(other)

    # --- Interval Arithmetic Helpers ---
    def _combine_add(self, other_min, other_max):
        return TrackedVariable(self.min + other_min,
                               self.max + other_max)

    def _combine_sub(self, other_min, other_max):
        return TrackedVariable(self.min - other_max,
                               self.max - other_min)

    def _combine_mul(self, other_min, other_max):
        candidates = [
            self.min * other_min,
            self.min * other_max,
            self.max * other_min,
            self.max * other_max,
        ]
        return TrackedVariable(min(candidates), max(candidates))

    def _combine_div(self, other_min, other_max):
        if other_min <= 0 <= other_max:
            raise ZeroDivisionError("Interval crosses zero; division undefined.")
        candidates = [
            self.min / other_min,
            self.min / other_max,
            self.max / other_min,
            self.max / other_max,
        ]
        return TrackedVariable(min(candidates), max(candidates))

    # --- Arithmetic Operators ---
    def __add__(self, other):
        o_min, o_max = self._extract(other)
        return self._combine_add(o_min, o_max)

    def __sub__(self, other):
        o_min, o_max = self._extract(other)
        return self._combine_sub(o_min, o_max)

    def __mul__(self, other):
        o_min, o_max = self._extract(other)
        return self._combine_mul(o_min, o_max)

    def __truediv__(self, other):
        o_min, o_max = self._extract(other)
        return self._combine_div(o_min, o_max)

    # Reverse ops
    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        o_min, o_max = self._extract(other)
        return TrackedVariable(o_min - self.max, o_max - self.min)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        o_min, o_max = self._extract(other)
        if self.min <= 0 <= self.max:
            raise ZeroDivisionError("Interval crosses zero; division undefined.")
        candidates = [
            o_min / self.min,
            o_min / self.max,
            o_max / self.min,
            o_max / self.max,
        ]
        return TrackedVariable(min(candidates), max(candidates))




def main() -> None:
    # test:
    A = TrackedVariable(2, 5)
    B = TrackedVariable(-3, 4)
    
    C = A + B
    D = A * B
    E = A - B
    
    print(C)   # min=-1, max=9
    print(D)   # min=-15, max=20
    print(E)   # min=-2, max=8
    
    

if __name__ == "__main__":
    main()
    