import os


class DataRecorder:
    DATA_PATH = 'data/'
    TRAINING_DATA_FILE = 'training_data.csv'

    def __int__(self):

        # check if data folder exists
        if not os.path.exists(self.DATA_PATH):
            os.mkdir(self.DATA_PATH)

        # create path to training file
        self.training_data_file_path = os.path.join(self.DATA_PATH, self.TRAINING_DATA_FILE)

        # create the file if it does not exist
        if not os.path.exists(self.training_data_file_path):
            training_file = open(self.training_data_file_path, "x")
            training_file.close()

    def record_training_data(self, data):
        training_file = open(self.training_data_file_path, "a")

        # write data to file
        training_file.write(data)

        training_file.close()
