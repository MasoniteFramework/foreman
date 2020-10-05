import os
import subprocess

from ..services.Configuration import Configuration


class Dnsmasq:
    def __init__(self):
        self.configuration = Configuration()

    def get_custom_config_dir(self) -> str:
        return "/usr/local/etc/dnsmasq.d/"

    def enable_custom_configs(self) -> None:
        """ Ensure dnsmasq is configured to allow extra config files """
        dnsmasq_config = "/usr/local/etc/dnsmasq.conf"
        with open(dnsmasq_config) as f:
            output = f.read()
        output = output.replace(
            "#conf-dir=/usr/local/etc/dnsmasq.d/,*.conf",
            "conf-dir=/usr/local/etc/dnsmasq.d/,*.conf",
        )
        with open(dnsmasq_config, "w+") as f:
            f.write(output)

    def remove_old_dns(self) -> None:
        oldtld = str(self.configuration.get("tld"))
        if oldtld != "":
            subprocess.run(f"sudo rm -f /etc/resolver/{oldtld}", shell=True)

    def update_custom_dns(self, tld: str) -> None:
        self.remove_old_dns()

        self.configuration.set("tld", tld)
        subprocess.run(
            f'echo "nameserver 127.0.0.1"|sudo tee /etc/resolver/{tld} > /dev/null',
            shell=True,
        )
        dnsmasq_config = os.path.join(
            self.configuration.get_config_path(), "dnsmasq.conf"
        )
        with open(dnsmasq_config, "w+") as f:
            f.write(f"address=/.{tld}/127.0.0.1")

    def force_link(self) -> None:
        dnsmasq_config = os.path.join(
            self.configuration.get_config_path(), "dnsmasq.conf"
        )
        dnsmasq_foreman_config = os.path.join(
            self.get_custom_config_dir(), "dnsmasq-foreman.conf"
        )
        if os.path.exists(dnsmasq_foreman_config):
            os.unlink(dnsmasq_foreman_config)
        os.symlink(dnsmasq_config, dnsmasq_foreman_config)
