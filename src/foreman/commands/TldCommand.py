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
        oldtld = configuration.get("tld")
        if oldtld is not None:
            subprocess.run(f"sudo rm -f /etc/resolver/{oldtld}", shell=True)
        configuration.set("tld", tld)

        # Add the foreman config
        with open(os.path.join(PATHS["stubs"], "foreman.conf")) as f:
            output = f.read()

        output = output.replace("TLD", tld)

        with open(os.path.join(self.get_home_path(), ".foreman/nginx.conf"), "w+") as f:
            f.write(output)
        self.configure_dnsmasq(tld)

        self.info("Restarting nginx ..")
        subprocess.run("sudo nginx", shell=True)
        subprocess.run("sudo nginx -s reload", shell=True)

        self.info("Starting applications under new TLD ..")
        self.call("start")

    def get_home_path(self):
        return str(Path.home())

    def configure_dnsmasq(self, tld):
        subprocess.run(
            f'echo "nameserver 127.0.0.1"|sudo tee /etc/resolver/{tld} > /dev/null',
            shell=True,
        )

        dnsmasq_config = os.path.join(self.get_home_path(), ".foreman/dnsmasq")
        with open(dnsmasq_config, "w+") as f:
            f.write(f"address=/.{tld}/127.0.0.1")

        if os.path.exists("/usr/local/etc/dnsmasq.d/dnsmasq-foreman.conf"):
            os.unlink("/usr/local/etc/dnsmasq.d/dnsmasq-foreman.conf")
        os.link(dnsmasq_config, "/usr/local/etc/dnsmasq.d/dnsmasq-foreman.conf")
        self.restart_dns_masq()

    def restart_dns_masq(self):
        self.info("Restarting dnsmasq ..")
        subprocess.run("sudo brew services restart dnsmasq", shell=True)
