import pyray
import random

class Color:
    def __init__(self, red, green, blue, alpha = 255):
        self._red = red
        self._green = green
        self._blue = blue 
        self._alpha = alpha
    def to_tuple(self):
        return (self._red, self._green, self._blue, self._alpha)

class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    def add(self, other):
        x = self._x + other.get_x()
        y = self._y + other.get_y()
        return Point(x, y)    
    def equals(self, other):
        return self._x == other.get_x() and self._y == other.get_y()
    def get_x(self):
        return self._x
    def get_y(self):
        return self._y
    def reverse(self):
        new_x = self._x * -1
        new_y = self._y * -1
        return Point(new_x, new_y)
    def scale(self, factor):
        return Point(self._x * factor, self._y * factor)
    
class VideoService:
    def __init__(self, debug = False):
        self._debug = debug
    def close_window(self):
        pyray.close_window()
    def clear_buffer(self):
        pyray.begin_drawing()
        pyray.clear_background(pyray.BLACK)
        if self._debug == True:
            self._draw_grid()
    def draw_actor(self, actor, centered=False):
        text = actor.get_text()
        x = actor.get_position().get_x()
        y = actor.get_position().get_y()
        font_size = actor.get_font_size()
        color = actor.get_color().to_tuple()
        if centered:
            width = pyray.measure_text(text, font_size)
            offset = int(width / 2)
            x -= offset
        pyray.draw_text(text, x, y, font_size, color)
    
    def draw_actor2(self, actor, centered=False):
        text = actor.get_text()
        x = actor.get_position2().get_x()
        y = actor.get_position2().get_y()
        font_size = actor.get_font_size()
        color = actor.get_color().to_tuple()
        if centered:
            width = pyray.measure_text(text, font_size)
            offset = int(width / 2)
            x -= offset
        pyray.draw_text(text, x, y, font_size, color)    
        
    def draw_actors(self, actors, centered=False):
        for actor in actors:
            self.draw_actor(actor, centered)
    def flush_buffer(self):
        pyray.end_drawing()
    def is_window_open(self):
        return not pyray.window_should_close()
    def open_window(self):
        pyray.init_window(MAX_X, MAX_Y, CAPTION, CAPTION2)
        pyray.set_target_fps(FRAME_RATE)
    def _draw_grid(self):
        for y in range(0, MAX_Y, CELL_SIZE):
            pyray.draw_line(0, y, MAX_X, y, pyray.GRAY)    
        for x in range(0, MAX_X, CELL_SIZE):
            pyray.draw_line(x, 0, x, MAX_Y, pyray.GRAY)
    def _get_x_offset(self, text, font_size):
        width = pyray.measure_text(text, font_size)
        return int(width / 2)    
        
class KeyboardService:
    def __init__(self):
        self._keys = {}
        self._keys['w'] = pyray.KEY_W
        self._keys['a'] = pyray.KEY_A
        self._keys['s'] = pyray.KEY_S
        self._keys['d'] = pyray.KEY_D

        self._keys['i'] = pyray.KEY_I
        self._keys['j'] = pyray.KEY_J
        self._keys['k'] = pyray.KEY_K
        self._keys['l'] = pyray.KEY_L
        
    def is_key_up(self, key):
        pyray_key = self._keys[key.lower()]
        return pyray.is_key_up(pyray_key)

    def is_key_down(self, key):
        pyray_key = self._keys[key.lower()]
        return pyray.is_key_down(pyray_key)        
        
COLUMNS = 40
ROWS = 20
CELL_SIZE = 15
MAX_X = 900
MAX_Y = 600
FRAME_RATE = 15
FONT_SIZE = 15
CAPTION = "Cycle"
CAPTION2 = "Cycle2"
CYCLE_LENGTH = 8
WHITE = Color(255, 255, 255)
RED = Color(255, 0, 0)
YELLOW = Color(255, 255, 0)
GREEN = Color(0, 255, 0)

class Actor:
    
    def __init__(self):
        self._text = ""
        self._font_size = 15
        self._color = Color(255, 255, 255)
        self._position = Point(0, 0)
        self._position2 = Point(0, 20)
        self._velocity = Point(0, 0)

    def get_color(self):
        return self._color

    def get_font_size(self):
        return self._font_size

    def get_position(self):
        return self._position
    
    def get_position2(self):
        return self._position2
    
    def get_text(self):
        return self._text

    def get_velocity(self):
        return self._velocity
    
    def move_next(self):
        x = (self._position.get_x() + self._velocity.get_x()) % MAX_X
        y = (self._position.get_y() + self._velocity.get_y()) % MAX_Y
        self._position = Point(x, y)

    def set_color(self, color):
        self._color = color

    def set_position(self, position):
        self._position = position
        
    def set_position2(self, position):
        self._position2 = position
    
    def set_font_size(self, font_size):
        self._font_size = font_size
    
    def set_text(self, text):
        self._text = text

    def set_velocity(self, velocity):
        self._velocity = velocity

class Cycle(Actor):
    def __init__(self):
        super().__init__()
        self._segments = []
        self._prepare_body()

    def get_segments(self):
        return self._segments

    def move_next(self):
        for segment in self._segments:
            segment.move_next()
    
        for i in range(len(self._segments) - 1, 0, -1):
            trailing = self._segments[i]
            previous = self._segments[i - 1]
            velocity = previous.get_velocity()
            trailing.set_velocity(velocity)

    def get_head(self):
        return self._segments[0]

    def grow_tail(self, number_of_segments):
        for i in range(number_of_segments):
            tail = self._segments[-2]
            velocity = tail.get_velocity()
            offset = velocity.reverse()
            position = tail.get_position().add(offset)
            
            segment = Actor()
            segment.set_position(position)
            segment.set_velocity(velocity)
            segment.set_text("#")
            segment.set_color(GREEN)
            self._segments.append(segment)

    def turn_head(self, velocity):
        self._segments[0].set_velocity(velocity)
    
    def _prepare_body(self):
        x = int(MAX_X / 2)
        y = int(MAX_Y / 2)

        for i in range(CYCLE_LENGTH):
            position = Point(x - i * CELL_SIZE, y)
            velocity = Point(1 * CELL_SIZE, 0)
            text = "8" if i == 0 else "#"
            color = YELLOW if i == 0 else GREEN
            
            segment = Actor()
            segment.set_position(position)
            segment.set_velocity(velocity)
            segment.set_text(text)
            segment.set_color(color)
            self._segments.append(segment)

class Cycle2(Actor):
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
            tail = self._segments2[-2]
            velocity = tail.get_velocity()
            offset = velocity.reverse()
            position = tail.get_position().add(offset)
            
            segment2 = Actor()
            segment2.set_position(position)
            segment2.set_velocity(velocity)
            segment2.set_text("#")
            segment2.set_color(RED)
            self._segments2.append(segment2)

    def turn_head2(self, velocity):
        self._segments2[0].set_velocity(velocity)
    
    def _prepare_body2(self):
        x = int(MAX_X / 2)
        y = int(MAX_Y / 4)

        for i in range(CYCLE_LENGTH):
            position = Point(x - i * CELL_SIZE, y)
            velocity = Point(1 * CELL_SIZE, 0)
            text = "8" if i == 0 else "#"
            color = RED if i == 0 else RED
            
            segment2 = Actor()
            segment2.set_position(position)
            segment2.set_velocity(velocity)
            segment2.set_text(text)
            segment2.set_color(color)
            self._segments2.append(segment2)

class Score(Actor):
    def __init__(self):
        super().__init__()
        self._points = 0
        self.add_points(0)

    def add_points(self, points):
        self._points += points
        self.set_text(f"Score: {self._points}")

class Score2(Actor):
    def __init__(self):
        super().__init__()
        self._points = 0
        self.add_points2(0)

    def add_points2(self, points):
        self._points += points
        self.set_text(f"Score2: {self._points}")

class Food(Actor):
    def __init__(self):
        super().__init__()
        self._points = 0
        self.set_text("@")
        self.set_color(RED)
        self.reset()
        
    def reset(self):
        self._points = random.randint(1, 8)
        x = random.randint(1, COLUMNS - 1)
        y = random.randint(1, ROWS - 1)
        position = Point(x, y)
        position = position.scale (CELL_SIZE)
        self.set_position(position)
        
    def get_points(self):
        return self._points
    
class Cast:
    def __init__(self):
        self._actors = {}
        
    def add_actor(self, group, actor):
        if not group in self._actors.keys():
            self._actors[group] = []
            
        if not actor in self._actors[group]:
            self._actors[group].append(actor)

    def get_actors(self, group):
        results = []
        if group in self._actors.keys():
            results = self._actors[group].copy()
        return results
    
    def get_all_actors(self):
        results = []
        for group in self._actors:
            results.extend(self._actors[group])
        return results

    def get_first_actor(self, group):
        result = None
        if group in self._actors.keys():
            result = self._actors[group][0]
        return result
    
    
    def remove_actor(self, group, actor):
        if group in self._actors:
            self._actors[group].remove(actor)
    
class Action:
    def execute(self, cast, script):
        pass
    
class ControlActorsAction(Action):
    def __init__(self, keyboard_service):
        self._keyboard_service = keyboard_service
        self._direction = Point(CELL_SIZE, 0)

    def execute(self, cast, script):
        # left
        if self._keyboard_service.is_key_down('a'):
            self._direction = Point(-CELL_SIZE, 0)
        
        # right
        if self._keyboard_service.is_key_down('d'):
            self._direction = Point(CELL_SIZE, 0)
        
        # up
        if self._keyboard_service.is_key_down('w'):
            self._direction = Point(0, -CELL_SIZE)
        
        # down
        if self._keyboard_service.is_key_down('s'):
            self._direction = Point(0, CELL_SIZE)
        
        cycle = cast.get_first_actor("cycles")
        cycle.turn_head(self._direction)

class ControlActorsAction2(Action):
    def __init__(self, keyboard_service):
        self._keyboard_service = keyboard_service
        self._direction = Point(CELL_SIZE, 0)

    def execute(self, cast, script):
        # left
        if self._keyboard_service.is_key_down('j'):
            self._direction = Point(-CELL_SIZE, 0)
        
        # right
        if self._keyboard_service.is_key_down('l'):
            self._direction = Point(CELL_SIZE, 0)
        
        # up
        if self._keyboard_service.is_key_down('i'):
            self._direction = Point(0, -CELL_SIZE)
        
        # down
        if self._keyboard_service.is_key_down('k'):
            self._direction = Point(0, CELL_SIZE)
        
        cycle2 = cast.get_first_actor("cycles2")
        cycle2.turn_head2(self._direction)

class DrawActorsAction(Action):
    def __init__(self, video_service):
        self._video_service = video_service

    def execute(self, cast, script):
        score = cast.get_first_actor("scores")
        score2 = cast.get_first_actor("scores2")
        food = cast.get_first_actor("foods")
        cycle = cast.get_first_actor("cycles")
        cycle2 = cast.get_first_actor("cycles2")
        segments = cycle.get_segments()
        segments2 = cycle2.get_segments2()
        messages = cast.get_actors("messages")

        self._video_service.clear_buffer()
        self._video_service.draw_actor(food)
        self._video_service.draw_actors(segments)
        self._video_service.draw_actors(segments2)
        self._video_service.draw_actor(score)
        self._video_service.draw_actor2(score2)
        self._video_service.draw_actors(messages, True)
        self._video_service.flush_buffer()
   
class MoveActorsAction(Action):
    def execute(self, cast, script):
        actors = cast.get_all_actors()
        for actor in actors:
            actor.move_next()

class MoveActorsAction2(Action):
    def execute(self, cast, script):
        actors = cast.get_all_actors()
        for actor in actors:
            actor.move_next2()
 
class HandleCollisionsAction(Action):
    def __init__(self):
        self._is_game_over = False

    def execute(self, cast, script):
        if not self._is_game_over:
            self._handle_food_collision(cast)
            self._handle_segment_collision(cast)
            self._handle_game_over(cast)

    def _handle_food_collision(self, cast):
        score = cast.get_first_actor("scores")
        score2 = cast.get_first_actor("scores2")
        food = cast.get_first_actor("foods")
        cycle = cast.get_first_actor("cycles")
        cycle2 = cast.get_first_actor("cycles2")
        head = cycle.get_head()
        head2 = cycle2.get_head2()

        if head.get_position().equals(food.get_position()):
            points = food.get_points()
            cycle.grow_tail(points)
            cycle2.grow_tail2(points)
            score.add_points(points)
            score2.add_points2(points)
            food.reset()

        if head2.get_position().equals(food.get_position()):
            points = food.get_points()
            cycle.grow_tail(points)
            cycle2.grow_tail2(points)
            score.add_points(points)
            score2.add_points2(points)
            food.reset()
        
    def _handle_segment_collision(self, cast):
        cycle = cast.get_first_actor("cycles")
        cycle2 = cast.get_first_actor("cycles2")
        head = cycle.get_segments()[0]
        head2 = cycle2.get_segments2()[0]
        segments = cycle.get_segments()[1:]
        segments2 = cycle2.get_segments2()[1:]
        for segment in segments:
            if head.get_position().equals(segment.get_position()):
                self._is_game_over = True
        for segment in segments2:
            if head2.get_position().equals(segment.get_position()):
                self._is_game_over = True    
        
    def _handle_game_over(self, cast):
        if self._is_game_over:
            cycle = cast.get_first_actor("cycles")
            cycle2 = cast.get_first_actor("cycles2")
            segments = cycle.get_segments()
            segments2 = cycle2.get_segments2()
            food = cast.get_first_actor("foods")

            x = int(MAX_X / 2)
            y = int(MAX_Y / 2)
            position = Point(x, y)

            message = Actor()
            message.set_text("Game Over!")
            message.set_position(position)
            cast.add_actor("messages", message)

            for segment in segments:
                segment.set_color(WHITE)
            food.set_color(WHITE) 
            
            for segment in segments2:
                segment.set_color(WHITE)
            food.set_color(WHITE) 
 
class Director:
    def __init__(self, video_service):
        self._video_service = video_service
        
    def start_game(self, cast, script):
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._execute_actions("input", cast, script)
            self._execute_actions("update", cast, script)
            self._execute_actions("output", cast, script)
        self._video_service.close_window()

    def _execute_actions(self, group, cast, script):
        actions = script.get_actions(group)    
        for action in actions:
            action.execute(cast, script) 

class Script:
    def __init__(self):
        self._actions = {}
        
    def add_action(self, group, action):
        if not group in self._actions.keys():
            self._actions[group] = []
            
        if not action in self._actions[group]:
            self._actions[group].append(action)

    def get_actions(self, group):
        results = []
        if group in self._actions.keys():
            results = self._actions[group].copy()
        return results
    
    def remove_action(self, group, action):
        if group in self._actions:
            self._actions[group].remove(action)
    
def main():
    # create the cast
    cast = Cast()
    cast.add_actor("foods", Food())
    cast.add_actor("cycles", Cycle())
    cast.add_actor("scores", Score())
    cast.add_actor("scores2", Score2())
    cast.add_actor("cycles2", Cycle2())
    
   
    # start the game
    keyboard_service = KeyboardService()
    video_service = VideoService()

    script = Script()
    script.add_action("input", ControlActorsAction(keyboard_service))
    script.add_action("input", ControlActorsAction2(keyboard_service))
    script.add_action("update", MoveActorsAction())
    script.add_action("update", HandleCollisionsAction())
    script.add_action("output", DrawActorsAction(video_service))
    
    director = Director(video_service)
    director.start_game(cast, script)


if __name__ == "__main__":
    main()