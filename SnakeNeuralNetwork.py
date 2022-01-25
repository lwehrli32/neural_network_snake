import random as rnd
import numpy as np
import math
import tflearn as tf

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression

from Snake import SnakeGame
from RecordData import DataRecorder


class NeuralNetwork:

    def __init__(self, num_games=10, user=False):
        print("Creating game. . .")
        self.num_games = num_games
        self.data_recorder = DataRecorder()
        self.user = user
        self.sc = StandardScaler()
        self.mlpc = MLPClassifier(hidden_layer_sizes=2, max_iter=500)
        self.filename = "snakeio_data.tflearn"
        self.prev_food_distance = 0
        self.learning_rate = 1e-2

    def init_data(self):
        for i in range(self.num_games):
            print("Starting game " + str(i + 1) + " of " + str(self.num_games) + ".")
            game = SnakeGame(user=self.user, game_number=i)
            loop = True

            self.prev_food_distance = self.calc_food_distance(game)

            while loop:
                if not self.user:
                    action = self.generate_snake_action()
                    snake_dir = game.snake.direction

                    if action == -1:
                        if snake_dir == 'right':
                            game.snake.direction = 'up'
                        elif snake_dir == 'left':
                            game.snake.direction = 'down'
                        elif snake_dir == 'up':
                            game.snake.direction = 'left'
                        elif snake_dir == 'down':
                            game.snake.direction = 'right'
                    elif action == 1:
                        if snake_dir == 'right':
                            game.snake.direction = 'down'
                        elif snake_dir == 'left':
                            game.snake.direction = 'up'
                        elif snake_dir == 'up':
                            game.snake.direction = 'right'
                        elif snake_dir == 'down':
                            game.snake.direction = 'left'
                else:
                    action = game.action

                loop = game.step()
                self.record_snake_obs(game, action)
                game.set_action(game.snake.direction)

            game.close_game()

        print("Getting all training data done. All " + str(self.num_games) + " games finished")

    def generate_snake_action(self):
        action = rnd.randint(0, 2) - 1
        return action

    def record_snake_obs(self, game, action):
        obs = self.get_snake_observations(game, action)
        self.record_data(obs)

    def calc_food_distance(self, game):
        snake = game.snake
        food = game.fruit
        snake_x = snake.xcor()
        snake_y = snake.ycor()
        food_x = food.xcor()
        food_y = food.ycor()

        x_diff = snake_x - food_x
        y_diff = snake_y - food_y

        x_squared = x_diff ** 2
        y_squared = y_diff ** 2

        total = x_squared + y_squared

        distance = math.sqrt(total)

        return distance

    def get_snake_observations(self, game, action, is_init=True):
        obs = game.find_obs()

        if is_init:
            obs.append(action)

            distance = self.calc_food_distance(game)
            if game.score > game.prev_score or distance < self.prev_food_distance:
                game.prev_score = game.score
                obs.append(1)
            else:
                obs.append(0)
            self.prev_food_distance = distance

            s_v = self.create_snake_vector(game)
            f_v = self.create_food_vector(game)
            obs.append(self.get_angle(s_v, f_v))

            if game.is_done:
                obs.append(0)
            else:
                obs.append(1)

        return obs

    def get_angle(self, v1, v2):
        v1 = v1 / np.linalg.norm(v1)
        v2 = v2 / np.linalg.norm(v2)

        return math.atan2(v1[0] * v2[1] - v1[1] * v2[0], v1[0] * v2[0] + v1[1] * v2[1]) / math.pi

    def create_model(self):
        print("Creating model data...")
        network = input_data(shape=[None, 6, 1], name='input')
        network = fully_connected(network, 25, activation='relu')
        network = fully_connected(network, 1, activation='linear')
        network = regression(network, optimizer='adam', learning_rate=self.learning_rate, loss='mean_square',
                             name='target')
        model = tf.DNN(network, tensorboard_dir='log')
        return model

    def train(self, data, model):
        print("Training data...")
        X = np.array([i[0:len(i) - 1] for i in data]).reshape(-1, 6, 1)
        y = np.array([i[len(i) - 1] for i in data]).reshape(-1, 1)
        model.fit(X, y, n_epoch=3, shuffle=True, run_id=self.filename)
        model.save(self.filename)
        return model

    def create_food_vector(self, game):
        snake = game.snake
        food = game.fruit
        return np.array([food.xcor(), food.ycor()]) - np.array([snake.xcor(), snake.ycor()])

    def create_snake_vector(self, game):
        snake = game.snake
        if len(game.old_fruit) > 0:
            snake_body = game.old_fruit[0]
            return np.array([snake.xcor(), snake.ycor()]) - np.array([snake_body.xcor(), snake_body.ycor()])
        else:
            return np.array([snake.xcor(), snake.ycor()])

    def snake_wtih_nn(self):
        print("Starting game with neural network. . .")

        for i in range(self.num_games):
            print("Starting game " + str(i + 1) + " of " + str(self.num_games) + ".")
            print("Training model. . .")
            model = self.train_data()

            game = SnakeGame(user=False)

            self.prev_food_distance = self.calc_food_distance(game)

            loop = True
            while loop:
                obs = self.get_snake_observations(game, None, is_init=False)

                distance = self.calc_food_distance(game)
                if game.score > game.prev_score or distance < self.prev_food_distance:
                    game.prev_score = game.score
                    obs.append(1)
                else:
                    obs.append(0)
                self.prev_food_distance = distance

                preds = []
                for new_action in range(-1, 2):
                    new_obs = [i for i in obs]
                    new_obs.append(new_action)
                    preds.append(model.predict(np.array(new_obs).reshape(-1, 6, 1)))

                new_snake_direction = np.argmax(np.array(preds)) - 1
                snake_dir = game.snake.direction

                if new_snake_direction == -1:
                    if snake_dir == 'left':
                        game.snake.direction = 'down'
                    elif snake_dir == 'right':
                        game.snake.direction = 'up'
                    elif snake_dir == 'up':
                        game.snake.direction = 'left'
                    elif snake_dir == 'down':
                        game.snake.direction = 'right'
                elif new_snake_direction == 1:
                    if snake_dir == 'left':
                        game.snake.direction = 'up'
                    elif snake_dir == 'right':
                        game.snake.direction = 'down'
                    elif snake_dir == 'up':
                        game.snake.direction = 'right'
                    elif snake_dir == 'down':
                        game.snake.direction = 'left'

                loop = game.step()
                #self.record_snake_obs(game, new_snake_direction)

            game.close_game()

    def record_data(self, data):
        self.data_recorder.record_data('training_data', data)

    def read_data(self):
        return self.data_recorder.read_data('training_data')

    def train_data(self):
        training_data = self.read_data()

        model = self.create_model()
        model = self.train(training_data, model)
        return model


def main():
    print("Loading. . .")
    snakeNN = NeuralNetwork(num_games=50, user=False)
    snakeNN.init_data()
    snakeNN.snake_wtih_nn()
    # snakeNN.load_dataset('training_data')
    # snakeNN.snake_wtih_nn()


if __name__ == "__main__":
    main()
