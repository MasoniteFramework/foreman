import glob
import os
import subprocess
from pathlib import Path

from cleo import Command as CLICommand
from ..drivers.MasoniteDriver import MasoniteDriver
from ..services.Configuration import Configuration
from ..settings import PATHS


class TldCommand(CLICommand):
    """
    Changes the TLD to serve on

    tld
        {tld : The TLD to change to}
    """

    def handle(self):
        configuration = Configuration()
        tld = self.argument("tld")

        # Stop NGINX
        self.info("Stopping NGINX ..")
        subprocess.run("sudo nginx -s stop", shell=True)

        self.info("Killing all applications ..")
        self.call("kill")

        self.info("Setting TLD ..")
        configuration.set("tld", tld)

        # Add the foreman config
        with open(os.path.join(PATHS["stubs"], "foreman.conf")) as f:
            output = f.read()

        output = output.replace("TLD", tld)

        with open(os.path.join(self.get_home_path(), ".foreman/nginx.conf"), "w+") as f:
            f.write(output)

        self.info("Restarting nginx ..")
        subprocess.run("sudo nginx", shell=True)
        subprocess.run("sudo nginx -s reload", shell=True)

        self.info("Starting applications under new TLD ..")
        self.call("start")

    def get_home_path(self):
        return str(Path.home())
