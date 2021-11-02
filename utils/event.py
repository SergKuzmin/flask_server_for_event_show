import datetime
import random


class Event:
    @staticmethod
    def random_generate():
        date = datetime.datetime.now()
        return {'timestamp': date,
                'camera_name': f'camera_{random.randint(0, 3)}',
                'open_date': date,
                'close_date': date,
                'num_in': random.randint(0, 10),
                'num_out': random.randint(0, 10)}

    @staticmethod
    def serializer(data: dict) -> dict:
        result = {}
        for key in data.keys():
            if key in ['num_in', 'num_out']:
                result[key] = int(data[key])
            else:
                result[key] = data[key]
        return result
