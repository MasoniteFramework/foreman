from cleo import Command as CLICommand

from ..services.Brew import Brew
from ..services.Dnsmasq import Dnsmasq
from ..services.Configuration import Configuration
from ..services.Nginx import Nginx


class InstallCommand(CLICommand):
    """
    Installs Foreman

    install
    """

    def handle(self) -> None:
        self.info("Creating foreman config directory .. ")
        self.configuration = Configuration()
        self.configuration.init()
        self.configuration.set("venv_locations", ["venv", "env"])

        self.brew = Brew()
        self.info("Updating Brew ..")
        self.brew.update()

        self.install_dnsmasq()
        self.install_nginx()
        self.info("Done")

    def install_dnsmasq(self) -> None:
        self.info("Installing dnsmasq ..")
        self.brew.install("dnsmasq")
        dnsmasq = Dnsmasq()
        dnsmasq.enable_custom_configs()

        self.info("Configuring dnsmasq ..")
        dnsmasq.update_custom_dns(self.configuration.get("tld", "test"))
        dnsmasq.force_link()

        self.info("Restarting dnsmasq ..")
        self.brew.restart_service("dnsmasq", use_sudo=True)

    def install_nginx(self):
        self.info("Installing NGINX ..")
        self.brew.install("nginx")

        self.info("Stopping nginx ..")
        self.brew.stop_service("nginx")

        self.info("Creating Foreman Nginx config ..")
        nginx = Nginx()
        nginx.update_custom_config(self.configuration.get("tld"))
        nginx.force_link()

        self.info("Starting nginx ..")
        self.brew.start_service("nginx")
        self.configuration.set("socket_directory", "/tmp")
