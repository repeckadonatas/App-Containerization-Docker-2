import source.logger as log
import source.get_metals_data as metals
import source.data_preparation as data
import source.db_functions as db

import concurrent.futures
import threading
import time
from queue import Queue

main_logger = log.app_logger(__name__)

"""
Main program file to run the program
using concurrent.futures module.
The programs performance is also timed
and printed out.
"""

start = time.perf_counter()

event = threading.Event()
queue = Queue(maxsize=4)
try:
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        tasks = [executor.map(metals.download_metals_data), 
                 executor.submit(data.prepare_json_data(queue, event)), 
                 executor.submit(db.metals_price_data_upload_to_db(queue, event))]

    concurrent.futures.wait(tasks)
except Exception as e:
    main_logger.error('Exception occurred while running "main.py": {}\n'.format(e))

end = time.perf_counter()
main_logger.info('Process completed in {} seconds\n'.format(end-start))
