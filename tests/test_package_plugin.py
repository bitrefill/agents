import importlib.util
import json
from pathlib import Path
import stat
import tempfile
import unittest
import zipfile

from jsonschema import ValidationError

SPEC = importlib.util.spec_from_file_location('package_plugin', Path(__file__).resolve().parents[1] / 'scripts/package_plugin.py')
package = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package)


class PackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = package.source_files(package.ROOT)
        cls.version = json.loads(cls.files['plugin.json'])['version']

    def setUp(self):
        self.work = tempfile.TemporaryDirectory()
        self.addCleanup(self.work.cleanup)
        self.directory = Path(self.work.name)

    def archive(self, entries):
        archive = self.directory / 'test.zip'
        with zipfile.ZipFile(archive, 'w') as zipped:
            for name, data, mode in entries:
                info = zipfile.ZipInfo(name)
                info.create_system = 3
                info.external_attr = (mode | 0o644) << 16
                zipped.writestr(info, data)
        return archive

    def test_built_archive_has_complete_runtime_and_no_marketplace(self):
        archive = package.build(package.ROOT, self.directory, f'v{self.version}')
        package.validate_archive(archive, f'v{self.version}')
        with zipfile.ZipFile(archive) as zipped:
            self.assertEqual(set(zipped.namelist()), set(self.files))
            self.assertIn('assets/logo.png', zipped.namelist())
            self.assertNotIn('.claude-plugin/marketplace.json', zipped.namelist())
            self.assertEqual(zipped.read('plugin.json'), self.files['plugin.json'])

    def test_build_is_reproducible(self):
        first = package.build(package.ROOT, self.directory / 'a').read_bytes()
        second = package.build(package.ROOT, self.directory / 'b').read_bytes()
        self.assertEqual(first, second)

    def test_release_tag_must_match(self):
        with self.assertRaisesRegex(ValueError, 'does not match'):
            package.validate_files(self.files, 'v0.0.0')

    def test_missing_logo_fails(self):
        files = dict(self.files)
        del files['assets/logo.png']
        with self.assertRaisesRegex(ValueError, 'Missing asset'):
            package.validate_files(files)

    def test_legacy_mcp_transport_is_not_portable(self):
        files = dict(self.files)
        mcp = json.loads(files['mcp.json'])
        mcp['mcpServers']['bitrefill']['type'] = 'http'
        files['mcp.json'] = json.dumps(mcp).encode()
        with self.assertRaises(ValidationError):
            package.validate_files(files)

    def test_broken_skill_reference_fails(self):
        files = dict(self.files)
        files['skills/bitrefill/SKILL.md'] += b'\n[Missing](references/missing.md)\n'
        with self.assertRaisesRegex(ValueError, 'Broken reference'):
            package.validate_files(files)

    def test_shadowed_app_binding_is_rejected(self):
        files = dict(self.files)
        manifest = json.loads(files['.claude-plugin/plugin.json'])
        manifest['apps'] = {}
        files['.claude-plugin/plugin.json'] = json.dumps(manifest).encode()
        with self.assertRaisesRegex(ValueError, 'App binding prohibited'):
            package.validate_files(files)

    def test_oversized_subtitle_fails(self):
        files = dict(self.files)
        manifest = json.loads(files['plugin.json'])
        manifest['extensions']['com.openai']['interface']['shortDescription'] = 'x' * 31
        files['plugin.json'] = json.dumps(manifest).encode()
        with self.assertRaisesRegex(ValueError, 'Invalid shortDescription'):
            package.validate_files(files)

    def test_zip_rejects_path_traversal_and_symlinks(self):
        for name, mode in [('../secret', stat.S_IFREG), ('assets/link', stat.S_IFLNK)]:
            with self.subTest(name=name):
                archive = self.archive([(name, b'bad', mode)])
                with self.assertRaisesRegex(ValueError, 'Unsafe ZIP path|Non-regular ZIP file'):
                    package.validate_archive(archive)

    def test_zip_rejects_case_collisions(self):
        archive = self.archive([('plugin.json', b'{}', stat.S_IFREG), ('PLUGIN.JSON', b'{}', stat.S_IFREG)])
        with self.assertRaisesRegex(ValueError, 'Duplicate ZIP path'):
            package.validate_archive(archive)

    def test_zip_rejects_marketplace_and_private_files(self):
        for name in ('.claude-plugin/marketplace.json', '.app.json', '.env', 'skills/bitrefill/.env'):
            with self.subTest(name=name):
                archive = self.archive([(name, b'{}', stat.S_IFREG)])
                with self.assertRaisesRegex(ValueError, 'Unrelated ZIP entry|Hidden ZIP entry'):
                    package.validate_archive(archive)

    def test_archive_validation_checks_contents(self):
        files = dict(self.files)
        del files['assets/logo.png']
        archive = self.archive([(name, data, stat.S_IFREG) for name, data in files.items()])
        with self.assertRaisesRegex(ValueError, 'Missing asset'):
            package.validate_archive(archive)


if __name__ == '__main__':
    unittest.main()
