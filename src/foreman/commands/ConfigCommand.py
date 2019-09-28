import glob
import os
import subprocess
from pathlib import Path

from cleo import Command as CLICommand
from ..drivers.MasoniteDriver import MasoniteDriver
from ..services.Configuration import Configuration

class ConfigCommand(CLICommand):
    """
    Sets or gets a config

    config
        {key : The key of the config to get}
        {value? : The value of the config to set}
    """

    def handle(self):   
        configuration = Configuration()
        if self.argument('value'):
            configuration.set(self.argument('key'), self.argument('value'))

        return self.info(configuration.get(self.argument('key')))  