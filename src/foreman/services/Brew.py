import subprocess


class Brew:
    def install(self, package: str) -> None:
        subprocess.run(f"brew install {package}", shell=True)

    def update(self) -> None:
        subprocess.run("brew update", shell=True)

    def stop_service(self, service: str, use_sudo=False) -> None:
        self.run_command(service, "stop", use_sudo)

    def start_service(self, service: str, use_sudo=False) -> None:
        self.run_command(service, "start", use_sudo)

    def restart_service(self, service: str, use_sudo=False) -> None:
        self.run_command(service, "restart", use_sudo)

    def run_command(self, service: str, action: str, use_sudo=False):
        command = f"brew services {action} {service}"
        if use_sudo:
            command = f"sudo {command}"
        subprocess.run(command, shell=True)
