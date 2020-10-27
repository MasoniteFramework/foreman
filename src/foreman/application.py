#!/usr/bin/env python
from cleo import Application
from .commands.StartCommand import StartCommand
from .commands.RegisterCommand import RegisterCommand
from .commands.UnregisterCommand import UnregisterCommand
from .commands.VenvCommand import VenvCommand
from .commands.VenvUnregisterCommand import VenvUnregisterCommand
from .commands.InstallCommand import InstallCommand
from .commands.KillCommand import KillCommand
from .commands.TldCommand import TldCommand
from .commands.ConfigCommand import ConfigCommand


application = Application(name="Masonite Foreman")
application.add(StartCommand())
application.add(RegisterCommand())
application.add(UnregisterCommand())
application.add(VenvCommand())
application.add(VenvUnregisterCommand())
application.add(InstallCommand())
application.add(KillCommand())
application.add(TldCommand())
application.add(ConfigCommand())

if __name__ == "__main__":
    application.run()
