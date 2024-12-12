from datetime import datetime

import mappings


def log_writer(message):
    log_file_name = "log_" + datetime.now().strftime('%Y_%m_%d') + ".log"
    log_path = mappings.paths("file_server_local") + log_file_name

    with open(log_path, 'a', encoding='utf-8') as log_file:
        log_file.write(message + "\n")
