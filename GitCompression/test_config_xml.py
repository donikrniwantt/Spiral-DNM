import glob
import os
import unittest
import xml.etree.ElementTree as ET


class ServerConfigXMLTests(unittest.TestCase):
    def test_all_server_config_files_are_well_formed(self):
        repository_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_dir = os.path.join(repository_root, "exe", "conf")
        config_files = sorted(glob.glob(os.path.join(config_dir, "*.xml")))
        self.assertTrue(config_files, "No XML server configuration files found")

        for config_path in config_files:
            with self.subTest(config=os.path.basename(config_path)):
                ET.parse(config_path)

    def test_admin_tool_listeners_are_loopback_only(self):
        repository_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for filename, port in (("login_conf.xml", "25002"), ("version_conf.xml", "24002")):
            config_path = os.path.join(repository_root, "exe", "conf", filename)
            root = ET.parse(config_path).getroot()
            listeners = [
                peer for peer in root.findall(".//Listen/peer")
                if peer.get("handler") == "gmtoollink" and peer.get("port") == port
            ]
            self.assertEqual(len(listeners), 1, f"Expected one GM tool listener in {filename}")
            self.assertEqual(listeners[0].get("ip"), "127.0.0.1")


if __name__ == "__main__":
    unittest.main()
