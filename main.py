"""
Main file to run the program using 
Python's concurrent.futures module.
The programs performance is also timed
and printed out.
"""

import time
import threading
import concurrent.futures
from queue import Queue

import source.logger as log
import source.get_metals_data as metals
import source.data_preparation as data
import source.db_functions as db
import source.ml_model as mlm

main_logger = log.app_logger(__name__)


start = time.perf_counter()

event = threading.Event()
queue = Queue(maxsize=4)
try:
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        tasks = [executor.submit(metals.download_metals_data()), 
                 executor.submit(data.prepare_json_data(queue, event)), 
                 executor.submit(db.metals_price_data_upload_to_db(queue, event))]
        
        training_models = executor.submit(mlm.train_price_prediction_models())

    concurrent.futures.wait(tasks)
except Exception as e:
    main_logger.error('Exception occurred while running "main.py": {}\n'.format(e))

end = time.perf_counter()
main_logger.info('Process completed in {} seconds\n'.format(end-start))
