from Snake import SnakeGame
from RecordData import DataRecorder


class NeuralNetwork:

    def __init__(self, num_games=3):
        self.num_games = num_games
        self.data_recorder = DataRecorder()

    def init(self):
        training_data = []

        for i in range(self.num_games):
            game = SnakeGame()

            loop = True

            while loop:
                break

    def record_training_data(self, data):
        self.data_recorder.record_training_data(data)

if __name__ == "__main__":
    pass
