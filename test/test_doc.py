import os
import shutil
import tempfile
import unittest

import nixio as nix
import odml

from nixodmlconverter import convert


class TestBlock(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp("_odmlnix", "test_", tempfile.gettempdir())

    def tearDown(self):
        # cleanup temporary files and folder
        shutil.rmtree(self.test_dir)

    def test_odml_to_nix_none(self):
        file_name = 'tmp'
        nix_path = os.path.join(self.test_dir, file_name + '.nix')

        odml_doc = odml.Document(author=None, date=None,
                                 version=None, repository=None)

        convert.nixwrite(odml_doc, nix_path, 'overwrite')
        nix_file = nix.File.open(nix_path)

        self.assertEqual(len(nix_file.sections), 1)
        self.assertEqual(len(nix_file.sections[0].props), 0)

        nix_doc = nix_file.sections[0]
        self.assertGreater(len(getattr(nix_doc, "id")), 0)
        nix_file.close()

    def test_odml_to_nix_empty(self):
        file_name = 'tmp'
        nix_path = os.path.join(self.test_dir, file_name + '.nix')

        odml_doc = odml.Document()

        convert.nixwrite(odml_doc, nix_path, 'overwrite')
        nix_file = nix.File.open(nix_path)

        self.assertEqual(len(nix_file.sections), 1)
        self.assertEqual(len(nix_file.sections[0].props), 0)

        nix_doc = nix_file.sections[0]
        self.assertGreater(len(getattr(nix_doc, "id")), 0)
        nix_file.close()

    def test_nix_to_odml_none(self):
        file_name = 'tmp'
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        odml_path = os.path.join(self.test_dir, file_name + '.xml')

        orig_odml_doc = odml.Document(author=None, date=None,
                                      version=None, repository=None)

        convert.nixwrite(orig_odml_doc, nix_path, nix.FileMode.Overwrite)

        nix_file_r = nix.File.open(nix_path, nix.FileMode.ReadOnly)
        convert.odmlwrite(nix_file_r, odml_path)
        odml_doc = odml.load(odml_path)

        self.assertGreater(len(getattr(odml_doc, "id")), 0)
        self.assertEqual(getattr(odml_doc, "author"), None)
        self.assertEqual(getattr(odml_doc, "version"), None)
        self.assertEqual(getattr(odml_doc, "repository"), None)

        nix_file_r.close()

    def test_nix_to_odml_empty(self):
        file_name = 'tmp'
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        odml_path = os.path.join(self.test_dir, file_name + '.xml')

        orig_odml_doc = odml.Document()

        convert.nixwrite(orig_odml_doc, nix_path, nix.FileMode.Overwrite)

        nix_file_r = nix.File.open(nix_path, nix.FileMode.ReadOnly)
        convert.odmlwrite(nix_file_r, odml_path)
        odml_doc = odml.load(odml_path)

        self.assertGreater(len(getattr(odml_doc, "id")), 0)
        self.assertEqual(getattr(odml_doc, "author"), None)
        self.assertEqual(getattr(odml_doc, "version"), None)
        self.assertEqual(getattr(odml_doc, "repository"), None)

        nix_file_r.close()
