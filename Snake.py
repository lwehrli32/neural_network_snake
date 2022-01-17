# importing libraries
import turtle
import random
import time
from RecordData import DataRecorder


class SnakeGame:

    def __init__(self, user=False, game_number=0):

        self.data_recorder = DataRecorder()
        self.game_number = game_number + 1

        # creating turtle screen
        self.screen = turtle.Screen()
        self.screen.title('SNAKE GAME')
        self.screen.setup(width=700, height=700)
        self.screen.tracer(0)
        self.screen.bgcolor('white')

        # creating a border for our game
        self.tracer = turtle.Turtle()
        self.tracer.speed(5)
        self.tracer.pensize(4)
        self.tracer.penup()
        self.tracer.goto(-310, 250)
        self.tracer.pendown()
        self.tracer.color('black')
        self.tracer.forward(600)
        self.tracer.right(90)
        self.tracer.forward(500)
        self.tracer.right(90)
        self.tracer.forward(600)
        self.tracer.right(90)
        self.tracer.forward(500)
        self.tracer.penup()
        self.tracer.hideturtle()

        # score
        self.score = 0
        self.delay = 0.1

        # snake
        self.snake = turtle.Turtle()
        self.snake.speed(0)
        self.snake.shape('square')
        self.snake.color("black")
        self.snake.penup()
        self.snake.goto(0, 0)
        self.snake.direction = 'right'

        # food
        self.fruit = turtle.Turtle()
        self.fruit.speed(0)
        self.fruit.shape('circle')
        self.fruit.color('red')
        self.fruit.penup()
        self.fruit.goto(30, 30)

        self.old_fruit = []

        # scoring
        self.scoring = turtle.Turtle()
        self.scoring.speed(0)
        self.scoring.color("black")
        self.scoring.penup()
        self.scoring.hideturtle()
        self.scoring.goto(0, 300)
        self.scoring.write("Score: 0  Game number: " + str(self.game_number), align="center",
                           font=("Courier", 24, "bold"))

        self.is_done = False
        self.action = 0

        if user:
            self.render_keys()

    def render_keys(self):
        self.screen.listen()
        self.screen.onkeypress(self.snake_go_up, "Up")
        self.screen.onkeypress(self.snake_go_down, "Down")
        self.screen.onkeypress(self.snake_go_left, "Left")
        self.screen.onkeypress(self.snake_go_right, "Right")

    def snake_go_up(self):
        if self.snake.direction != "down":
            self.set_action('up')
            self.snake.direction = "up"

    def snake_go_down(self):
        if self.snake.direction != "up":
            self.set_action('down')
            self.snake.direction = "down"

    def snake_go_left(self):
        if self.snake.direction != "right":
            self.set_action('left')
            self.snake.direction = "left"

    def snake_go_right(self):
        if self.snake.direction != "left":
            self.set_action('right')
            self.snake.direction = "right"

    def snake_move(self):
        if self.snake.direction == "up":
            y = self.snake.ycor()
            self.snake.sety(y + 20)

        if self.snake.direction == "down":
            y = self.snake.ycor()
            self.snake.sety(y - 20)

        if self.snake.direction == "left":
            x = self.snake.xcor()
            self.snake.setx(x - 20)

        if self.snake.direction == "right":
            x = self.snake.xcor()
            self.snake.setx(x + 20)

    def set_action(self, action):
        snake_dir = self.snake.direction
        new_action = 0
        if snake_dir == 'up':
            if action == 'up':
                new_action = 0
            elif action == 'right':
                new_action = 1
            elif action == 'left':
                new_action = -1
        elif snake_dir == 'down':
            if action == 'down':
                new_action = 0
            elif action == 'left':
                new_action = 1
            elif action == 'right':
                new_action = -1
        elif snake_dir == 'right':
            if action == 'right':
                new_action = 0
            elif action == 'down':
                new_action = 1
            elif action == 'up':
                new_action = -1
        elif snake_dir == 'left':
            if action == 'left':
                new_action = 0
            elif action == 'up':
                new_action = 1
            elif action == 'down':
                new_action = -1

        self.action = new_action

    def is_overlapping(self, left, front, right, fruit):
        can_turn = [1,1,1]
        s_top = self.snake.ycor() + 10
        s_bottom = self.snake.ycor() - 10
        s_right = self.snake.xcor() + 10
        s_left = self.snake.xcor() - 10

        try:
            f_top = fruit.top
            f_bottom = fruit.bottom
            f_left = fruit.left
            f_right = fruit.right
        except Exception as e:
            print(e)
            return True

        if left == 'right' or front == 'right' or right == 'right':
            if f_right >= s_right + 20 > f_left and s_top == f_top:
                if left == 'right':
                    can_turn[0] = 0
                elif front == 'right':
                    can_turn[1] = 0
                elif right == 'right':
                    can_turn[2] = 0
        elif left == 'left' or front == 'left' or right == 'left':
            if f_left <= s_left - 20 < f_right and s_top == f_top:
                if left == 'left':
                    can_turn[0] = 0
                elif front == 'left':
                    can_turn[1] = 0
                elif right == 'left':
                    can_turn[2] = 0
        elif left == 'up' or front == 'up' or right == 'up':
            if f_top >= s_top + 20 > f_bottom and s_right == f_right:
                if left == 'up':
                    can_turn[0] = 0
                elif front == 'up':
                    can_turn[1] = 0
                elif right == 'up':
                    can_turn[2] = 0
        elif left == 'down' or front == 'down' or right == 'down':
            if f_bottom <= s_bottom - 20 < f_top and s_right == f_right:
                if left == 'down':
                    can_turn[0] = 0
                elif front == 'down':
                    can_turn[1] = 0
                elif right == 'down':
                    can_turn[2] = 0
        return can_turn

    def find_obs(self):
        # left, front, right
        can_turn = [1, 1, 1]

        if len(self.old_fruit) > 0:

            # find if you can turn that direction
            for i, fruit in enumerate(self.old_fruit):
                if self.snake.direction == 'right':
                    can_turn = self.is_overlapping('up', 'right', 'down', fruit)
                    if self.snake.xcor() >= 240 - 10:
                        can_turn[0] = 0
                    if self.snake.xcor() >= 280 - 10:
                        can_turn[1] = 0
                    if self.snake.xcor() <= -240 + 10:
                        can_turn[2] = 0
                elif self.snake.direction == 'left':
                    can_turn = self.is_overlapping('down', 'left', 'up', fruit)
                    if self.snake.xcor() <= -240 + 10:
                        can_turn[0] = 0
                    if self.snake.xcor() <= -300 + 10:
                        can_turn[1] = 0
                    if self.snake.xcor() >= 240 - 10:
                        can_turn[2] = 0
                elif self.snake.direction == 'up':
                    can_turn = self.is_overlapping('left', 'up', 'right', fruit)
                    if self.snake.xcor() <= -300 + 10:
                        can_turn[0] = 0
                    if self.snake.xcor() >= 240 - 10:
                        can_turn[1] = 0
                    if self.snake.xcor() >= 280 - 10:
                        can_turn[2] = 0
                elif self.snake.direction == 'down':
                    can_turn = self.is_overlapping('right', 'down', 'left', fruit)
                    if self.snake.xcor() <= -300 + 10:
                        can_turn[2] = 0
                    if self.snake.xcor() <= -240 + 10:
                        can_turn[1] = 0
                    if self.snake.xcor() >= 280 - 10:
                        can_turn[0] = 0
        else:
            if self.snake.direction == 'right':
                if self.snake.xcor() >= 240 - 10:
                    can_turn[0] = 0
                if self.snake.xcor() >= 280 - 10:
                    can_turn[1] = 0
                if self.snake.xcor() <= -240 + 10:
                    can_turn[2] = 0
            elif self.snake.direction == 'left':
                if self.snake.xcor() <= -240 + 10:
                    can_turn[0] = 0
                if self.snake.xcor() <= -300 + 10:
                    can_turn[1] = 0
                if self.snake.xcor() >= 240 - 10:
                    can_turn[2] = 0
            elif self.snake.direction == 'up':
                if self.snake.xcor() <= -300 + 10:
                    can_turn[0] = 0
                if self.snake.xcor() >= 240 - 10:
                    can_turn[1] = 0
                if self.snake.xcor() >= 280 - 10:
                    can_turn[2] = 0
            elif self.snake.direction == 'down':
                if self.snake.xcor() <= -300 + 10:
                    can_turn[2] = 0
                if self.snake.xcor() <= -240 + 10:
                    can_turn[1] = 0
                if self.snake.xcor() >= 280 - 10:
                    can_turn[0] = 0

        return can_turn

    def calc_optimal(self):
        optimal_dir = [0, 0, 0, 0]

        f_x = self.fruit.xcor()
        f_y = self.fruit.ycor()
        s_x = self.snake.xcor()
        s_y = self.snake.ycor()

        if s_x > f_x:
            optimal_dir[0] = 1
        elif s_x < f_x:
            optimal_dir[1] = 1

        if s_y < f_y:
            optimal_dir[2] = 1
        elif s_y > f_y:
            optimal_dir[3] = 1

        return optimal_dir

    def step(self):
        # snake and fruit collisions
        if self.snake.distance(self.fruit) < 20:
            x = random.randint(-290, 270)
            y = random.randint(-240, 240)
            self.fruit.goto(x, y)
            self.scoring.clear()
            self.score += 1
            self.scoring.write("Score: {}  Game number: {}".format(self.score, self.game_number), align="center",
                               font=("Courier", 24, "bold"))
            self.delay -= 0.001

            # creating new_ball
            new_fruit = turtle.Turtle()
            new_fruit.speed(0)
            new_fruit.shape('square')
            new_fruit.color('red')
            new_fruit.penup()
            self.old_fruit.append(new_fruit)

        # adding ball to snake
        for index in range(len(self.old_fruit) - 1, 0, -1):
            a = self.old_fruit[index - 1].xcor()
            b = self.old_fruit[index - 1].ycor()

            self.old_fruit[index].goto(a, b)

            self.old_fruit[index].top = b + 10
            self.old_fruit[index].bottom = b - 10
            self.old_fruit[index].left = a - 10
            self.old_fruit[index].right = a + 10

        if len(self.old_fruit) > 0:
            a = self.snake.xcor()
            b = self.snake.ycor()
            self.old_fruit[0].goto(a, b)

            self.old_fruit[0].top = b + 10
            self.old_fruit[0].bottom = b - 10
            self.old_fruit[0].left = a - 10
            self.old_fruit[0].right = a + 10
        self.snake_move()

        # snake and border collision
        if self.snake.xcor() > 280 or self.snake.xcor() < -300 or self.snake.ycor() > 240 or self.snake.ycor() < -240:
            time.sleep(1)
            self.screen.clear()
            self.screen.bgcolor('white')
            self.scoring.goto(0, 0)
            self.scoring.write("   GAME OVER \n Your Score is {}".format(self.score), align="center",
                               font=("Courier", 30, "bold"))
            self.is_done = True
            return False

        # snake collision
        for food in self.old_fruit:
            if food.distance(self.snake) < 20:
                time.sleep(1)
                self.screen.clear()
                self.screen.bgcolor('white')
                self.scoring.goto(0, 0)
                self.scoring.write("    GAME OVER \n Your Score is {}".format(self.score), align="center",
                                   font=("Courier", 30, "bold"))
                self.is_done = True
                return False

        time.sleep(self.delay)
        self.screen.update()
        return True

    def close_game(self):
        self.screen.clear()
        turtle.Terminator()


if __name__ == "__main__":
    snake = SnakeGame()

    while True:
        if not snake.step():
            snake.close_game()
            break
