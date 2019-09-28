import glob
import os
import subprocess
from pathlib import Path

from cleo import Command as CLICommand
from ..drivers.MasoniteDriver import MasoniteDriver
from ..services.Configuration import Configuration

class KillCommand(CLICommand):
    """
    Kills serving applications

    kill
        {app? : The application name you want to kill}
    """

    def handle(self):
        if self.argument('app'):
            self.kill(self.argument('app'))
        else:
            for directory in self.get_registered_directories():
                app = directory.split('/')[-2]
                self.kill(app)
    
    def kill(self, app):
        self.info(f"Killing app: {app}")

        configuration = Configuration()
        tld = configuration.get('tld')
        socket_directory = configuration.get('socket_directory')
        subprocess.run(f"rm {os.path.join(socket_directory, app)}.{tld}.sock", shell=True)
        self.info("App stopped")  

    def get_registered_directories(self):
        directories = []
        for directory in Configuration().get('directories', []):
            directories += glob.glob(os.path.join(directory, '*/'))
        return directories