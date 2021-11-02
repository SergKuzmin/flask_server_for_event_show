import time
import requests
import random
import datetime
import logging

logging.basicConfig(level=logging.INFO)
POST_ROW_URL = 'http://127.0.0.1:5000/add_event'


def run(post_url: str):
    while True:
        time.sleep(random.randint(1, 5))
        date = datetime.datetime.now().isoformat()
        result = {'timestamp': date,
                  'camera_name': f'camera_{random.randint(0, 3)}',
                  'open_date': date,
                  'close_date': date,
                  'num_in': random.randint(0, 10),
                  'num_out': random.randint(0, 10)}
        try:
            requests.post(post_url, data=result)
            logging.info('success')
        except requests.exceptions.ConnectionError:
            logging.error('run server')


if __name__ == '__main__':
    run(post_url=POST_ROW_URL)
