import constants
from game.casting.actor import Actor
from game.shared.point import Point


class Cycle2(Actor):
    """
       
    The responsibility of Cycle is to move itself.

    Attributes:
        _points (int): The number of points the food is worth.
    """
    def __init__(self):
        super().__init__()
        self._segments2 = []
        self._prepare_body2()

    def get_segments2(self):
        return self._segments2

    def move_next(self):
        # move all segments
        for segment2 in self._segments2:
            segment2.move_next()
        # update velocities
        for i in range(len(self._segments2) - 1, 0, -1):
            trailing = self._segments2[i]
            previous = self._segments2[i - 1]
            velocity = previous.get_velocity()
            trailing.set_velocity(velocity)

    def get_head2(self):
        return self._segments2[0]

    def grow_tail2(self, number_of_segments2):
        for i in range(number_of_segments2):
            tail = self._segments2[-1]
            velocity = tail.get_velocity()
            offset = velocity.reverse()
            position = tail.get_position().add(offset)
            
            segment2 = Actor()
            segment2.set_position(position)
            segment2.set_velocity(velocity)
            segment2.set_text("#")
            segment2.set_color(constants.RED)
            self._segments2.append(segment2)

    def turn_head2(self, velocity):
        self._segments2[0].set_velocity(velocity)
    
    def _prepare_body2(self):
        x = int(constants.MAX_X / 2)
        y = int(constants.MAX_Y / 4)

        for i in range(constants.CYCLE_LENGTH):
            position = Point(x - i * constants.CELL_SIZE, y)
            velocity = Point(1 * constants.CELL_SIZE, 0)
            text = "8" if i == 0 else "#"
            color = constants.RED if i == 0 else constants.RED
            
            segment2 = Actor()
            segment2.set_position(position)
            segment2.set_velocity(velocity)
            segment2.set_text(text)
            segment2.set_color(color)
            self._segments2.append(segment2)