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
        self.info('Updating Brew ..')
        subprocess.run("brew update", shell=True)
        # Brew install NGINX
        self.info('Installing NGINX ..')
        subprocess.run("brew install nginx", shell=True)

        self.info('Stopping nginx ..')
        subprocess.run("sudo nginx -s stop", shell=True)
        with open(os.path.join(PATHS['stubs'], 'nginx.conf')) as f:
            output = f.read()
        
        self.info('Creating foreman config directory .. ')
        subprocess.run("mkdir -p ~/.foreman", shell=True)

        self.info('Moving NGINX config ..')
        output = output.replace('FOREMAN_NGINX_CONF', os.path.join(
            self.get_home_path(), '.foreman/nginx.conf'))
        output = output.replace('SYSTEM_USER', self.current_user())
        
        with open(self.nginx_config_path(), 'w+') as f:
            f.write(output)

        self.info("Moving Foreman config ..")

        with open(os.path.join(PATHS['stubs'], 'foreman.conf')) as f:
            output = f.read()

        output = output.replace('TLD', 'test')

        with open(os.path.join(self.get_home_path(), '.foreman/nginx.conf'), 'w+') as f:
            f.write(output)

        self.info('Restarting nginx ..')
        subprocess.run("sudo nginx", shell=True)
        # subprocess.run("sudo nginx -s reload", shell=True)

    def nginx_config_path(self):
        return subprocess.check_output(
            "nginx -V 2>&1 | grep -o '\-\-conf-path=\(.*conf\)' | cut -d '=' -f2", shell=True).decode('utf-8').strip()
    
    def current_user(self):
        return subprocess.check_output("whoami", shell=True).decode('utf-8').strip()
    
    def get_home_path(self):
        return str(Path.home())
