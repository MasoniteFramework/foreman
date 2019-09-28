import glob
import os
import subprocess
from pathlib import Path

from cleo import Command as CLICommand
from ..drivers.MasoniteDriver import MasoniteDriver
from ..services.Configuration import Configuration

class RegisterCommand(CLICommand):
    """
    Registers the current directory to serve Python applications

    register
        {directory? : The directory you want to register}
    """

    def handle(self):
        if self.argument('directory'):
            directory = self.argument('directory')
        else:
            directory = os.getcwd()

        configuration = Configuration()

        self.info(f'Adding current directory: {directory}')
        configuration.set('directories', [directory])
        self.info('Directory Added Successfully')

        self.call("start")