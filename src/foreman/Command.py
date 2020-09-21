import subprocess
import os
import glob
from pathlib import Path
from .services.Configuration import Configuration


class Command:

    def startup(self):
        for directory in self.get_registered_directories():
            site = directory.split('/')[-2]
            activation_environment = self.find_virtual_environment_activation_file(directory)

            if activation_environment is None:
                self.line(f"<error>No virtual environment detected, not starting site {site}.</error>")
                self.line("<error>Please register your venv by running:</error>")
                self.line("<fg=magenta;options=bold>    foreman register /path/to/venv</>")
            else:
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
        for location in Configuration().get('venv_locations'):
            if "/" in location:
                project = os.path.basename(directory)
                venv = os.path.join(location, project, 'bin/activate')
            else:
                venv = os.path.join(directory, location, 'bin/activate')
            if os.path.exists(venv):
                return venv
        return None
