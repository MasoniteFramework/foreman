import glob
import os
import subprocess
from pathlib import Path

from cleo import Command as CLICommand
from ..drivers.MasoniteDriver import MasoniteDriver
from ..services.Configuration import Configuration
from ..settings import PATHS


class InstallCommand(CLICommand):
    """
    Installs Foreman

    install
    """

    def handle(self):
        # Brew update
        self.info("Updating Brew ..")
        subprocess.run("brew update", shell=True)

        self.info("Creating foreman config directory .. ")
        subprocess.run("mkdir -p ~/.foreman", shell=True)

        self.install_nginx()
        self.install_dnsmasq()
        self.info("Done")

    def install_dnsmasq(self):
        self.info("Installing dnsmasq ..")
        subprocess.run("brew install dnsmasq", shell=True)

        # Ensure dnsmasq is configured to allow extra config files
        dnsmasq_config = "/usr/local/etc/dnsmasq.conf"
        with open(dnsmasq_config) as f:
            output = f.read()
        output = output.replace(
            "#conf-dir=/usr/local/etc/dnsmasq.d/,*.conf",
            "conf-dir=/usr/local/etc/dnsmasq.d/,*.conf",
        )
        with open(dnsmasq_config, "w+") as f:
            f.write(output)

        self.info("Configuring dnsmasq ..")
        subprocess.run(
            'echo "nameserver 127.0.0.1"|sudo tee /etc/resolver/test > /dev/null',
            shell=True,
        )

        dnsmasq_config = os.path.join(self.get_home_path(), ".foreman/dnsmasq")
        with open(dnsmasq_config, "w+") as f:
            f.write(f"address=/.test/127.0.0.1")

        if os.path.exists("/usr/local/etc/dnsmasq.d/dnsmasq-foreman.conf"):
            os.unlink("/usr/local/etc/dnsmasq.d/dnsmasq-foreman.conf")
        os.link(dnsmasq_config, "/usr/local/etc/dnsmasq.d/dnsmasq-foreman.conf")

        self.info("Restarting dnsmasq ..")
        subprocess.run("sudo brew services restart dnsmasq", shell=True)

    def install_nginx(self):
        self.info("Installing NGINX ..")
        subprocess.run("brew install nginx", shell=True)

        self.info("Stopping nginx ..")
        subprocess.run("sudo nginx -s stop", shell=True)

        self.info("Creating Foreman Nginx config ..")
        with open(os.path.join(PATHS["stubs"], "foreman.conf")) as f:
            output = f.read()

        output = output.replace("TLD", "test")

        self.info("Creating NGINX config ..")
        with open(os.path.join(self.get_home_path(), ".foreman/nginx.conf"), "w+") as f:
            f.write(output)

        os.unlink(os.path.join(self.nginx_config_path(), "servers/foreman.conf"))
        os.link(
            os.path.join(self.get_home_path(), ".foreman/nginx.conf"),
            os.path.join(self.nginx_config_path(), "servers/foreman.conf"),
        )

        self.info("Restarting nginx ..")
        subprocess.run("sudo nginx", shell=True)
        configuration = Configuration()
        configuration.set("tld", "test")
        configuration.set("venv_locations", ["venv", "env"])
        configuration.set("socket_directory", "/tmp")

    def nginx_config_path(self):
        nginx_conf = (
            subprocess.check_output(
                "nginx -V 2>&1 | grep -o '\-\-conf-path=\(.*conf\)' | cut -d '=' -f2",
                shell=True,
            )
            .decode("utf-8")
            .strip()
        )
        return os.path.dirname(nginx_conf)

    def current_user(self):
        return subprocess.check_output("whoami", shell=True).decode("utf-8").strip()

    def get_home_path(self):
        return str(Path.home())
