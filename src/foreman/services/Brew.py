import subprocess


class Brew:
    @staticmethod
    def install(package: str) -> None:
        subprocess.run(["/usr/local/bin/brew", "install", package], check=True)

    @staticmethod
    def update() -> None:
        subprocess.run(["/usr/local/bin/brew", "update"], check=True)

    def stop_service(self, service: str, use_sudo=False) -> None:
        self.run_command(service, "stop", use_sudo)

    def start_service(self, service: str, use_sudo=False) -> None:
        self.run_command(service, "start", use_sudo)

    def restart_service(self, service: str, use_sudo=False) -> None:
        self.run_command(service, "restart", use_sudo)

    @classmethod
    def run_command(cls, service: str, action: str, use_sudo=False):
        command = ["/usr/local/bin/brew", "services", action, service]
        if use_sudo:
            command = ["sudo"] + command
        subprocess.run(command, check=True)
