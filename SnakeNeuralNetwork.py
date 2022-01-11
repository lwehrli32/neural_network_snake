from Snake import SnakeGame


class NeuralNetwork:

    def __init__(self, num_games=3):
        self.num_games = num_games

    def init(self):
        training_data = []

        for i in range(self.num_games):
            game = SnakeGame()

            loop = True

            while loop:



if __name__ == "__main__":
    pass
