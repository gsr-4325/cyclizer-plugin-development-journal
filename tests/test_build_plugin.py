from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.build_plugin import build_package

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = "third-party.development-journal"


class LocalPluginPackageTests(unittest.TestCase):
    def test_archive_is_reproducible_without_any_documents_or_urls(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "journal.cyclizer.plugin.zip"
            first = build_package(archive)
            content = archive.read_bytes()
            self.assertEqual(build_package(archive), first)
            self.assertEqual(archive.read_bytes(), content)
            with zipfile.ZipFile(archive) as bundle:
                self.assertEqual(len(bundle.namelist()), 3)
                manifest = json.loads(bundle.read("plugin.json"))
                self.assertEqual(manifest["version"], "0.2.0")
                self.assertEqual(manifest["requested_capabilities"], [])
                for name in bundle.namelist():
                    self.assertNotIn("docs/plans", name)
                    self.assertNotIn("site.json", name)
                    self.assertNotIn("http", bundle.read(name).decode("utf-8").lower())

    def test_real_sdk_handshake_only_claims_local_docs_contribute(self) -> None:
        sdk = ROOT.parent / "Cyclizer/components/cyclizer.product.platform/sdk/python"
        if not (sdk / "cyclizer_plugin_sdk.py").is_file():
            self.skipTest("Cyclizer source SDK not available")
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "journal.cyclizer.plugin.zip"
            build_package(archive)
            with zipfile.ZipFile(archive) as bundle:
                bundle.extractall(Path(directory) / "package")
            process = Path(directory) / "package/components" / COMPONENT / "process.py"
            bootstrap = (
                "import runpy,sys;sys.path.insert(0,sys.argv[1]);"
                "runpy.run_path(sys.argv[2],run_name='__main__')"
            )
            child = subprocess.run(
                [sys.executable, "-I", "-c", bootstrap, str(sdk), str(process)],
                input=b'{"op":"stop"}\n',
                capture_output=True,
                timeout=10,
                check=True,
            )
            declaration = json.loads(child.stdout.splitlines()[0])
            self.assertEqual(declaration["component_id"], COMPONENT)
            self.assertEqual(declaration.get("navigation", []), [])
            self.assertEqual(len(declaration["local_documents"]), 1)
            self.assertEqual(declaration["local_documents"][0]["document_set"], "cyclizer.plans")
            self.assertEqual(declaration["local_documents"][0]["point"], "cyclizer.ui-local-documents/v1")


if __name__ == "__main__":
    unittest.main()
