import os
import subprocess
from pathlib import Path
from pyfakefs.fake_filesystem_unittest import TestCase

from foreman.services.Dnsmasq import Dnsmasq


class Test_Dnsmasq(TestCase):
    package_path = os.path.dirname(os.path.dirname(__file__))
    def setUp(self):
        self.setUpPyfakefs()
        self.fs.add_real_directory(self.package_path)
        self.home = Path.home()
        os.makedirs(f"{self.home}/.foreman", exist_ok=True)
        os.makedirs("/usr/local/etc/dnsmasq.d", exist_ok=True)
        os.makedirs("/etc/resolver", exist_ok=True)

    def test_get_custom_config_dir(self):
        self.assertEqual("/usr/local/etc/dnsmasq.d/", Dnsmasq().get_custom_config_dir())

    def test_enable_custom_configs(self):
        dnsmasq_config = "/usr/local/etc/dnsmasq.conf"
        self.fs.create_file(dnsmasq_config, contents="""
            some content
            #conf-dir=/usr/local/etc/dnsmasq.d/,*.conf
            #some other content
            """
        )
        Dnsmasq().enable_custom_configs()
        with open(dnsmasq_config) as f:
            actual = f.read()
        self.assertIn("conf-dir=/usr/local/etc/dnsmasq.d/,*.conf", actual)

    def test_remove_old_dns(self):
        self.fs.create_file("/etc/resolver/test")
        self.fs.create_file(f"{self.home}/.foreman/config.yml", contents="tld: test")
        subprocess.run = subprocess_run
        Dnsmasq().remove_old_dns()
        self.assertFalse(os.path.exists("/etc/resolver/test"))

    def test_update_custom_dns(self):
        self.fs.create_file("/etc/resolver/test")
        self.fs.create_file(f"{self.home}/.foreman/config.yml", contents="tld: test")
        subprocess.run = subprocess_run
        Dnsmasq().update_custom_dns('test2')
        self.assertFalse(os.path.exists("/etc/resolver/test"))
        self.assertTrue(os.path.exists("/etc/resolver/test2"))
        with open(f"{self.home}/.foreman/dnsmasq.conf") as f:
            actual = f.read()
        self.assertEqual("address=/.test2/127.0.0.1", actual)

    def test_force_link(self):
        self.fs.create_file(f"{self.home}/.foreman/dnsmasq.conf")
        Dnsmasq().force_link()
        self.assertTrue(os.path.exists("/usr/local/etc/dnsmasq.d/dnsmasq-foreman.conf"))

def subprocess_run(command, shell=False):
    if command.startswith("sudo"):
        os.remove('/etc/resolver/test')
    if  command.startswith("echo"):
        with open('/etc/resolver/test2', "w+") as f:
            f.write('nameserver 127.0.0.1')
    return "".encode()
