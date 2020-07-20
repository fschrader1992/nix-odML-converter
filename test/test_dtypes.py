import datetime
import os
import shutil
import tempfile
import unittest
import numpy as np
import uuid

import nixio as nix
import odml

from nixodmlconverter import convert


class TestDtypes(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp("_odmlnix", "test_", tempfile.gettempdir())

        self.odml_doc = odml.Document(author='me', date=datetime.date.today(),
                                      version='0.0.1', repository='unknown')
        odml.Section(name='first section', parent=self.odml_doc)

    def tearDown(self):
        # cleanup temporary files and folder
        shutil.rmtree(self.test_dir)

    def test_odml_to_nix_string(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        odml.Property(name='string property', values=["a", "b", "c"],
                      parent=self.odml_doc.sections[0], dtype='string')
        convert.nixwrite(self.odml_doc, nix_path, 'overwrite')
        nix_file = nix.File.open(nix_path)
        nix_prop = nix_file.sections[0].sections[0].props[0]
        vals = nix_prop.values
        self.assertEqual(getattr(nix_prop, "odml_type"), nix.OdmlType("string"))
        self.assertEqual(getattr(nix_prop, "data_type"), np.str_)
        self.assertEqual(len(vals), 3)
        self.assertEqual(vals, ("a", "b", "c"))

    def test_odml_to_nix_int(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        odml.Property(name='int property', values=[1, 2, 3],
                      parent=self.odml_doc.sections[0], dtype='int')
        convert.nixwrite(self.odml_doc, nix_path, 'overwrite')
        nix_file = nix.File.open(nix_path)
        nix_prop = nix_file.sections[0].sections[0].props[0]
        vals = nix_prop.values
        self.assertEqual(getattr(nix_prop, "odml_type"), nix.OdmlType("int"))
        self.assertEqual(getattr(nix_prop, "data_type"), np.int_)
        self.assertEqual(len(vals), 3)
        self.assertEqual(vals, (1, 2, 3))

    '''
    # there seems to be a problem with float64 conversion in the nixpy lib
    def test_odml_to_nix_float(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        odml.Property(name='float property', values=[1.1, 2.2, 3.3],
                      parent=self.odml_doc.sections[0], dtype='float')
        convert.nixwrite(self.odml_doc, nix_path, 'overwrite')
        nix_file = nix.File.open(nix_path)
        nix_prop = nix_file.sections[0].sections[0].props[0]
        vals = nix_prop.values
        self.assertEqual(getattr(nix_prop, "odml_type"), nix.OdmlType("float"))
        self.assertEqual(getattr(nix_prop, "data_type"), np.float_)
        self.assertEqual(len(vals), 3)
        self.assertEqual(vals, (1.1, 2.2, 3.2))
    '''

    def test_odml_to_nix_boolean(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        odml.Property(name='boolean property', values=[True, False, 1],
                      parent=self.odml_doc.sections[0], dtype='boolean')
        convert.nixwrite(self.odml_doc, nix_path, 'overwrite')
        nix_file = nix.File.open(nix_path)
        nix_prop = nix_file.sections[0].sections[0].props[0]
        vals = nix_prop.values
        self.assertEqual(getattr(nix_prop, "odml_type"), nix.OdmlType("boolean"))
        self.assertEqual(getattr(nix_prop, "data_type"), np.bool_)
        self.assertEqual(len(vals), 3)
        self.assertEqual(vals, (True, False, 1))

    def test_odml_to_nix_date(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        odml.Property(name='date property', values=[datetime.date(2011, 12, 1), '2011-12-02'],
                      parent=self.odml_doc.sections[0], dtype='date')
        convert.nixwrite(self.odml_doc, nix_path, 'overwrite')
        nix_file = nix.File.open(nix_path)
        nix_prop = nix_file.sections[0].sections[0].props[0]
        vals = nix_prop.values
        self.assertEqual(getattr(nix_prop, "odml_type"), nix.OdmlType("date"))
        self.assertEqual(getattr(nix_prop, "data_type"), np.str_)
        self.assertEqual(len(vals), 2)
        self.assertEqual(vals, ('2011-12-01', '2011-12-02'))

    def test_odml_to_nix_time(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        odml.Property(name='time property', values=[datetime.time(11, 11, 11), '02:02:02'],
                      parent=self.odml_doc.sections[0], dtype='time')
        convert.nixwrite(self.odml_doc, nix_path, 'overwrite')
        nix_file = nix.File.open(nix_path)
        nix_prop = nix_file.sections[0].sections[0].props[0]
        vals = nix_prop.values
        self.assertEqual(getattr(nix_prop, "odml_type"), nix.OdmlType("time"))
        self.assertEqual(getattr(nix_prop, "data_type"), np.str_)
        self.assertEqual(len(vals), 2)
        self.assertEqual(vals, ('11:11:11', '02:02:02'))

    def test_odml_to_nix_datetime(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        odml.Property(name='datetime property',
                      values=[datetime.datetime(2011, 12, 1, 1, 1, 1), '2011-12-02 02:02:02'],
                      parent=self.odml_doc.sections[0], dtype='datetime')
        convert.nixwrite(self.odml_doc, nix_path, 'overwrite')
        nix_file = nix.File.open(nix_path)
        nix_prop = nix_file.sections[0].sections[0].props[0]
        vals = nix_prop.values
        self.assertEqual(getattr(nix_prop, "odml_type"), nix.OdmlType("datetime"))
        self.assertEqual(getattr(nix_prop, "data_type"), np.str_)
        self.assertEqual(len(vals), 2)
        self.assertEqual(vals, ('2011-12-01T01:01:01', '2011-12-02T02:02:02'))

    def test_odml_to_nix_text(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        odml.Property(name='text property', values=["a\nb", "c", "d\ne"],
                      parent=self.odml_doc.sections[0], dtype='text')
        convert.nixwrite(self.odml_doc, nix_path, 'overwrite')
        nix_file = nix.File.open(nix_path)
        nix_prop = nix_file.sections[0].sections[0].props[0]
        vals = nix_prop.values
        self.assertEqual(getattr(nix_prop, "odml_type"), nix.OdmlType("text"))
        self.assertEqual(getattr(nix_prop, "data_type"), np.str_)
        self.assertEqual(len(vals), 3)
        self.assertEqual(vals, ("a\nb", "c", "d\ne"))

    def test_odml_to_nix_tuple(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        odml.Property(name='2-tuple property', values=["(1; 2)", "(3; 4)"],
                      parent=self.odml_doc.sections[0], dtype='2-tuple')
        convert.nixwrite(self.odml_doc, nix_path, 'overwrite')
        nix_file = nix.File.open(nix_path)
        nix_prop = nix_file.sections[0].sections[0].props[0]
        vals = nix_prop.values
        #assert None, such that backconversion works correctly
        self.assertEqual(getattr(nix_prop, "odml_type"), None)
        self.assertEqual(getattr(nix_prop, "data_type"), np.str_)
        self.assertEqual(len(vals), 2)
        self.assertEqual(vals, ("(1; 2)", "(3; 4)"))
        nix_file.close()

        file_name_2 = 'tmp' + str(uuid.uuid4())
        nix_path_2 = os.path.join(self.test_dir, file_name_2 + '.nix')
        odml.Property(name='3-tuple property', values=["(1; 2; 3)", "(4; 5; 6)"],
                      parent=self.odml_doc.sections[0], dtype='3-tuple')
        convert.nixwrite(self.odml_doc, nix_path_2, 'overwrite')
        nix_file_2 = nix.File.open(nix_path_2)
        nix_prop_2 = nix_file_2.sections[0].sections[0].props[1]
        vals_2 = nix_prop_2.values
        #assert None, such that backconversion works correctly
        self.assertEqual(getattr(nix_prop_2, "odml_type"), None)
        self.assertEqual(getattr(nix_prop_2, "data_type"), np.str_)
        self.assertEqual(len(vals_2), 2)
        self.assertEqual(vals_2, ("(1; 2; 3)", "(4; 5; 6)"))

    def test_nix_to_odml_string(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        nix_file = nix.File.open(nix_path, nix.FileMode.Overwrite)
        odml_path = os.path.join(self.test_dir, file_name + '.xml')

        sec = nix_file.create_section(name="section")
        prop = sec.create_property(name="string property", values_or_dtype=np.str_)
        prop.values = ['a', 'b', 'c']

        convert.odmlwrite(nix_file, odml_path)
        odml_doc = odml.load(odml_path)

        odml_prop = odml_doc.sections[0].props[0]
        vals = odml_prop.values
        self.assertEqual(getattr(odml_prop, "dtype"), odml.DType.string)
        self.assertEqual(len(vals), 3)
        self.assertEqual(vals, ['a', 'b', 'c'])

        file_name_2 = 'tmp' + str(uuid.uuid4())
        nix_path_2 = os.path.join(self.test_dir, file_name_2 + '.nix')
        nix_file_2 = nix.File.open(nix_path_2, nix.FileMode.Overwrite)
        odml_path_2 = os.path.join(self.test_dir, file_name_2 + '.xml')

        sec_2 = nix_file_2.create_section(name="section")

        prop2 = sec_2.create_property(name="string property 2", values_or_dtype=np.str_)
        prop2.values = ['d', 'e', 'f']
        setattr(prop2, "odml_type", nix.OdmlType("string"))

        convert.odmlwrite(nix_file_2, odml_path_2)
        odml_doc_2 = odml.load(odml_path_2)

        odml_prop_2 = odml_doc_2.sections[0].props[0]
        vals = odml_prop_2.values
        self.assertEqual(getattr(odml_prop_2, "dtype"), odml.DType.string)
        self.assertEqual(len(vals), 3)
        self.assertEqual(vals, ["d", "e", "f"])

    def test_nix_to_odml_int(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        nix_file = nix.File.open(nix_path, nix.FileMode.Overwrite)
        odml_path = os.path.join(self.test_dir, file_name + '.xml')

        sec = nix_file.create_section(name="section")
        prop = sec.create_property(name="int property", values_or_dtype=np.int_)
        prop.values = [1, 2, 3]

        convert.odmlwrite(nix_file, odml_path)
        odml_doc = odml.load(odml_path)

        odml_prop = odml_doc.sections[0].props[0]
        vals = odml_prop.values
        self.assertEqual(getattr(odml_prop, "dtype"), odml.DType.int)
        self.assertEqual(len(vals), 3)
        self.assertEqual(vals, [1, 2, 3])
        
        file_name_2 = 'tmp' + str(uuid.uuid4())
        nix_path_2 = os.path.join(self.test_dir, file_name_2 + '.nix')
        nix_file_2 = nix.File.open(nix_path_2, nix.FileMode.Overwrite)
        odml_path_2 = os.path.join(self.test_dir, file_name_2 + '.xml')

        sec_2 = nix_file_2.create_section(name="section")

        prop2 = sec_2.create_property(name="string int property", values_or_dtype=np.str_)
        prop2.values = ["4", "5", "6"]

        convert.odmlwrite(nix_file_2, odml_path_2)
        odml_doc_2 = odml.load(odml_path_2)

        odml_prop_2 = odml_doc_2.sections[0].props[0]
        vals = odml_prop_2.values
        self.assertEqual(getattr(odml_prop_2, "dtype"), odml.DType.int)
        self.assertEqual(len(vals), 3)
        self.assertEqual(vals, [4, 5, 6])

        file_name_3 = 'tmp' + str(uuid.uuid4())
        nix_path_3 = os.path.join(self.test_dir, file_name_3 + '.nix')
        nix_file_3 = nix.File.open(nix_path_3, nix.FileMode.Overwrite)
        odml_path_3 = os.path.join(self.test_dir, file_name_3 + '.xml')

        sec_3 = nix_file_3.create_section(name="section")

        prop3 = sec_3.create_property(name="int property 3", values_or_dtype=np.int_)
        prop3.values = [7, 8, 9]
        setattr(prop3, "odml_type", nix.OdmlType("int"))

        convert.odmlwrite(nix_file_3, odml_path_3)
        odml_doc_3 = odml.load(odml_path_3)

        odml_prop_3 = odml_doc_3.sections[0].props[0]
        vals = odml_prop_3.values
        self.assertEqual(getattr(odml_prop_3, "dtype"), odml.DType.int)
        self.assertEqual(len(vals), 3)
        self.assertEqual(vals, [7, 8, 9])

    def test_nix_to_odml_float(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        nix_file = nix.File.open(nix_path, nix.FileMode.Overwrite)
        odml_path = os.path.join(self.test_dir, file_name + '.xml')

        sec = nix_file.create_section(name="section")
        prop = sec.create_property(name="float property", values_or_dtype=np.float_)
        prop.values = [1.1, 2.2, 3.3]

        convert.odmlwrite(nix_file, odml_path)
        odml_doc = odml.load(odml_path)

        odml_prop = odml_doc.sections[0].props[0]
        vals = odml_prop.values
        self.assertEqual(getattr(odml_prop, "dtype"), odml.DType.float)
        self.assertEqual(len(vals), 3)
        self.assertEqual(vals, [1.1, 2.2, 3.3])

        file_name_2 = 'tmp' + str(uuid.uuid4())
        nix_path_2 = os.path.join(self.test_dir, file_name_2 + '.nix')
        nix_file_2 = nix.File.open(nix_path_2, nix.FileMode.Overwrite)
        odml_path_2 = os.path.join(self.test_dir, file_name_2 + '.xml')

        sec_2 = nix_file_2.create_section(name="section")

        prop2 = sec_2.create_property(name="string float property", values_or_dtype=np.str_)
        prop2.values = ["4.4", "5.5", "6.6"]

        convert.odmlwrite(nix_file_2, odml_path_2)
        odml_doc_2 = odml.load(odml_path_2)

        odml_prop_2 = odml_doc_2.sections[0].props[0]
        vals = odml_prop_2.values
        self.assertEqual(getattr(odml_prop_2, "dtype"), odml.DType.float)
        self.assertEqual(len(vals), 3)
        self.assertEqual(vals, [4.4, 5.5, 6.6])

        '''
        # there seems to be a problem with float64 conversion in the nixpy lib
        file_name_2 = 'tmp' + str(uuid.uuid4())
        nix_path_2 = os.path.join(self.test_dir, file_name_2 + '.nix')
        nix_file_2 = nix.File.open(nix_path_2, nix.FileMode.Overwrite)
        odml_path_2 = os.path.join(self.test_dir, file_name_2 + '.xml')

        sec_2 = nix_file_2.create_section(name="section")

        prop2 = sec_2.create_property(name="string float property", values_or_dtype=np.float_)
        prop3.values = [7.7, 8.8, 9.9]
        setattr(prop3, "odml_type", nix.OdmlType("float"))

        convert.odmlwrite(nix_file_2, odml_path_2)
        odml_doc_2 = odml.load(odml_path_2)

        odml_prop_2 = odml_doc_2.sections[0].props[0]
        vals = odml_prop_2.values
        self.assertEqual(getattr(odml_prop_2, "dtype"), odml.DType.float)
        self.assertEqual(len(vals), 3)
        self.assertEqual(vals, [7.7, 8.8, 9.9])
        '''

    def test_nix_to_odml_double(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        nix_file = nix.File.open(nix_path, nix.FileMode.Overwrite)
        odml_path = os.path.join(self.test_dir, file_name + '.xml')

        sec = nix_file.create_section(name="section")
        prop = sec.create_property(name="double property", values_or_dtype=np.double)
        prop.values = [1.1, 2.2, 3.3]

        convert.odmlwrite(nix_file, odml_path)
        odml_doc = odml.load(odml_path)

        odml_prop = odml_doc.sections[0].props[0]
        vals = odml_prop.values
        self.assertEqual(getattr(odml_prop, "dtype"), odml.DType.float)
        self.assertEqual(len(vals), 3)
        self.assertEqual(vals, [1.1, 2.2, 3.3])
        
        '''
        # there seems to be a problem with float64 conversion in the nixpy lib
        prop2 = sec.create_property(name="double property 2", values_or_dtype=np.double)
        prop2.values = [4.4, 5.5, 6.6]
        setattr(prop2, "odml_type", nix.OdmlType("float"))

        convert.odmlwrite(nix_file, odml_path)
        odml_doc = odml.load(odml_path)

        odml_prop_2 = odml_doc.sections[0].props[1]
        vals = odml_prop_2.values
        self.assertEqual(getattr(odml_prop_2, "dtype"), odml.DType.float)
        self.assertEqual(len(vals), 3)
        self.assertEqual(vals, [4.4, 5.5, 6.6])
        '''

    def test_nix_to_odml_boolean(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        nix_file = nix.File.open(nix_path, nix.FileMode.Overwrite)
        odml_path = os.path.join(self.test_dir, file_name + '.xml')

        sec = nix_file.create_section(name="section")
        prop = sec.create_property(name="boolean property", values_or_dtype=np.bool_)
        prop.values = [True, False, True]

        convert.odmlwrite(nix_file, odml_path)
        odml_doc = odml.load(odml_path)

        odml_prop = odml_doc.sections[0].props[0]
        vals = odml_prop.values
        self.assertEqual(getattr(odml_prop, "dtype"), odml.DType.boolean)
        self.assertEqual(len(vals), 3)
        self.assertEqual(vals, [True, False, True])

        file_name_2 = 'tmp' + str(uuid.uuid4())
        nix_path_2 = os.path.join(self.test_dir, file_name_2 + '.nix')
        nix_file_2 = nix.File.open(nix_path_2, nix.FileMode.Overwrite)
        odml_path_2 = os.path.join(self.test_dir, file_name_2 + '.xml')

        sec_2 = nix_file_2.create_section(name="section")

        prop2 = sec_2.create_property(name="string boolean property", values_or_dtype=np.str_)
        prop2.values = ["True", "False", "TRUE", "FALSE"]

        convert.odmlwrite(nix_file_2, odml_path_2)
        odml_doc_2 = odml.load(odml_path_2)

        odml_prop_2 = odml_doc_2.sections[0].props[0]
        vals = odml_prop_2.values
        self.assertEqual(getattr(odml_prop_2, "dtype"), odml.DType.boolean)
        self.assertEqual(len(vals), 4)
        self.assertEqual(vals, [True, False, True, False])

        file_name_3 = 'tmp' + str(uuid.uuid4())
        nix_path_3 = os.path.join(self.test_dir, file_name_3 + '.nix')
        nix_file_3 = nix.File.open(nix_path_3, nix.FileMode.Overwrite)
        odml_path_3 = os.path.join(self.test_dir, file_name_3 + '.xml')

        sec_3 = nix_file_3.create_section(name="section")

        prop3 = sec_3.create_property(name="boolean property 3", values_or_dtype=np.bool_)
        prop3.values = [False, True, False]
        setattr(prop3, "odml_type", nix.OdmlType("boolean"))

        convert.odmlwrite(nix_file_3, odml_path_3)
        odml_doc_3 = odml.load(odml_path_3)

        odml_prop_3 = odml_doc_3.sections[0].props[0]
        vals = odml_prop_3.values
        self.assertEqual(getattr(odml_prop_3, "dtype"), odml.DType.boolean)
        self.assertEqual(len(vals), 3)
        self.assertEqual(vals, [False, True, False])

    def test_nix_to_odml_date(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        nix_file = nix.File.open(nix_path, nix.FileMode.Overwrite)
        odml_path = os.path.join(self.test_dir, file_name + '.xml')

        sec = nix_file.create_section(name="section")
        prop = sec.create_property(name="date property", values_or_dtype="date")
        prop.values = ['2011-11-01', '2011-12-02']

        convert.odmlwrite(nix_file, odml_path)
        odml_doc = odml.load(odml_path)

        odml_prop = odml_doc.sections[0].props[0]
        vals = odml_prop.values
        self.assertEqual(getattr(odml_prop, "dtype"), odml.DType.date)
        self.assertEqual(len(vals), 2)
        self.assertEqual(vals, [datetime.date(2011, 11, 1), datetime.date(2011, 12, 2)])

        file_name_2 = 'tmp' + str(uuid.uuid4())
        nix_path_2 = os.path.join(self.test_dir, file_name_2 + '.nix')
        nix_file_2 = nix.File.open(nix_path_2, nix.FileMode.Overwrite)
        odml_path_2 = os.path.join(self.test_dir, file_name_2 + '.xml')

        sec_2 = nix_file_2.create_section(name="section")

        prop2 = sec_2.create_property(name="date property 2", values_or_dtype=np.str_)
        prop2.values = ['2011-11-03', '2011-12-04']
        setattr(prop2, "odml_type", nix.OdmlType("date"))

        convert.odmlwrite(nix_file_2, odml_path_2)
        odml_doc_2 = odml.load(odml_path_2)

        odml_prop_2 = odml_doc_2.sections[0].props[0]
        vals = odml_prop_2.values
        self.assertEqual(getattr(odml_prop_2, "dtype"), odml.DType.date)
        self.assertEqual(len(vals), 2)
        self.assertEqual(vals, [datetime.date(2011, 11, 3), datetime.date(2011, 12, 4)])

    def test_nix_to_odml_time(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        nix_file = nix.File.open(nix_path, nix.FileMode.Overwrite)
        odml_path = os.path.join(self.test_dir, file_name + '.xml')

        sec = nix_file.create_section(name="section")
        prop = sec.create_property(name="time property", values_or_dtype="time")
        prop.values = ['11:11:11', '02:02:02']

        convert.odmlwrite(nix_file, odml_path)
        odml_doc = odml.load(odml_path)

        odml_prop = odml_doc.sections[0].props[0]
        vals = odml_prop.values
        self.assertEqual(getattr(odml_prop, "dtype"), odml.DType.time)
        self.assertEqual(len(vals), 2)
        self.assertEqual(vals, [datetime.time(11, 11, 11), datetime.time(2, 2, 2)])

        file_name_2 = 'tmp' + str(uuid.uuid4())
        nix_path_2 = os.path.join(self.test_dir, file_name_2 + '.nix')
        nix_file_2 = nix.File.open(nix_path_2, nix.FileMode.Overwrite)
        odml_path_2 = os.path.join(self.test_dir, file_name_2 + '.xml')

        sec_2 = nix_file_2.create_section(name="section")

        prop2 = sec_2.create_property(name="time property 2", values_or_dtype=np.str_)
        prop2.values = ['12:12:12', '03:03:03']
        setattr(prop2, "odml_type", nix.OdmlType("time"))

        convert.odmlwrite(nix_file_2, odml_path_2)
        odml_doc_2 = odml.load(odml_path_2)

        odml_prop_2 = odml_doc_2.sections[0].props[0]
        vals = odml_prop_2.values
        self.assertEqual(getattr(odml_prop_2, "dtype"), odml.DType.time)
        self.assertEqual(len(vals), 2)
        self.assertEqual(vals, [datetime.time(12, 12, 12), datetime.time(3, 3, 3)])

    def test_nix_to_odml_datetime(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        nix_file = nix.File.open(nix_path, nix.FileMode.Overwrite)
        odml_path = os.path.join(self.test_dir, file_name + '.xml')

        sec = nix_file.create_section(name="section")
        prop = sec.create_property(name="datetime property", values_or_dtype="datetime")
        prop.values = ['2011-11-01 11:11:11', '2012-12-02 02:02:02']

        convert.odmlwrite(nix_file, odml_path)
        odml_doc = odml.load(odml_path)

        odml_prop = odml_doc.sections[0].props[0]
        vals = odml_prop.values
        self.assertEqual(getattr(odml_prop, "dtype"), odml.DType.datetime)
        self.assertEqual(len(vals), 2)
        self.assertEqual(vals, [datetime.datetime(2011, 11, 1, 11, 11, 11),
                                datetime.datetime(2012, 12, 2, 2, 2, 2)])

        file_name_2 = 'tmp' + str(uuid.uuid4())
        nix_path_2 = os.path.join(self.test_dir, file_name_2 + '.nix')
        nix_file_2 = nix.File.open(nix_path_2, nix.FileMode.Overwrite)
        odml_path_2 = os.path.join(self.test_dir, file_name_2 + '.xml')

        sec_2 = nix_file_2.create_section(name="section")

        prop2 = sec_2.create_property(name="datetime property 2", values_or_dtype=np.str_)
        prop2.values = ['2012-12-02 12:12:12', '2013-01-01 01:01:01']
        setattr(prop2, "odml_type", nix.OdmlType("datetime"))

        convert.odmlwrite(nix_file_2, odml_path_2)
        odml_doc_2 = odml.load(odml_path_2)

        odml_prop_2 = odml_doc_2.sections[0].props[0]
        vals = odml_prop_2.values
        self.assertEqual(getattr(odml_prop_2, "dtype"), odml.DType.datetime)
        self.assertEqual(len(vals), 2)
        self.assertEqual(vals, [datetime.datetime(2012, 12, 2, 12, 12, 12),
                                datetime.datetime(2013, 1, 1, 1, 1, 1)])

    def test_nix_to_odml_text(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        nix_file = nix.File.open(nix_path, nix.FileMode.Overwrite)
        odml_path = os.path.join(self.test_dir, file_name + '.xml')

        sec = nix_file.create_section(name="section")
        prop = sec.create_property(name="text property", values_or_dtype=np.str_)
        prop.values = ['a\nb', 'c d', 'e\nix_path']

        convert.odmlwrite(nix_file, odml_path)
        odml_doc = odml.load(odml_path)

        odml_prop = odml_doc.sections[0].props[0]
        vals = odml_prop.values
        self.assertEqual(getattr(odml_prop, "dtype"), odml.DType.text)
        # this does currently not work as there seems to be a problem
        # in the odML core lib reading the file including a line break.
        # self.assertEqual(len(vals), 3)
        # self.assertEqual(vals, ['a\nb', 'c d', 'e\nix_path'])

    def test_nix_to_odml_tuple(self):
        file_name = 'tmp' + str(uuid.uuid4())
        nix_path = os.path.join(self.test_dir, file_name + '.nix')
        nix_file = nix.File.open(nix_path, nix.FileMode.Overwrite)
        odml_path = os.path.join(self.test_dir, file_name + '.xml')

        sec = nix_file.create_section(name="section")
        prop = sec.create_property(name="2-tuple property", values_or_dtype=np.str_)
        prop.values = ["(1; 2)", "(3; 4)"]

        convert.odmlwrite(nix_file, odml_path)
        odml_doc = odml.load(odml_path)

        odml_prop = odml_doc.sections[0].props[0]
        vals = odml_prop.values
        self.assertEqual(getattr(odml_prop, "dtype"), "2-tuple")
        self.assertEqual(len(vals), 2)
        self.assertEqual(vals, [["1", "2"], ["3", "4"]])

        file_name_2 = 'tmp' + str(uuid.uuid4())
        nix_path_2 = os.path.join(self.test_dir, file_name_2 + '.nix')
        nix_file_2 = nix.File.open(nix_path_2, nix.FileMode.Overwrite)
        odml_path_2 = os.path.join(self.test_dir, file_name_2 + '.xml')

        sec_2 = nix_file_2.create_section(name="section")

        prop2 = sec_2.create_property(name="3-tuple property", values_or_dtype=np.str_)
        prop2.values = ["(1; 2; 3)", "(4; 5; 6)"]

        convert.odmlwrite(nix_file_2, odml_path_2)
        odml_doc_2 = odml.load(odml_path_2)

        odml_prop_2 = odml_doc_2.sections[0].props[0]
        vals = odml_prop_2.values
        self.assertEqual(getattr(odml_prop_2, "dtype"), "3-tuple")
        self.assertEqual(len(vals), 2)
        self.assertEqual(vals, [["1", "2", "3"], ["4", "5", "6"]])
