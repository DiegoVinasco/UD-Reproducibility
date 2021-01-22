import os
import sys
import logging
from docker_helper import DockerHelperTask


class DockerShapechange(DockerHelperTask):

    def __init__(self):
        super().__init__('liris/ud-graph', 'latest')
        # this_file_dir = os.path.dirname(os.path.realpath(__file__))
        # context_dir = os.path.join(this_file_dir,
                                #    'ShapeChange-DockerContext')
        # self.build(context_dir)

        self.local_input_dir = '/UD-Graph/Transformations/input/'
        self.local_output_dir = '/UD-Graph/Transformations/output/'
        self.configuration_filename = None
        self.input_filename = None
        self.output_directory = None

    def assert_ready_for_run(self):
        if not self.configuration_filename:
            logging.error('Missing configuration_filename for running. Exiting')
            sys.exit(1)
        if not self.input_filename:
            logging.error('Missing input_filename for running. Exiting')
            sys.exit(1)
        if not self.output_directory:
            logging.error('Missing output_directory for running. Exiting')
            sys.exit(1)

    def set_configuration_filename(self, configuration_filename):
        full_configuration_filename = os.path.join(self.mounted_input_dir,
                                                   configuration_filename)
        if not os.path.isfile(full_configuration_filename):
            logging.error(f'Configuration file {full_configuration_filename} not found. Exiting')
            sys.exit(1)
        self.configuration_filename = f'{self.local_input_dir}/{configuration_filename}'

    def set_input_filename(self, input_filename):
        full_input_filename = os.path.join(self.mounted_input_dir,
                                           input_filename)
        if not os.path.isfile(full_input_filename):
            logging.error(f'Input file {full_input_filename} not found. Exiting')
            sys.exit(1)
        self.input_filename = f'{self.local_input_dir}/{input_filename}'

    def set_output_directory(self, output_directory):
        self.output_directory = f'{self.local_output_dir}/{output_directory}'

    def get_command(self):
        self.assert_ready_for_run()
        # We don't need to specify the executable since an entrypoint
        # is specified in the DockerFile
        command = f'uml2owl --config {self.configuration_filename} '
        command +=        f'--input {self.input_filename} '
        command +=        f'--output {self.output_directory} '
        # logging.info(f'command: {command}')
        return command

    def run(self):
        # Set input and output volumes
        self.add_volume(self.mounted_input_dir, self.local_input_dir, 'rw')
        self.add_volume(self.mounted_output_dir, self.local_output_dir, 'rw')
        super().run()

    @staticmethod
    def transform_single_file(input_dir,
                              output_dir,
                              input_filename,
                              output_directory,
                              configuration_filename):

        # Docker only accepts absolute path names as argument for its volumes
        # to be mounted:
        absolute_path_input_dir = os.path.join(os.getcwd(), input_dir)
        absolute_path_output_dir = os.path.join(os.getcwd(), output_dir)
        container = DockerShapechange()
        container.set_mounted_input_directory(absolute_path_input_dir)
        container.set_mounted_output_directory(absolute_path_output_dir)
        container.set_configuration_filename(configuration_filename)
        container.set_input_filename(input_filename)
        container.set_output_directory(output_directory)
        container.run()

        full_output_directory = os.path.join(os.getcwd(), output_dir)
        if not os.path.isdir(full_output_directory):
            logging.error(
                'Output directory {full_output_directory} not found. Exiting.')
            sys.exit(1)
