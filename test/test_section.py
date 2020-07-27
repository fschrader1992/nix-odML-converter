import datetime
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

        self.odml_doc = odml.Document(author='me', date=datetime.date.today(),
                                      version='0.0.1', repository='unknown')

    def tearDown(self):
        # cleanup temporary files and folder
        shutil.rmtree(self.test_dir)

    def test_odml_to_nix_none(self):
        file_name = 'tmp'
        nix_path = os.path.join(self.test_dir, file_name + '.nix')

        odml.Section(name=None, oid=None, definition=None,
                     parent=self.odml_doc, type="MustBeSet",
                     reference=None, repository=None,
                     link=None, include=None)

        convert.nixwrite(self.odml_doc, nix_path, 'overwrite')
        nix_file = nix.File.open(nix_path)

        self.assertEqual(len(nix_file.sections[0].sections), 1)

        nix_sec = nix_file.sections[0].sections[0]

        self.assertGreater(len(getattr(nix_sec, "id")), 0)
        self.assertEqual(getattr(nix_sec, "name"), getattr(nix_sec, "id"))
        self.assertEqual(getattr(nix_sec, "type"), "MustBeSet")
        self.assertEqual(getattr(nix_sec, "definition"), None)
        self.assertEqual(getattr(nix_sec, "reference"), None)
        self.assertEqual(getattr(nix_sec, "repository"), None)
        self.assertEqual(getattr(nix_sec, "link"), None)
        #self.assertEqual(getattr(nix_sec, "include"), None)

        nix_file.close()

    def test_odml_to_nix_empty(self):
        file_name = 'tmp'
        nix_path = os.path.join(self.test_dir, file_name + '.nix')

        odml.Section(parent=self.odml_doc)

        convert.nixwrite(self.odml_doc, nix_path, 'overwrite')
        nix_file = nix.File.open(nix_path)

        self.assertEqual(len(nix_file.sections[0].sections), 1)

        nix_sec = nix_file.sections[0].sections[0]

        self.assertGreater(len(getattr(nix_sec, "id")), 0)
        self.assertEqual(getattr(nix_sec, "name"), getattr(nix_sec, "id"))
        self.assertEqual(getattr(nix_sec, "type"), "n.s.")
        self.assertEqual(getattr(nix_sec, "definition"), None)
        self.assertEqual(getattr(nix_sec, "reference"), None)
        self.assertEqual(getattr(nix_sec, "repository"), None)
        self.assertEqual(getattr(nix_sec, "link"), None)
        #self.assertEqual(getattr(nix_sec, "include"), None)

        nix_file.close()

    def test_nix_to_odml_none(self):
        file_name = 'tmp'
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        nix_file_w = nix.File.open(nix_path, nix.FileMode.Overwrite)
        odml_path = os.path.join(self.test_dir, file_name + '.xml')

        odml.Section(name=None, oid=None, definition=None,
                     parent=self.odml_doc, type="MustBeSet",
                     reference=None, repository=None,
                     link=None, include=None)

        convert.nixwrite(self.odml_doc, nix_path)
        nix_file_w.close()

        nix_file_r = nix.File.open(nix_path, nix.FileMode.ReadOnly)
        convert.odmlwrite(nix_file_r, odml_path)
        odml_doc = odml.load(odml_path)
        self.assertEqual(len(odml_doc.sections), 1)
        odml_sec = odml_doc.sections[0]

        self.assertGreater(len(getattr(odml_sec, "id")), 0)
        self.assertEqual(getattr(odml_sec, "name"), getattr(odml_sec, "id"))
        self.assertEqual(getattr(odml_sec, "type"), "MustBeSet")
        self.assertEqual(getattr(odml_sec, "definition"), None)
        self.assertEqual(getattr(odml_sec, "reference"), None)
        self.assertEqual(getattr(odml_sec, "repository"), None)
        self.assertEqual(getattr(odml_sec, "link"), None)
        self.assertEqual(getattr(odml_sec, "include"), None)

        nix_file_r.close()

    def test_nix_to_odml_empty(self):
        file_name = 'tmp'
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        nix_file_w = nix.File.open(nix_path, nix.FileMode.Overwrite)
        odml_path = os.path.join(self.test_dir, file_name + '.xml')

        odml.Section(parent=self.odml_doc)

        convert.nixwrite(self.odml_doc, nix_path)
        nix_file_w.close()

        nix_file_r = nix.File.open(nix_path, nix.FileMode.ReadOnly)
        convert.odmlwrite(nix_file_r, odml_path)
        odml_doc = odml.load(odml_path)
        self.assertEqual(len(odml_doc.sections), 1)
        odml_sec = odml_doc.sections[0]

        self.assertGreater(len(getattr(odml_sec, "id")), 0)
        self.assertEqual(getattr(odml_sec, "name"), getattr(odml_sec, "id"))
        self.assertEqual(getattr(odml_sec, "type"), "n.s.")
        self.assertEqual(getattr(odml_sec, "definition"), None)
        self.assertEqual(getattr(odml_sec, "reference"), None)
        self.assertEqual(getattr(odml_sec, "repository"), None)
        self.assertEqual(getattr(odml_sec, "link"), None)
        self.assertEqual(getattr(odml_sec, "include"), None)

        nix_file_r.close()
