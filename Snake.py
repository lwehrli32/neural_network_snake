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
        self.new_fruit = None

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
            self.snake.direction = "up"

    def snake_go_down(self):
        if self.snake.direction != "up":
            self.snake.direction = "down"

    def snake_go_left(self):
        if self.snake.direction != "right":
            self.snake.direction = "left"

    def snake_go_right(self):
        if self.snake.direction != "left":
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

    def is_overlapping(self, direction, fruit):
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

        if direction == 0:
            if f_left <= s_left - 20 < f_right and s_top == f_top:
                return True
        elif direction == 1:
            if f_right >= s_right + 20 > f_left and s_top == f_top:
                return True
        elif direction == 2:
            if f_top >= s_top + 20 > f_bottom and s_right == f_right:
                return True
        elif direction == 3:
            if f_bottom <= s_bottom - 20 < f_top and s_right == f_right:
                return True

        return False

    def find_obs(self):
        can_turn = [1, 1, 1, 1]

        if len(self.old_fruit) > 0:

            # find if you can turn that direction
            for i, fruit in enumerate(self.old_fruit):
                for index, dir in enumerate(can_turn):
                    if index == 0:
                        if self.snake.direction == 'right':
                            can_turn[index] = 0
                        elif self.is_overlapping(index, fruit):
                            can_turn[index] = 0
                        elif self.snake.xcor() <= -300 + 10:
                            can_turn[index] = 0
                    elif index == 1:
                        if self.snake.direction == 'left':
                            can_turn[index] = 0
                        elif self.is_overlapping(index, fruit):
                            can_turn[index] = 0
                        elif self.snake.xcor() >= 280 - 10:
                            can_turn[index] = 0
                    elif index == 2:
                        if self.snake.direction == 'down':
                            can_turn[index] = 0
                        elif self.is_overlapping(index, fruit):
                            can_turn[index] = 0
                        elif self.snake.xcor() >= 240 - 10:
                            can_turn[index] = 0
                    elif index == 3:
                        if self.snake.direction == 'up':
                            can_turn[index] = 0
                        elif self.is_overlapping(index, fruit):
                            can_turn[index] = 0
                        elif self.snake.xcor() <= -240 + 10:
                            can_turn[index] = 0
        else:
            if self.snake.direction == 'right':
                can_turn[0] = 0
            if self.snake.direction == 'left':
                can_turn[1] = 0
            if self.snake.direction == 'up':
                can_turn[3] = 0
            if self.snake.direction == 'down':
                can_turn[2] = 0

        return can_turn

    def calc_optimal(self, new_fruit):
        optimal_dir = [0, 0, 0, 0]

        f_x = new_fruit.xcor()
        f_y = new_fruit.ycor()
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
            self.new_fruit = turtle.Turtle()
            self.new_fruit.speed(0)
            self.new_fruit.shape('square')
            self.new_fruit.color('red')
            self.new_fruit.penup()
            self.old_fruit.append(self.new_fruit)

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
