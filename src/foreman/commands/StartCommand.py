import glob
import os
import subprocess
from pathlib import Path

from cleo import Command as CLICommand
from ..drivers.MasoniteDriver import MasoniteDriver
from ..services.Configuration import Configuration

class StartCommand(CLICommand):
    """
    Starts all the dev sites in the registered directories

    start
    """

    drivers = {
        'masonite': MasoniteDriver
    }

    def handle(self):
        # Configuration().config()
        self.info('Ensuring All Applications Are Started ..')
        configuration = Configuration()
        for directory in self.get_registered_directories():

            site = directory.split('/')[-2]
            self.info(f"Starting {site}..")
            venv_config = configuration.get('venvs')
            if site in venv_config:
                activation_environment = venv_config[site]
            else:
                activation_environment = self.find_virtual_environment_activation_file(directory, site)
                
            print('activation is', activation_environment)
            continue
            driver = 'masonite'
            # print(activation_environment)
            # return
            command = f"cd {directory}"
            command += f" && source {activation_environment}"
            command += f" && pip install uwsgi && set -m; nohup uwsgi --socket /tmp/{site}.test.sock --wsgi-file {self.make(driver).wsgi_path()} &> /dev/null &"
            subprocess.run(command, shell=True, close_fds=True,
                           env={'PYTHONPATH': f'{directory}'})

    def get_home_path(self):
        return str(Path.home())

    def get_registered_directories(self):
        directories = []
        for directory in Configuration().get('directories', []):
            directories += glob.glob(os.path.join(directory, '*/'))
        return directories

    def find_virtual_environment_activation_file(self, directory, site):
        return os.path.join(directory, 'venv/bin/activate')

    def make(self, driver):
        return self.drivers[driver]()
