import glob
import os

from cleo import Command as CLICommand

from ..services.Configuration import Configuration


class KillCommand(CLICommand):
    """
    Kills serving applications

    kill
        {app? : The application name you want to kill}
    """

    def handle(self):
        if self.argument("app"):
            self.kill(self.argument("app"))
        else:
            for directory in self.get_registered_directories():
                app = directory.split("/")[-2]
                self.kill(app)

    def kill(self, app):
        self.info(f"Killing app: {app}")

        configuration = Configuration()
        tld = configuration.get("tld")
        socket_directory = configuration.get("socket_directory")
        pipe_file = f"{os.path.join(socket_directory, app)}.{tld}.sock"
        if os.path.exists(pipe_file):
            os.unlink(pipe_file)
        self.info("App stopped")

    def get_registered_directories(self):
        directories = []
        for directory in Configuration().get("directories", []):
            directories += glob.glob(os.path.join(directory, "*/"))
        return directories
