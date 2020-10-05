import glob
import os
import sys
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
        activation_environment = self.get_activation_environment(site, venv_config, directory)

        if activation_environment is None:
            self.line(f"<error>No virtual environment detected, not starting site {site}.</error>")
            self.line("<error>Please register your venv by running:</error>")
            self.line("<fg=magenta;options=bold>    foreman register /path/to/venv</>")
            return
        driver = self.make(directory)
        if driver is None:
            return
        command = f"cd {directory}"
        if activation_environment:
            command += f" && source {activation_environment}"
        socket_path = os.path.join(socket_directory, site)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "uwsgi"])
        command += f" && set -m; nohup uwsgi --socket {socket_path}.{tld}.sock --wsgi-file {driver.wsgi_path(directory)} --py-autoreload=1 &> /dev/null &"
        subprocess.run(command, shell=True, close_fds=True,
                        env={'PYTHONPATH': f'{directory}'})

    def get_activation_environment(self, site, venv_config, directory):
        if self.in_virtualenv():
            return False
        if site in venv_config:
            return os.path.join(venv_config[site], 'bin/activate')
        return self.find_virtual_environment_activation_file(directory, site)

    def get_registered_directories(self):
        directories = []
        for directory in Configuration().get('directories', []):
            directories += glob.glob(os.path.join(directory, '*/'))
        return directories

    def find_virtual_environment_activation_file(self, directory, site):
        for location in Configuration().get('venv_locations'):
            if "/" in location:
                project = os.path.basename(directory)
                venv = os.path.join(location, project, 'bin/activate')
            else:
                venv = os.path.join(directory, location, 'bin/activate')
            if os.path.exists(venv):
                return venv
        return None

    def make(self, directory):
        for key, available_driver in self.drivers.items():
            selected_driver = available_driver()
            if selected_driver.detect(directory):
                self.info(f'Using driver: {key.capitalize()}')
                return selected_driver

        self.line(f"<error>Could not detect a driver for this project</error>")
        return None

    def in_virtualenv(self):
        return os.getenv('VIRTUAL_ENV') is not None
