import os
import tempfile
import unittest

import CompressLFS
import RestoreLFS


class CompressLFSTests(unittest.TestCase):
    def _round_trip(self, payload, split_size):
        with tempfile.TemporaryDirectory() as root:
            source_path = os.path.join(root, "payload.bin")
            with open(source_path, "wb") as source:
                source.write(payload)

            self.assertTrue(
                CompressLFS.process_files(root, max_size=64, split_size=split_size)
            )
            self.assertFalse(os.path.exists(source_path))
            self.assertTrue(RestoreLFS.restore_files(root))

            with open(source_path, "rb") as restored:
                self.assertEqual(restored.read(), payload)

    def test_regular_archive_round_trip(self):
        self._round_trip(b"A" * 1024, 4096)

    def test_split_archive_round_trip(self):
        self._round_trip(bytes(range(256)) * 64, 128)

    def test_existing_archive_fails_without_deleting_original(self):
        with tempfile.TemporaryDirectory() as root:
            source_path = os.path.join(root, "payload.bin")
            with open(source_path, "wb") as source:
                source.write(b"payload" * 100)
            with open(source_path + ".zip", "wb") as archive:
                archive.write(b"existing")

            self.assertFalse(
                CompressLFS.process_files(root, max_size=64, split_size=128)
            )
            self.assertTrue(os.path.exists(source_path))


if __name__ == "__main__":
    unittest.main()
