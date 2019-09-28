import glob
import os
import subprocess
from pathlib import Path

from cleo import Command as CLICommand
from ..drivers.MasoniteDriver import MasoniteDriver
from ..services.Configuration import Configuration

class VenvCommand(CLICommand):
    """
    Unregisters the path to the virtualenv directory

    venv:register
        {directory? : The directory you want to register the venv directory}
    """

    def handle(self):
        if self.argument('directory'):
            directory = self.argument('directory')
        else:
            directory = os.getcwd()

        configuration = Configuration()

        site = os.getcwd().split('/')[-1]
        
        if 'VIRTUAL_ENV' in os.environ:
            virtual = os.environ['VIRTUAL_ENV']
            self.info(f'Registering {virtual} for {site}')
            configuration.set('venvs', {
                site: virtual
            })
            self.info("Registered")
        else:
            self.info(f'Could not detect virtualenv path. Ensure you are inside your virtualenv.')