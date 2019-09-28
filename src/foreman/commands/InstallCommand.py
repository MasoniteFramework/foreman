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

    # def start_directory(self, directory, site):
    #     configuration = Configuration()
    #     self.info(f"Starting {site}..")
    #     venv_config = configuration.get('venvs')
    #     if site in venv_config:
    #         activation_environment = venv_config[site]
    #     else:
    #         activation_environment = self.find_virtual_environment_activation_file(
    #             directory, site)

    #     driver = self.make('masonite')
    #     # print(activation_environment)
    #     # return
    #     command = f"cd {directory}"
    #     command += f" && source {activation_environment}"
    #     command += f" && pip install uwsgi && set -m; nohup uwsgi --socket /tmp/{site}.test.sock --wsgi-file {self.make(driver).wsgi_path()} &> /dev/null &"
    #     subprocess.run(command, shell=True, close_fds=True,
    #                    env={'PYTHONPATH': f'{directory}'})

    # def get_registered_directories(self):
    #     directories = []
    #     for directory in Configuration().get('directories', []):
    #         directories += glob.glob(os.path.join(directory, '*/'))
    #     return directories

    # def find_virtual_environment_activation_file(self, directory, site):
    #     return os.path.join(directory, 'venv/bin/activate')

    # def make(self, driver):
    #     return self.drivers[driver]()
