"""Interval class, implements interval arithmetic.

written by microsoft copilot Sep 26, 2026
modified by Timothy Woodard Sep 26, 2026
"""
import numpy as np


class Interval:
    """Basic interval arithmetic object supporting +, -, *, /, unary ops, pow, abs, exp, log, trig, comparisons,
    intersection, union, containment with correct endpoint propagation.
    """
    def __init__(self, min_val, max_val=None):
        if max_val is None:
            max_val = min_val
            
        if min_val > max_val:
            temp = min_val
            min_val = max_val
            max_val = temp
       
        self.min = float(min_val)
        self.max = float(max_val)

    def __repr__(self):
        return f"Interval({self.min}, {self.max})"

    # --- Helpers ---
    def _extract(self, other):
        if isinstance(other, np.ndarray):
            return np.min(other), np.max(other)
        elif isinstance(other, Interval):
            return other.min, other.max
        else:
            return float(other), float(other)

    # --- Arithmetic ---
    def __add__(self, other):
        o_min, o_max = self._extract(other)
        return Interval(self.min + o_min, self.max + o_max)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        o_min, o_max = self._extract(other)
        return Interval(self.min - o_max, self.max - o_min)

    def __rsub__(self, other):
        o_min, o_max = self._extract(other)
        return Interval(o_min - self.max, o_max - self.min)

    def __mul__(self, other):
        o_min, o_max = self._extract(other)
        candidates = [
            self.min * o_min,
            self.min * o_max,
            self.max * o_min,
            self.max * o_max,
        ]
        return Interval(min(candidates), max(candidates))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        o_min, o_max = self._extract(other)
        if o_min <= 0 <= o_max:
            raise ZeroDivisionError("Interval crosses zero; division undefined.")
        candidates = [
            self.min / o_min,
            self.min / o_max,
            self.max / o_min,
            self.max / o_max,
        ]
        return Interval(min(candidates), max(candidates))

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
        return Interval(min(candidates), max(candidates))

    # -------------------------
    # Unary operators
    # -------------------------
    def __neg__(self):
        return Interval(-self.max, -self.min)

    def __pos__(self):
        return Interval(self.min, self.max)

    def __abs__(self):
        if self.min >= 0:
            return Interval(self.min, self.max)
        if self.max <= 0:
            return Interval(-self.max, -self.min)
        return Interval(0, max(-self.min, self.max))

    # -------------------------
    # Power
    # -------------------------
    def __pow__(self, exponent):
        if isinstance(exponent, Interval):
            raise NotImplementedError("Interval exponent not supported.")

        if exponent == 0:
            return Interval(1, 1)

        if exponent < 0:
            return (Interval(1, 1) / (self ** (-exponent)))

        # even exponent
        if exponent % 2 == 0:
            candidates = [self.min**exponent, self.max**exponent]
            if self.min < 0 < self.max:
                candidates.append(0)
            return Interval(min(candidates), max(candidates))

        # odd exponent
        return Interval(self.min**exponent, self.max**exponent)

    # -------------------------
    # exp, log, sqrt
    # -------------------------
    def exp(self):
        """e^[a,b] = [e^a, e^b]"""
        return Interval(np.exp(self.min), np.exp(self.max))

    def log(self):
        if self.min <= 0:
            raise ValueError("log undefined for intervals crossing zero.")
        return Interval(np.log(self.min), np.log(self.max))

    def sqrt(self):
        if self.min < 0:
            raise ValueError("sqrt undefined for negative intervals.")
        return Interval(np.sqrt(self.min), np.sqrt(self.max))

    # -------------------------
    # Trigonometric functions
    # -------------------------
    def sin(self):
        # full-cycle bounding
        lo, hi = self.min, self.max
        # If interval spans >= 2π, result is [-1,1]
        if hi - lo >= 2 * np.pi:
            return Interval(-1, 1)

        # Evaluate endpoints
        candidates = [np.sin(lo), np.sin(hi)]

        # Check if interval contains a max or min of sine
        # max at π/2 + 2πk, min at 3π/2 + 2πk
        for k in range(-3, 4):
            peak = np.pi/2 + 2*np.pi*k
            trough = 3*np.pi/2 + 2*np.pi*k
            if lo <= peak <= hi:
                candidates.append(1)
            if lo <= trough <= hi:
                candidates.append(-1)

        return Interval(min(candidates), max(candidates))

    def cos(self):
        lo, hi = self.min, self.max
        if hi - lo >= 2 * np.pi:
            return Interval(-1, 1)

        candidates = [np.cos(lo), np.cos(hi)]

        for k in range(-3, 4):
            peak = 0 + 2*np.pi*k
            trough = np.pi + 2*np.pi*k
            if lo <= peak <= hi:
                candidates.append(1)
            if lo <= trough <= hi:
                candidates.append(-1)

        return Interval(min(candidates), max(candidates))

    def tan(self):
        lo, hi = self.min, self.max
        # tan blows up at π/2 + πk
        for k in range(-3, 4):
            asym = np.pi/2 + np.pi*k
            if lo <= asym <= hi:
                raise ValueError("tan undefined: interval crosses asymptote.")

        return Interval(np.tan(lo), np.tan(hi))

    # -------------------------
    # Comparisons (interval logic)
    # -------------------------
    def __eq__(self, other):
        o_min, o_max = self._extract(other)
        return self.min == o_min and self.max == o_max

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        o_min, o_max = self._extract(other)
        return self.max < o_min

    def __le__(self, other):
        o_min, o_max = self._extract(other)
        return self.max <= o_max

    def __gt__(self, other):
        o_min, o_max = self._extract(other)
        return self.min > o_max

    def __ge__(self, other):
        o_min, o_max = self._extract(other)
        return self.min >= o_min

    # -------------------------
    # Containment
    # -------------------------
    def __contains__(self, value):
        return self.min <= value <= self.max

    # -------------------------
    # Intersection & Union
    # -------------------------
    def intersection(self, other):
        o_min, o_max = self._extract(other)
        lo = max(self.min, o_min)
        hi = min(self.max, o_max)
        if lo > hi:
            return None
        return Interval(lo, hi)

    def union(self, other):
        o_min, o_max = self._extract(other)
        return Interval(min(self.min, o_min), max(self.max, o_max))


def sin(arg):
    if arg is Interval:
        return arg.sin()
    else:
        return np.sin(arg)


def cos(arg):
    if arg is Interval:
        return arg.cos()
    else:
        return np.cos(arg)


def tan(arg):
    if arg is Interval:
        return arg.tan()
    else:
        return np.tan(arg)


def sqrt(arg):
    if arg is Interval:
        return arg.sqrt()
    else:
        return np.sqrt(arg)


def main() -> None:
    # Test:
    A = Interval(2, 1)
    print(f"A = {A}")
    
    B = Interval(1, 2)
    print(f"B = {B}")
    
    C = 2.0 * A
    print(f"C = {C}")
    
    D = B + 1.0
    print(f"D = {D}")
    
    sD = sqrt(D)
    print(f"sqrt(D) = {sD}")
    
    E = A - 3.0
    print(f"E = {E}")
    
    F = B / 3.0
    print(f"F = {F}")
    
    print(f"A + B = {A + B}")
    print(f"A - B = {A - B}")
    print(f"A * B = {A * B}")
    print(f"A / Interval(1, 2) = {A / Interval(1, 2)}")
    
    print(f"A == B: {A==B}")

    x = Interval(-2, 3)
    
    print(f"x = {x}")
    print(f"-x = {-x}")
    print(f"abs(x) = {abs(x)}")
    print(f"x**2 = {x**2}")
    print(f"x.exp() = {x.exp()}")
    print(f"x.sin() = {x.sin()}")
    print(f"interval.sin(x) = {sin(x)}")
    print(f"1 in x = {1 in x}")
    print(f"x.intersection(Interval(1, 10)) = {x.intersection(Interval(1, 10))}")


    # Special tests for trigonometry:
    theta = Interval(np.pi/8.0, np.pi/8.0+0.001)
    theta = Interval(-0.001, +0.001)
    # theta = Interval(np.pi/2.0-0.001, np.pi/2.0+0.001)
    theta = Interval(np.pi-0.001, np.pi+0.001)
    
    print(f"sin(theta) = {sin(theta)}")
    print(f"cos(theta) = {cos(theta)}")
    print(f"tan(theta) = {tan(theta)}")


    # Special tests for comparisons:
    val1 = Interval(1, 4)
    val2 = Interval(2, 3)
    
    print(f"val1 > val2 = {val1 > val2}")
    print(f"val1 < val2 = {val1 < val2}")
    print(f"val1 == val2 = {val1 == val2}")
    print(f"val1 != val2 = {val1 != val2}")


    array = np.array([1,2,3,4,5])
    
    
    try:
        val3 = val1 * array
        print(f"val3 = {val3}")
    except:
        print("failed...")


if __name__ == "__main__":
    main()
    