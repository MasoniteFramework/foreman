import glob
import os
import subprocess
from pathlib import Path

from cleo import Command as CLICommand
from ..drivers.MasoniteDriver import MasoniteDriver
from ..drivers.DjangoDriver import DjangoDriver
from ..services.Configuration import Configuration

class StartCommand(CLICommand):
    """
    Starts all the dev sites in the registered directories

    start
        {directory? : The directory you want to start}
    """

    drivers = {
        'masonite': MasoniteDriver,
        'django': DjangoDriver
    }

    def handle(self):
        # Configuration().config()
        if self.argument('directory') and self.argument('directory') == '.':
            site = os.getcwd().split('/')[-1]
            self.start_directory(os.getcwd(), site)
            return
        else:
            self.info('Ensuring All Applications Are Started ..')
            configuration = Configuration()
            for directory in self.get_registered_directories():
                site = directory.split('/')[-2]
                self.start_directory(directory, site)

    def get_home_path(self):
        return str(Path.home())

    def start_directory(self, directory, site):
        configuration = Configuration()
        self.info(f"Starting {site}..")
        venv_config = configuration.get('venvs')
        tld = configuration.get('tld')
        socket_directory = configuration.get('socket_directory')
        if site in venv_config:
            activation_environment = os.path.join(venv_config[site], 'bin/activate')
        else:
            activation_environment = self.find_virtual_environment_activation_file(directory, site)

        driver = self.make(directory)
        command = f"cd {directory}"
        command += f" && source {activation_environment}"
        socket_path = os.path.join(socket_directory, site)
        command += f" && pip install uwsgi && set -m; nohup uwsgi --socket {socket_path}.{tld}.sock --wsgi-file {driver.wsgi_path(directory)} --py-autoreload=1 &> /dev/null &"
        subprocess.run(command, shell=True, close_fds=True,
                        env={'PYTHONPATH': f'{directory}'})

    def get_registered_directories(self):
        directories = []
        for directory in Configuration().get('directories', []):
            directories += glob.glob(os.path.join(directory, '*/'))
        return directories

    def find_virtual_environment_activation_file(self, directory, site):
        return os.path.join(directory, 'venv/bin/activate')

    def make(self, directory):
        for key, available_driver in self.drivers.items():
            selected_driver = available_driver()
            if selected_driver.detect(directory):
                self.info(f'Using driver: {key.capitalize()}')
                return selected_driver
        
        raise ValueError("Could not detect a driver for this project")
        # return self.drivers[driver]()
