import os
import sys
import logging
from docker_helper import DockerHelperBuild, DockerHelperTask


class DockerShapechange(DockerHelperBuild, DockerHelperTask):

    def __init__(self):
        super().__init__('liris', 'shapechange')
        this_file_dir = os.path.dirname(os.path.realpath(__file__))
        context_dir = os.path.join(this_file_dir,
                                   'ShapeChange-DockerContext')
        self.build(context_dir)

        self.input_filename = None

    def assert_ready_for_run(self):
        if not self.input_filename:
            logging.info('Missing input_filename for running. Exiting')
            sys.exit(1)

    def set_input_filename(self, input_filename):
        full_input_filename = os.path.join(self.mounted_input_dir,
                                           input_filename)
        if not os.path.isfile(full_input_filename):
            logging.info('Input file ' + full_input_filename + ' not found. Exiting')
            sys.exit(1)
        self.input_filename = input_filename

    def get_command(self):
        self.assert_ready_for_run()
        # We don't need to specify the executable since an entrypoint
        # is specified in the DockerFile of DockerStripAttributes
        command = '/data-io/' + self.input_filename

        return command

    def run(self):
        # Set input and output volumes
        self.add_volume(self.mounted_input_dir, '/data-io', 'rw')
        super().run()

    @staticmethod
    def strip_single_file(input_dir,
                          input_filename):

        # Docker only accepts absolute path names as argument for its volumes
        # to be mounted:
        absolute_path_input_dir = os.path.join(os.getcwd(), input_dir)
        container = DockerShapechange()
        container.set_mounted_input_directory(absolute_path_input_dir)
        container.set_input_filename(input_filename)
        container.run()

        output_dir = input_dir
        # TODO: update naming conventions
        full_output_filename = os.path.join(output_dir, 'output/FLATTENER1')
        # logging.info(f'Striping to yield file {full_output_filename}.')
        if not os.path.isdir(full_output_filename):
            logging.error(
                'Output file ' + full_output_filename + ' not found. Exiting.')
            sys.exit(1)

if __name__ == "__main__":
    log_filename = os.path.join(os.getcwd(), 'demo_full_workflow.log')

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=log_filename,
                        filemode='w')

    DockerShapechange.strip_single_file('data-io', 'input/CityGML2.0_config.xml')
    