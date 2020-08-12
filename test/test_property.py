import datetime
import os
import shutil
import tempfile
import unittest
import numpy as np

import nixio as nix
import odml

from nixodmlconverter import convert


class TestBlock(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp("_odmlnix", "test_", tempfile.gettempdir())

        self.odml_doc = odml.Document(author='me', date=datetime.date.today(),
                                      version='0.0.1', repository='unknown')
        odml.Section(name='first section', parent=self.odml_doc)

    def tearDown(self):
        # cleanup temporary files and folder
        shutil.rmtree(self.test_dir)

    def test_odml_to_nix_none(self):
        file_name = 'tmp'
        nix_path = os.path.join(self.test_dir, file_name + '.nix')

        odml.Property(name=None, oid=None, definition=None,
                      parent=self.odml_doc.sections[0],
                      values=None, dtype=None,
                      unit=None, uncertainty=None,
                      reference=None, dependency=None,
                      dependency_value=None, value_origin=None)

        convert.nixwrite(self.odml_doc, nix_path, 'overwrite')
        nix_file = nix.File.open(nix_path)

        self.assertEqual(len(nix_file.sections[0].sections[0].props), 1)

        nix_prop = nix_file.sections[0].sections[0].props[0]

        self.assertGreater(len(getattr(nix_prop, "id")), 0)
        self.assertEqual(getattr(nix_prop, "name"), getattr(nix_prop, "id"))
        self.assertEqual(getattr(nix_prop, "values"), ())
        self.assertEqual(getattr(nix_prop, "data_type"), np.str_)
        self.assertEqual(getattr(nix_prop, "odml_type"), None)
        self.assertEqual(getattr(nix_prop, "definition"), None)
        self.assertEqual(getattr(nix_prop, "unit"), None)
        self.assertEqual(getattr(nix_prop, "uncertainty"), None)
        self.assertEqual(getattr(nix_prop, "reference"), None)
        self.assertEqual(getattr(nix_prop, "dependency"), None)
        self.assertEqual(getattr(nix_prop, "dependency_value"), None)
        self.assertEqual(getattr(nix_prop, "value_origin"), None)

        nix_file.close()

    def test_odml_to_nix_empty(self):
        file_name = 'tmp'
        nix_path = os.path.join(self.test_dir, file_name + '.nix')

        odml.Property(parent=self.odml_doc.sections[0])

        convert.nixwrite(self.odml_doc, nix_path, 'overwrite')
        nix_file = nix.File.open(nix_path)

        self.assertEqual(len(nix_file.sections[0].sections[0].props), 1)

        nix_prop = nix_file.sections[0].sections[0].props[0]

        self.assertGreater(len(getattr(nix_prop, "id")), 0)
        self.assertEqual(getattr(nix_prop, "name"), getattr(nix_prop, "id"))
        self.assertEqual(getattr(nix_prop, "values"), ())
        self.assertEqual(getattr(nix_prop, "data_type"), np.str_)
        self.assertEqual(getattr(nix_prop, "odml_type"), None)
        self.assertEqual(getattr(nix_prop, "definition"), None)
        self.assertEqual(getattr(nix_prop, "unit"), None)
        self.assertEqual(getattr(nix_prop, "uncertainty"), None)
        self.assertEqual(getattr(nix_prop, "reference"), None)
        self.assertEqual(getattr(nix_prop, "dependency"), None)
        self.assertEqual(getattr(nix_prop, "dependency_value"), None)
        self.assertEqual(getattr(nix_prop, "value_origin"), None)

        nix_file.close()

    def test_nix_to_odml_none(self):
        file_name = 'tmp'
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        nix_file_w = nix.File.open(nix_path, nix.FileMode.Overwrite)
        odml_path = os.path.join(self.test_dir, file_name + '.xml')

        odml.Property(name=None, oid=None, definition=None,
                      parent=self.odml_doc.sections[0],
                      values=None, dtype=None,
                      unit=None, uncertainty=None,
                      reference=None, dependency=None,
                      dependency_value=None, value_origin=None)

        convert.nixwrite(self.odml_doc, nix_path)
        nix_file_w.close()

        nix_file_r = nix.File.open(nix_path, nix.FileMode.ReadOnly)
        convert.odmlwrite(nix_file_r, odml_path)
        odml_doc = odml.load(odml_path)

        self.assertEqual(len(odml_doc.sections[0].props), 1)

        odml_prop = odml_doc.sections[0].props[0]

        self.assertGreater(len(getattr(odml_prop, "id")), 0)
        self.assertEqual(getattr(odml_prop, "name"), getattr(odml_prop, "id"))
        self.assertEqual(getattr(odml_prop, "values"), [])
        self.assertEqual(getattr(odml_prop, "dtype"), None)
        self.assertEqual(getattr(odml_prop, "definition"), None)
        self.assertEqual(getattr(odml_prop, "unit"), None)
        self.assertEqual(getattr(odml_prop, "uncertainty"), None)
        self.assertEqual(getattr(odml_prop, "reference"), None)
        self.assertEqual(getattr(odml_prop, "dependency"), None)
        self.assertEqual(getattr(odml_prop, "dependency_value"), None)
        self.assertEqual(getattr(odml_prop, "value_origin"), None)

        nix_file_r.close()

    def test_nix_to_odml_empty(self):
        file_name = 'tmp'
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        nix_file_w = nix.File.open(nix_path, nix.FileMode.Overwrite)
        odml_path = os.path.join(self.test_dir, file_name + '.xml')

        odml.Property(parent=self.odml_doc.sections[0])

        convert.nixwrite(self.odml_doc, nix_path)
        nix_file_w.close()

        nix_file_r = nix.File.open(nix_path, nix.FileMode.ReadOnly)
        convert.odmlwrite(nix_file_r, odml_path)
        odml_doc = odml.load(odml_path)

        self.assertEqual(len(odml_doc.sections[0].props), 1)

        odml_prop = odml_doc.sections[0].props[0]

        self.assertGreater(len(getattr(odml_prop, "id")), 0)
        self.assertEqual(getattr(odml_prop, "name"), getattr(odml_prop, "id"))
        self.assertEqual(getattr(odml_prop, "values"), [])
        self.assertEqual(getattr(odml_prop, "dtype"), None)
        self.assertEqual(getattr(odml_prop, "definition"), None)
        self.assertEqual(getattr(odml_prop, "unit"), None)
        self.assertEqual(getattr(odml_prop, "uncertainty"), None)
        self.assertEqual(getattr(odml_prop, "reference"), None)
        self.assertEqual(getattr(odml_prop, "dependency"), None)
        self.assertEqual(getattr(odml_prop, "dependency_value"), None)
        self.assertEqual(getattr(odml_prop, "value_origin"), None)

        nix_file_r.close()
