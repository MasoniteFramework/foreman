import glob
import os
import subprocess
from pathlib import Path

from cleo import Command as CLICommand
from ..drivers.MasoniteDriver import MasoniteDriver
from ..services.Configuration import Configuration

class UnregisterCommand(CLICommand):
    """
    Unregisters the current directory from serving Python applications

    unregister
        {directory? : The directory you want to unregister}
    """

    def handle(self):
        if self.argument('directory'):
            directory = self.argument('directory')
        else:
            directory = os.getcwd()

        configuration = Configuration()

        self.info(f'Removing directory: {directory}')
        configuration.remove('directories', [directory])
        self.info('Directory has been deregistered from serving python applications')

        self.call("start")