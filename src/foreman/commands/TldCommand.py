from cleo import Command as CLICommand

from ..services.Brew import Brew
from ..services.Configuration import Configuration
from ..services.Dnsmasq import Dnsmasq
from ..services.Nginx import Nginx


class TldCommand(CLICommand):
    """
    Changes the TLD to serve on (or displays current selected TLD if no argument provided)

    tld
        {tld? : The TLD to change to}
    """

    def handle(self) -> None:
        dnsmasq = Dnsmasq()
        nginx = Nginx()
        brew = Brew()
        configuration = Configuration()
        tld = self.argument("tld")
        if tld is None:
            self.info(configuration.get("tld"))
            return

        self.info("Killing all applications ..")
        self.call("kill")

        self.info("Setting TLD ..")
        dnsmasq.update_custom_dns(tld)
        nginx.update_custom_config(tld)

        self.info("Restarting dnsmasq ..")
        brew.restart_service("dnsmasq", use_sudo=True)

        self.info("Restarting nginx ..")
        brew.restart_service("nginx")

        self.info("Starting applications under new TLD ..")
        self.call("start")
