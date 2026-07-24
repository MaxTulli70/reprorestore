import io
import json
import tarfile
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from reprorestore.cli import main


MANIFEST = """\
[project]
name = "demo-service"
version = "1.0"

[[resources]]
name = "documents"
path = "documents"
required = true
"""


class ReproRestoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "documents").mkdir()
        (self.root / "documents" / "a.txt").write_text("alpha\n", encoding="utf-8")
        self.manifest = self.root / "reprorestore.toml"
        self.manifest.write_text(MANIFEST, encoding="utf-8")
        self.bundle = self.root / "bundle.tar.gz"

    def tearDown(self):
        self.tmp.cleanup()

    def test_inspect_and_capture_verify(self):
        self.assertEqual(main(["inspect", str(self.manifest)]), 0)
        self.assertEqual(
            main([
                "capture",
                str(self.manifest),
                "--source-root",
                str(self.root),
                "--output",
                str(self.bundle),
            ]),
            0,
        )
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = main(["verify", str(self.bundle)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(stream.getvalue())["status"], "PASS")

    def test_tamper_is_detected(self):
        main([
            "capture",
            str(self.manifest),
            "--source-root",
            str(self.root),
            "--output",
            str(self.bundle),
        ])
        unpack = self.root / "unpack"
        unpack.mkdir()
        with tarfile.open(self.bundle, "r:gz") as archive:
            archive.extractall(unpack, filter="data")
        (unpack / "payload" / "documents" / "a.txt").write_text("tampered\n", encoding="utf-8")
        with tarfile.open(self.bundle, "w:gz") as archive:
            archive.add(unpack / "evidence.json", arcname="evidence.json")
            archive.add(unpack / "payload", arcname="payload")
        self.assertEqual(main(["verify", str(self.bundle)]), 2)


if __name__ == "__main__":
    unittest.main()
