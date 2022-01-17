import random as rnd
from pandas import read_csv
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

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

    def init_data(self):
        for i in range(self.num_games):
            print("Starting game " + str(i + 1) + " of " + str(self.num_games) + ".")
            game = SnakeGame(user=self.user, game_number=i)
            loop = True

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
                            game.snake.direction == 'right'
                    elif action == 1:
                        if snake_dir == 'right':
                            game.snake.direction = 'down'
                        elif snake_dir == 'left':
                            game.snake.direction = 'up'
                        elif snake_dir == 'up':
                            game.snake.direction = 'right'
                        elif snake_dir == 'down':
                            game.snake.direction == 'left'
                else:
                    action = game.action

                self.record_snake_obs(game, action)
                game.set_action(game.snake.direction)
                loop = game.step()

            self.record_snake_obs(game, action)
            game.close_game()

        print("Getting all training data done. All " + str(self.num_games) + " games finished")

    def generate_snake_action(self):
        action = rnd.randint(0, 2) - 1
        return action

    def record_snake_obs(self, game, action):
        obs = self.get_snake_observations(game, action)
        self.record_data(obs)

    def get_snake_observations(self, game, action):
        obs = game.find_obs()
        obs.append(action)

        if game.is_done:
            obs.append(0)
        else:
            obs.append(1)

        return obs

    def load_dataset(self, file):

        print("Training data...")

        file_meta_data = self.data_recorder.FILES.get(file)
        file_path = file_meta_data.get('filepath')

        names = ['left', 'right', 'up', 'down', 'direction']
        dataset = read_csv(file_path, names=names)
        array = dataset.values
        x = array[:, 0:4]
        y = array[:, 4]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=1)
        x_train = self.sc.fit_transform(x_train)
        #x_test = self.sc.transform(x_test)

        self.mlpc.fit(x_train, y_train)

    def run_nn(self, obs):
        xnew = []
        xnew.append(obs)
        xnew = self.sc.transform(xnew)
        pred = self.mlpc.predict(xnew)
        return pred[0]

    def snake_wtih_nn(self):
        print("Starting game with neural network. . .")
        game = SnakeGame(user=False)

        loop = True
        while loop:
            obs = self.get_snake_observations(game)
            new_snake_direction = self.run_nn(obs)
            snake_dir = game.snake.direction

            if new_snake_direction == 'left' and snake_dir != "right":
                game.snake.direction = 'left'
            elif new_snake_direction == 'right' and snake_dir != 'left':
                game.snake.direction = 'right'
            elif new_snake_direction == 'up' and snake_dir != 'down':
                game.snake.direction = 'up'
            elif new_snake_direction == 'down' and snake_dir != 'up':
                game.snake.direction = 'down'

            loop = game.step()

    def record_data(self, data):
        self.data_recorder.record_data('training_data', data)


def main():
    print("Loading. . .")
    snakeNN = NeuralNetwork(num_games=1, user=True)
    snakeNN.init_data()
    #snakeNN.load_dataset('training_data')
    #snakeNN.snake_wtih_nn()

if __name__ == "__main__":
    main()
