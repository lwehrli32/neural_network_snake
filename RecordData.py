import os


class DataRecorder:
    DATA_PATH = 'data/'
    FILES = {
        "training_data": {
            "index": 0,
            "filename": 'training_data.csv'
        },
        "move_data": {
            "index": 1,
            "filename": 'move_data.csv'
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

    def record_data(self, file, data):
        try:
            file_path = self.FILES[file]['filepath']
        except Exception as e:
            print(e)
            return False

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

if __name__ == "__main__":
    record = DataRecorder()
