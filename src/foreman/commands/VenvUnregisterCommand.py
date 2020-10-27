import os

from cleo import Command as CLICommand

from ..services.Configuration import Configuration


class VenvUnregisterCommand(CLICommand):
    """
    Unregisters the path to the virtualenv directory

    venv:unregister
        {directory? : The directory you want to register the venv directory}
    """

    def handle(self):
        if self.argument("directory"):
            directory = self.argument("directory")
        else:
            directory = os.getcwd()

        configuration = Configuration()

        site = os.getcwd().split("/")[-1]

        if "VIRTUAL_ENV" in os.environ:
            virtual = os.environ["VIRTUAL_ENV"]
            self.info(f"Unregistering {virtual} for {site}")
            configuration.remove("venvs", site)
            self.info("Registered")
        else:
            self.info("Could not detect virtualenv path")
