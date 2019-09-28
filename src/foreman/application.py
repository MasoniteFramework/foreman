#!/usr/bin/env python
# import subprocess, os, glob
# from pathlib import Path
# home = str(Path.home())

import glob
import os
import subprocess
from pathlib import Path

from cleo import Application
from .commands.StartCommand import StartCommand
from .commands.RegisterCommand import RegisterCommand
from .commands.UnregisterCommand import UnregisterCommand
from .commands.VenvCommand import VenvCommand
from .commands.VenvUnregisterCommand import VenvUnregisterCommand
from .commands.InstallCommand import InstallCommand


application = Application(name="Masonite Foreman")
application.add(StartCommand())
application.add(RegisterCommand())
application.add(UnregisterCommand())
application.add(VenvCommand())
application.add(InstallCommand())

if __name__ == '__main__':
    application.run()

# folders = glob.glob(os.path.join(home, 'sites/*/'))

# for folder in folders:

#     folder = folder.split('/')[-2]
#     # print(folder)
#     # continue
#     activate_environment = f"source ~/sites/{folder}/venv/bin/activate"

#     command = f"cd ~/sites/{folder}"
#     command += f" && source venv/bin/activate"
#     command += f" && pip install uwsgi && set -m; nohup uwsgi --socket /tmp/{folder}.test.sock --wsgi-file wsgi.py &> /dev/null &"
#     subprocess.run(command, shell=True, close_fds=True,
#                 env={'PYTHONPATH': f'~/sites/{folder}/venv/lib/python3.6/site-packages'})
