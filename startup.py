#!/usr/bin/env python
# import subprocess, os, glob
# from pathlib import Path
# home = str(Path.home())

import glob
import os
import subprocess
from pathlib import Path

from cleo import Application
from cleo import Command as CLICommand

from src.foreman.services.Command import Command


class StartCommand(CLICommand):
    """
    Starts all the dev sites in the registered directories

    start
    """

    drivers = {
        'masonite'
    }

    def handle(self):
        for directory in self.get_registered_directories():
            site = directory.split('/')[-2]
            activation_environment = self.find_virtual_environment_activation_file(
                directory)
            # print(activation_environment)
            # return

            command = f"cd {directory}"
            command += f" && source {activation_environment}"
            command += f" && pip install uwsgi && set -m; nohup uwsgi --socket /tmp/{site}.test.sock --wsgi-file wsgi.py &> /dev/null &"
            subprocess.run(command, shell=True, close_fds=True,
                           env={'PYTHONPATH': f'{directory}'})

    def get_home_path(self):
        return str(Path.home())

    def get_registered_directories(self):
        return glob.glob(os.path.join(self.get_home_path(), 'sites/*/'))

    def find_virtual_environment_activation_file(self, directory):
        return f"{directory}venv/bin/activate"

    def make(self, driver):
        return self.drivers[driver]

application = Application(name="Masonite Foreman")
application.add(StartCommand())

if __name__ == '__main__':
    application.run()

# folders = glob.glob(os.path.join(home, 'sites/*/'))

# for folder in folders:

#     folder = folder.split('/')[-2]
#     # print(folder)
#     # continue
#     activate_environment = f"source ~/sites/{folder}/venv/bin/activate"

#     command = f"cd ~/sites/{folder}"
#     command += f" && source venv/bin/activate"
#     command += f" && pip install uwsgi && set -m; nohup uwsgi --socket /tmp/{folder}.test.sock --wsgi-file wsgi.py &> /dev/null &"
#     subprocess.run(command, shell=True, close_fds=True,
#                 env={'PYTHONPATH': f'~/sites/{folder}/venv/lib/python3.6/site-packages'})
