import os
import site
import subprocess
from pathlib import Path

from pyfakefs.fake_filesystem_unittest import TestCase

from foreman.services.Nginx import Nginx


class Test_Nginx(TestCase):
    package_path = os.path.dirname(os.path.dirname(__file__))

    def setUp(self):
        self.setUpPyfakefs()
        for packages_dir in site.getsitepackages():
            self.fs.add_real_directory(packages_dir)

    def test_get_config_path(self):
        expected_config_path = "/usr/local/etc/nginx"
        actual_config_path = Nginx().get_config_path()
        self.assertEqual(expected_config_path, actual_config_path)

    def test_update_custom_config(self):
        home = Path.home()
        os.makedirs(f"{home}/.foreman", exist_ok=True)
        self.assertFalse(os.path.exists(f"{home}/.foreman/nginx.conf"))
        Nginx().update_custom_config("test")
        self.assertTrue(os.path.exists(f"{home}/.foreman/nginx.conf"))

    def test_force_link(self):
        os.makedirs("/usr/local/etc/nginx/servers", exist_ok=True)
        home = Path.home()
        os.makedirs(f"{home}/.foreman", exist_ok=True)
        self.fs.create_file(f"{home}/.foreman/nginx.conf")
        subprocess.check_output = subprocess_check_output
        Nginx().force_link()
        self.assertTrue(os.path.exists("/usr/local/etc/nginx/servers/foreman.conf"))


def subprocess_check_output(command, shell=False, check=False):
    if command.startswith("/usr/local/bin/nginx"):
        return "/usr/local/etc/nginx/nginx.conf".encode()
    return "".encode()
