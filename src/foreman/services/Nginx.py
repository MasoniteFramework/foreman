import os
import subprocess  # skipcq: BAN-B404

from ..services.Configuration import Configuration
from ..settings import PATHS


class Nginx:
    configuration = Configuration()

    @staticmethod
    def get_config_path():
        nginx_conf = (
            subprocess.check_output(
                "/usr/local/bin/nginx -V 2>&1 | grep -o '\\-\\-conf-path=\\(.*conf\\)' | cut -d '=' -f2",
                shell=True,  # skipcq: BAN-B602
            )
            .decode("utf-8")
            .strip()
        )
        return os.path.dirname(nginx_conf)

    def update_custom_config(self, tld):
        with open(os.path.join(PATHS["stubs"], "foreman.conf")) as f:
            output = f.read()

        output = output.replace("TLD", tld)

        with open(
            os.path.join(self.configuration.get_config_path(), "nginx.conf"), "w+"
        ) as f:
            f.write(output)

    def force_link(self):
        nginx_foreman_config = os.path.join(
            self.get_config_path(), "servers/foreman.conf"
        )
        if os.path.exists(nginx_foreman_config):
            os.unlink(nginx_foreman_config)
        os.symlink(
            os.path.join(self.configuration.get_config_path(), "nginx.conf"),
            os.path.join(nginx_foreman_config),
        )
