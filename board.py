from segment import Segment
import hashlib


def getHash(available_segments: [], score: int):
    s = ','.join(str(segment._id) for segment in available_segments) + '-' + str(score)
    b = bytes(s, 'utf-8')
    m = hashlib.md5()
    m.update(b)
    return m.hexdigest()


class Board:

    def __init__(self, rows: int, columns: int):
        self.available_segments = []
        self.completed_segments = []
        self.last_completed_segment = None
        self.rows = rows
        self.columns = columns
        self.generateBoard(rows, columns)
        self.completeEdges(rows, columns)
        # self.printBoard()

    def generateBoard(self, rows: int, columns: int):
        _id = 0
        for x in range(rows + 1):
            for y in range(columns + 1):
                if x < rows:
                    self.available_segments.append(Segment((x, y), (x + 1, y), _id))
                    _id += 1
                if y < columns:
                    self.available_segments.append(Segment((x, y), (x, y + 1), _id))
                    _id += 1

    def getHash(self, score: int):
        return getHash(self.available_segments, score)

    def completeEdges(self, rows: int, columns: int):
        self.completed_segments = [segment for segment in self.available_segments if
                                   (segment.point_from[0] == segment.point_to[0] == 0
                                    or segment.point_from[0] == segment.point_to[0] == rows
                                    or segment.point_from[1] == segment.point_to[1] == 0
                                    or segment.point_from[1] == segment.point_to[1] == columns)]
        self.available_segments = [segment for segment in self.available_segments
                                   if segment not in self.completed_segments]

    def completeSegment(self, index: int):
        completed_segment = self.available_segments.pop(index)
        self.last_completed_segment = completed_segment
        self.completed_segments.append(completed_segment)

    def isComplete(self):
        return len(self.available_segments) == 0

    def getRewardWithSegment(self, last_completed_segment) -> int:
        reward = 0
        self.last_completed_segment = last_completed_segment
        if last_completed_segment.is_horizontal:
            if self.topSquareIsCompleted():
                reward += 1
            if self.bottomSquareIsCompleted():
                reward += 1
        else:
            if self.leftSquareIsCompleted():
                reward += 1
            if self.rightSquareIsCompleted():
                reward += 1
        return reward

    def getReward(self) -> int:
        return self.getRewardWithSegment(self.last_completed_segment)

    def topSquareIsCompleted(self) -> bool:
        return any(segment.point_from == (self.last_completed_segment.point_from[0] - 1, self.last_completed_segment.point_from[1])
                   and segment.point_to == self.last_completed_segment.point_from
                   for segment in self.completed_segments)\
               and any(segment.point_from == (self.last_completed_segment.point_from[0] - 1, self.last_completed_segment.point_from[1])
                    and segment.point_to == (self.last_completed_segment.point_to[0] - 1, self.last_completed_segment.point_to[1])
                    for segment in self.completed_segments)\
               and any(segment.point_from == (self.last_completed_segment.point_to[0] - 1, self.last_completed_segment.point_to[1])
                    and segment.point_to == self.last_completed_segment.point_to
                    for segment in self.completed_segments)

    def bottomSquareIsCompleted(self) -> bool:
        return any(segment.point_from == self.last_completed_segment.point_from
                   and segment.point_to == (self.last_completed_segment.point_from[0] + 1, self.last_completed_segment.point_from[1])
                   for segment in self.completed_segments)\
               and any(segment.point_from == (self.last_completed_segment.point_from[0] + 1, self.last_completed_segment.point_from[1])
                    and segment.point_to == (self.last_completed_segment.point_to[0] + 1, self.last_completed_segment.point_to[1])
                    for segment in self.completed_segments)\
               and any(segment.point_from == self.last_completed_segment.point_to
                       and segment.point_to == (self.last_completed_segment.point_to[0] + 1, self.last_completed_segment.point_to[1])
                    for segment in self.completed_segments)

    def leftSquareIsCompleted(self) -> bool:
        return any(segment.point_from == (self.last_completed_segment.point_from[0], self.last_completed_segment.point_from[1] - 1)
                   and segment.point_to == self.last_completed_segment.point_from
                   for segment in self.completed_segments)\
               and any(segment.point_from == (self.last_completed_segment.point_from[0], self.last_completed_segment.point_from[1] - 1)
                    and segment.point_to == (self.last_completed_segment.point_to[0], self.last_completed_segment.point_to[1] - 1)
                    for segment in self.completed_segments)\
               and any(segment.point_from == (self.last_completed_segment.point_to[0], self.last_completed_segment.point_to[1] - 1)
                    and segment.point_to == self.last_completed_segment.point_to
                    for segment in self.completed_segments)

    def rightSquareIsCompleted(self) -> bool:
        return any(segment.point_from == self.last_completed_segment.point_from
                   and segment.point_to == (self.last_completed_segment.point_from[0], self.last_completed_segment.point_from[1] + 1)
                   for segment in self.completed_segments)\
               and any(segment.point_from == (self.last_completed_segment.point_from[0], self.last_completed_segment.point_from[1] + 1)
                    and segment.point_to == (self.last_completed_segment.point_to[0], self.last_completed_segment.point_to[1] + 1)
                    for segment in self.completed_segments)\
               and any(segment.point_from == self.last_completed_segment.point_to
                    and segment.point_to == (self.last_completed_segment.point_to[0], self.last_completed_segment.point_to[1] + 1)
                    for segment in self.completed_segments)

    def printBoard(self):
        for x in range(self.rows + 1):
            line = ''
            for y in range(2 * self.columns + 1):
                line += '_' if y % 2 == 1 and any(segment.point_from == (x, (y - 1) / 2) and
                                                  segment.point_to == (x, (y - 1) / 2 + 1)
                                                  for segment in self.completed_segments) else\
                    ('|' if y % 2 == 0 and x > 0 and any(segment.point_from == (x - 1, y / 2)
                                                         and segment.point_to == (x, y / 2)
                                                         for segment in self.completed_segments) else ' ')
            print(line)
