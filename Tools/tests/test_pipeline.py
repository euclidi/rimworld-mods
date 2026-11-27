import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pipeline

META = """<ModMetaData><name>Fixture</name><author>Test</author>
<packageId>euclidi.fixture</packageId><description>Test</description>
<supportedVersions><li>1.7</li></supportedVersions></ModMetaData>"""

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.mod = self.root / "Mods" / "Fixture"
        (self.mod / "About").mkdir(parents=True)
        self.meta = self.mod / "About" / "About.xml"
        self.meta.write_text(META)

    def test_valid(self):
        self.assertEqual([], pipeline.check(self.root))

    def test_malformed_xml(self):
        self.meta.write_text("<broken")
        self.assertTrue(pipeline.check(self.root))

    def test_required_dlc_rejected(self):
        self.meta.write_text(META.replace("</ModMetaData>", "<modDependencies><li><packageId>Ludeon.RimWorld.Biotech</packageId></li></modDependencies></ModMetaData>"))
        self.assertTrue(any("paid DLC" in e for e in pipeline.check(self.root)))

    def test_wrong_version_rejected(self):
        self.meta.write_text(META.replace("1.7", "1.6"))
        self.assertTrue(pipeline.check(self.root))

    def test_missing_assembly_rejected(self):
        (self.mod / "Source").mkdir()
        (self.mod / "Source" / "x.csproj").write_text("<Project/>")
        self.assertTrue(pipeline.check(self.root))
        self.assertEqual([], pipeline.check(self.root, require_assemblies=False))

    def test_package_excludes_source(self):
        (self.mod / "Source").mkdir()
        (self.mod / "Source" / "note.txt").write_text("not runtime")
        pipeline.package(self.root)
        with zipfile.ZipFile(self.root / "dist" / "Fixture-1.7.zip") as z:
            self.assertEqual(["Fixture/About/About.xml"], z.namelist())

if __name__ == "__main__":
    unittest.main()
