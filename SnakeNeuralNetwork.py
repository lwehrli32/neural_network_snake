import random as rnd
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from Snake import SnakeGame
from RecordData import DataRecorder


class NeuralNetwork:

    def __init__(self, num_games=10, user=False):
        self.num_games = num_games
        self.data_recorder = DataRecorder()
        self.user = user

    def init_data(self):
        for i in range(self.num_games):
            print("Starting game " + str(i + 1) + " of " + str(self.num_games) + ".")
            game = SnakeGame(user=self.user, game_number=i)
            loop = True

            while loop:
                if not self.user:
                    new_snake_direction = rnd.randint(0, 3)
                    snake_dir = game.snake.direction

                    if new_snake_direction == 0 and snake_dir != 'right':
                        game.snake.direction = 'left'
                    elif new_snake_direction == 1 and snake_dir != 'left':
                        game.snake.direction = 'right'
                    elif new_snake_direction == 2 and snake_dir != 'down':
                        game.snake.direction = 'up'
                    elif new_snake_direction == 3 and snake_dir != 'up':
                        game.snake.direction = 'down'

                self.record_snake_obs(game)

                loop = game.step()

            self.record_snake_obs(game)
            game.close_game()
        print("All " + str(self.num_games) + " games finished")

    def record_snake_obs(self, game):
        obs = self.get_snake_observations(game)
        self.record_data(obs)

    def get_snake_observations(self, game):
        obs = game.find_obs()

        if game.is_done:
            obs.append(1)
        else:
            obs.append(0)
        return obs

    def load_dataset(self, file):

        file_meta_data = self.data_recorder.FILES.get(file)
        file_path = file_meta_data.get('filepath')

        names = ['left', 'right', 'up', 'down', 'is_done']
        dataset = read_csv(file_path, names=names)
        array = dataset.values
        x = array[:, 0:4]
        y = array[:, 4]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=1)
        sc = StandardScaler()
        x_train = sc.fit_transform(x_train)
        x_test = sc.transform(x_test)

    def record_data(self, data):
        self.data_recorder.record_data('move_data', data)


if __name__ == "__main__":
    snakeNN = NeuralNetwork(num_games=20)
    snakeNN.init_data()
