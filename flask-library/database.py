import json


class Database:
    def __init__(self, filepath):
        self.filepath = filepath

    def _is_json_format(self):
        with open(self.filepath, mode='r') as f:
            try:
                json.loads(f.read())
                return True
            except json.JSONDecodeError:
                return False

    def read(self):
        with open(self.filepath, mode='r') as f:
            data = json.loads(f.read())
        return data

    def write(self, data):
        data = json.dumps(data, indent=4, sort_keys=True)
        with open(self.filepath, mode='w') as f:
            f.write(data)


if __name__ == '__main__':
    db = Database('database.json')
    print(db._is_json_format())
