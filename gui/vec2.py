# # TODO Marked for removal
# # class Rect:
# #     def __init__(self, x0, y0, x1, y1):
# #         self.p1 = Vec2(x0, y0)
# #         self.p2 = Vec2(x1, y1)

# #     def __repr__(self) -> str:
# #         return f"Rect({self.p1}, {self.p2})"

# #     def contains(self, point: 'Vec2') -> bool:
# #         return (self.p1.x <= point.x
# #                 and self.p1.y <= point.y
# #                 and self.p2.x > point.x
# #                 and self.p2.y > point.y)


class Vec2:
    def __init__(self, *args):
        """
        Initializes a new Vec2 instance. `args` is expected to be one of the following:
        - A single `number`: Initializes both coordinates to this value.
        - Two `numbers`: Uses these as the `x` and `y` coordinates, respectively.
        - Another `Vec2`: Creates a copy of the given `Vec2` instance.
        """
        assert (len(args) > 0 and len(args) <= 2)

        if isinstance(args[0], self.__class__):
            # copy self
            self.__init__(*[c for c in args[0]._coords])
        elif len(args) == 1:
            self.__init__(*[args[0] for i in range(2)])
        else:
            self._coords = tuple([c for c in args])

    def __repr__(self) -> str:
        return f"Vec2({self.x}, {self.y})"

    @property
    def x(self) -> float:
        return self._coords[0]

    @property
    def y(self) -> float:
        return self._coords[1]

    def __add__(self, other: 'Vec2 | float') -> 'Vec2':
        if isinstance(other, self.__class__):
            coords = [c1 + c2 for c1, c2 in zip(self._coords, other._coords)]
            return self.__class__(*coords)
        else:
            return self + self.__class__(other)

    def __neg__(self) -> 'Vec2':
        return self.__class__(*[-c for c in self._coords])

    def __sub__(self, other: 'Vec2 | float') -> 'Vec2':
        return self + (-other)

    def __mul__(self, other: 'Vec2 | float') -> 'Vec2':
        if isinstance(other, self.__class__):
            coords = [c1 * c2 for c1, c2 in zip(self._coords, other._coords)]
            return self.__class__(*coords)
        else:
            return self * self.__class__(other)

    def __truediv__(self, other: 'Vec2 | float') -> 'Vec2':
        if isinstance(other, self.__class__):
            coords = [c1 / c2 for c1, c2 in zip(self._coords, other._coords)]
            return self.__class__(*coords)
        else:
            # assumes dividend is a scalar
            return self / self.__class__(other)

    def _floor(self) -> 'Vec2':
        return self.__class__(*[int(c) for c in self._coords])

    def __floordiv__(self, other: 'Vec2 | float') -> 'Vec2':
        return (self / other)._floor()
