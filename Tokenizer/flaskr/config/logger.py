import logging
import os
import sys


def setup_logger() -> None:
    log_directory = 'logs'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_file_path = os.path.join(log_directory, 'tokenizer.log')
    logging.basicConfig(filename=log_file_path, level=logging.INFO, encoding='utf-8',
                        format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
