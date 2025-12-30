import json


class TaskGenerator:
    def __init__(self, json_file_path='../data/dataset_1.json'):
        with open(json_file_path, 'r') as file:
            self.tasks = json.load(file)
        self.current_index = 0

    def generate_task(self):
        if self.current_index < len(self.tasks):
            task = self.tasks[self.current_index]
            self.current_index += 1
            return task
        return None

    def __len__(self):
        return len(self.tasks)