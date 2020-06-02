from settings import Settings


class Segment:

    def __init__(self, point_from: tuple, point_to: tuple, _id: int):
        self.point_from = point_from
        self.point_to = point_to
        self._id = _id
        self.is_horizontal = self.isHorizontal()
        self.neighbours_ids = self.previousNeighboursIds()
        self.neighbours_ids.extend(self.nextNeighboursIds())

    def isHorizontal(self) -> bool:
        return self.point_from[0] == self.point_to[0] and self.point_from[1] == self.point_to[1] - 1

    def previousNeighboursIds(self):
        if self.is_horizontal:
            return [self._id - 2 * Settings.BOARD_DIMENSION - 2, self._id - 2 * Settings.BOARD_DIMENSION - 1, self._id - 2 * Settings.BOARD_DIMENSION]
        return [self._id - 1, self._id - 2, self._id + 2 * Settings.BOARD_DIMENSION]

    def nextNeighboursIds(self):
        if self.is_horizontal:
            return [self._id - 1, self._id + 1, self._id + 2 * Settings.BOARD_DIMENSION + 1]
        return [self._id + 1, self._id + 2, self._id + 2 * Settings.BOARD_DIMENSION + 2]

    def toString(self) -> str:
        return "({0},{1}) -> ({2},{3})".format(self.point_from[0], self.point_from[1], self.point_to[0], self.point_to[1])
