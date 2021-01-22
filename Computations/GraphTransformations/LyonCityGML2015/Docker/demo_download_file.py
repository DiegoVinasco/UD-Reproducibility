import os
import sys
import logging
import requests

class DemoDownloadFile:
    """
    A utility class for downloading a citygml file.
    """
    def __init__(self, output_dir = None, filename = None):
        self.output_dir = output_dir
        self.filename = filename
        self.create_output_dir()

    def set_output_dir(self, output_dir):
        self.output_dir = output_dir
        self.create_output_dir()

    def set_filename(self, filename):
        self.filename = filename

    def create_output_dir(self):
        output_dir = self.output_dir
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

    def download_file(self, url):
        self.assert_ready_for_run()
        request = requests.get(url)
        logging.info(f'http download status code: {request.status_code}')
        with open(f'{self.output_dir}/{self.filename}', 'wb') as file:
            file.write(request.content)

    def assert_ready_for_run(self):
        if self.output_dir is None:
            logging.error(f'No output_dir set. Exiting.')
            sys.exit(1)
        if self.filename is None:
            logging.error(f'No filename set. Exiting.')
            sys.exit(1)
