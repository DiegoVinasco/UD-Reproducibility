import os
import sys
import docker
import logging
from abc import ABC, abstractmethod


class DockerHelper(ABC):

    def __init__(self, context_dir, tag_name):
        self.context_dir = context_dir
        self.tag_name = tag_name
        self.client = None     # The name for the docker client (read server)
        self.mounted_input_dir = None
        self.mounted_output_dir = None
        # Some containers (like 3DUse) provide multiple commands each of
        # which might require its proper working directory (i.e. the WORKDIR
        # variable of the Dockerfile)
        self.working_dir = '.'

        self.assert_server_is_active()
        self.build()

    def assert_server_is_active(self):
        """
        Assert that a docker server is up and available
        :return: None, sys.exit() on failure
        """
        self.client = docker.from_env()
        try:
            self.client.ping()
        except (requests.exceptions.ConnectionError, docker.errors.APIError):
            logging.error('Unable to connect to a docker server:')
            logging.error('   is a docker server running this host ?')
            sys.exit(1)

        # Assert that the context directory exists
        if not os.path.exists(self.context_dir):
            logging.error(f'Unfound context directory: {self.context_dir} ')
            sys.exit(1)

    def build(self):
        """
        Provision the docker image.
        """
        try:
            result = self.client.images.build(
                path=self.context_dir,
                tag=self.tag_name)
            logging.info(f'Docker building image: {self.tag_name}')
            for line in result:
                logging.info(f'    {line}')
            logging.info(f'Docker building image done.')
        except docker.errors.APIError as err:
            logging.error('Unable to build the docker image: with error')
            logging.error(f'   {err}')
            sys.exit(1)
        except TypeError:
            logging.error('Building the docker image requires path or fileobj.')
            sys.exit(1)

    def set_mounted_input_directory(self, directory):
        if not os.path.isdir(directory):
            logging.info(f'Input dir to mount {directory} not found. Exiting')
            sys.exit(1)
        self.mounted_input_dir = directory

    def set_mounted_output_directory(self, directory):
        if not os.path.isdir(directory):
            logging.info(f'Output dir to mount {directory} not found. Exiting')
            sys.exit(1)
        self.mounted_output_dir = directory

    @abstractmethod
    def get_command(self):
        print("WTF")

    def run(self):
        volumes = {self.mounted_input_dir: {'bind': '/Input', 'mode': 'rw'}}
        if not self.mounted_input_dir == self.mounted_output_dir:
            # When mounting the same directory twice (which is the case when
            # the input and output directory are the same) then containers.run()
            # raises a docker.errors.ContainerError. Hence we only mount the
            # /Output volume when they both differ. Note that when this
            # happens the command in the derived class must be altered in order
            # to place its output in the /Input mounted point (because in this
            # /Output is (equal to) /Input.
            volumes[self.mounted_output_dir] = {'bind': '/Output', 'mode': 'rw'}
        self.client.containers.run(
            self.tag_name,
            # command=["/bin/sh", "-c", "ls > ls_results"],
            command=["/bin/sh", "-c", self.get_command()],
            #volumes={self.mounted_input_dir: {'bind': '/Input', 'mode': 'rw'},
            #         self.mounted_output_dir: {'bind': '/Output', 'mode': 'rw'}
            #         },
            volumes=volumes,
            working_dir=self.working_dir,
            stdin_open=True,
            stderr=True,
            tty=True)


class Docker3DUse(DockerHelper):

    def __init__(self):
        context_dir = os.path.join(os.getcwd(),
                                   '..',
                                   'Docker',
                                   '3DUse-DockerContext')
        tag_name = 'liris:3DUse'
        super().__init__(context_dir, tag_name)


class DockerSplitBuilding(Docker3DUse):

    def __init__(self):
        super().__init__()
        self.working_dir = '/root/3DUSE/Build/src/utils/cmdline/'
        self.input_filename = None
        self.output_filename = None
        self.command_output_directory = None

    def assert_ready_for_run(self):
        if not self.input_filename:

            logging.info('Missing input_filename for running. Exiting')
            sys.exit(1)
        if not self.output_filename:
            logging.info('Missing output_filename for running. Exiting')
            sys.exit(1)

    def set_input_filename(self, input_filename):
        full_input_filename = os.path.join(self.mounted_input_dir,
                                           input_filename)
        if not os.path.isfile(full_input_filename):
            logging.info(f'Input file {full_input_filename} not found. Exiting')
            sys.exit(1)
        self.input_filename = input_filename

    def set_output_filename(self, output_filename):
        self.output_filename = output_filename

    def set_command_output_directory(self, output_directory):
        # This is internal to the container and as seen by the container
        # command (as opposed to the directory mounted from "outside" the
        # container i.e. DockerHelper.mounted_output_dir)
        self.command_output_directory = output_directory

    def get_command(self):
        self.assert_ready_for_run()
        command = 'splitCityGMLBuildings '   # Mind the trailing separator
        command += '--input-file /Input/' + self.input_filename + ' '
        # In order to set the output the syntax of splitCityGMLBuildings
        # separates the directory from the file specifications:
        command += '--output-file ' + self.output_filename + ' '
        if not self.mounted_input_dir == self.mounted_output_dir:
            command += '--output-dir /Output/'
        else:
            command += '--output-dir /Input/'
        if self.command_output_directory:
            command += self.command_output_directory + ' '
        command += ' > DockerCommandOutput.log 2>&1'
        return command


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='docker_helper.log',
                        filemode='w')

    d = DockerSplitBuilding()
    d.set_mounted_input_directory(os.path.join(os.getcwd(),
                                               'junk/LYON_1ER_2009'))
    d.set_input_filename('LYON_1ER_BATI_2009.gml')
    # output_dir = os.path.join(os.getcwd(),'junk_split')
    output_dir = os.path.join(os.getcwd(), 'junk/LYON_1ER_2009')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    d.set_mounted_output_directory(output_dir)
    d.set_output_filename('LYON_1ER_BATI_2009_splited.gml')
    # Not strictly required d.set_command_output_directory('LYON_1ER')
    d.run()
