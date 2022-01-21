import os


class DataRecorder:
    DATA_PATH = 'data/'
    FILES = {
        "training_data": {
            "index": 0,
            "filename": 'training_data.csv'
        }
    }

    def __init__(self):

        # check if data folder exists
        if not os.path.exists(self.DATA_PATH):
            os.mkdir(self.DATA_PATH)

        self.init_files()

    def init_files(self):

        for file in self.FILES:
            meta_data = self.FILES.get(file)

            # create path to files
            file_path = os.path.join(self.DATA_PATH, meta_data['filename'])
            self.FILES[file]['filepath'] = file_path

            # create the file if it does not exist
            if not os.path.exists(file_path):
                training_file = open(file_path, "x")
                training_file.close()

    def test_file(self, file):
        try:
            file_path = self.FILES[file]['filepath']
            return file_path
        except Exception as e:
            print('Cannot read file: ' + e)
            return None

    def record_data(self, file, data):
        file_path = self.test_file(file)
        if not file_path:
            return False

        new_data = ""
        if isinstance(data, list):
            for index, item in enumerate(data):
                if index == len(data) - 1:
                    new_data += str(item) + "\n"
                else:
                    new_data += str(item) + ","
        else:
            new_data = data

        file = open(file_path, "a")
        file.write(new_data)
        file.close()

        return True

    def read_data(self, file):
        file_path = self.test_file(file)
        if not file_path:
            return False

        training_file = open(file_path, "r")
        file_data = []
        for line in training_file:
            vals = line.split(",")
            new_line = []
            for val in vals:
                if '\n' in val:
                    val = val[0]
                new_line.append(val)
            file_data.append(new_line)

        training_file.close()
        return file_data


if __name__ == "__main__":
    record = DataRecorder()
