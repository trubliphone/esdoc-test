####################
#   ES-DOC CIM Questionnaire
#   Copyright (c) 2017 ES-DOC. All rights reserved.
#
#   University of Colorado, Boulder
#   http://cires.colorado.edu/
#
#   This project is distributed according to the terms of the MIT license [http://www.opensource.org/licenses/MIT].
####################

"""
.. module:: test_utils

Tests for utilities
"""

from django.db import models
from django_fake_model import models as fake_models
from django.core.files.uploadedfile import SimpleUploadedFile

from Q.questionnaire import APP_LABEL
from Q.questionnaire.tests.test_base import TestQBase, incomplete_test
from Q.questionnaire.q_constants import *
from Q.questionnaire.q_fields import *


###############################
# some constants & helper fns #
###############################

UPLOAD_DIR = "tests"
UPLOAD_PATH = os.path.join(APP_LABEL, UPLOAD_DIR)  # this will be concatenated w/ MEDIA_ROOT by FileField


def get_file_path(file=None):
    if file:
        return os.path.join(settings.MEDIA_ROOT, UPLOAD_PATH, file.name)
    else:
        return os.path.join(settings.MEDIA_ROOT, UPLOAD_PATH)


###############################################
# a silly set of models to use w/ these tests #
###############################################

# these aren't _real_ models (they're not part of the app)
# but they still need to be included in the db for the tests to work
# I use django_fake_models to get around this
# (see the decorators on the actual test class below)

class TestFileFieldModel(fake_models.FakeModel):

    name = models.CharField(blank=True, max_length=BIG_STRING, unique=True)
    file = QFileField(blank=True, upload_to=UPLOAD_PATH)


class TestVersionFieldModel(fake_models.FakeModel):
    name = models.CharField(blank=True, max_length=BIG_STRING, unique=True)
    version = QVersionField(blank=True, null=True)


#########################
# the actual test class #
#########################

@TestFileFieldModel.fake_me
@TestVersionFieldModel.fake_me
class Test(TestQBase):

    def setUp(self):
        # make sure the UPLOAD_TO directory has been cleaned...
        self.test_file_dir = get_file_path()
        self.assertEqual(len(os.listdir(self.test_file_dir)), 0)

        # don't need questionnaire infrastructure...
        # super(Test, self).setUp()
        pass

    def tearDown(self):
        # clean the UPLOAD_TO directory...
        for test_file_name in os.listdir(self.test_file_dir):
            os.unlink(os.path.join(self.test_file_dir, test_file_name))
        self.assertEqual(len(os.listdir(self.test_file_dir)), 0)

        # don't need questionnaire infrastructure...
        # super(Test, self).tearDown()
        pass

    ##############
    # QFileField #
    ##############

    def test_qfilefield_creation(self):

        test_file_content = "test file"
        test_file = SimpleUploadedFile("test", test_file_content.encode())

        test_file_field_model = TestFileFieldModel(name="test", file=test_file)
        test_file_field_model.save()
        self.assertTrue(os.path.isfile(get_file_path(test_file)))

        test_file_field = test_file_field_model.file
        self.assertTrue(isinstance(test_file_field.storage, OverwriteStorage))
        self.assertEqual(test_file_field.field.help_text, QFileField.default_help_text)

    def test_qfilefield_deletion(self):

        # files should be deleted when no other class instances are using them

        test_file_content = "test file"
        test_file = SimpleUploadedFile("test", test_file_content.encode())

        test_file_field_model_1 = TestFileFieldModel(name="one", file=test_file)
        test_file_field_model_2 = TestFileFieldModel(name="two", file=test_file)

        test_file_field_model_1.save()
        test_file_field_model_2.save()
        self.assertTrue(os.path.isfile(get_file_path(test_file)))

        # deleting the 1st model shouldn't delete the file
        # (b/c the 2nd model is still using it)
        test_file_field_model_1.delete()
        self.assertTrue(os.path.isfile(get_file_path(test_file)))

        # deleting the 2nd model should delete the file
        # (b/c no other models are still using it)
        test_file_field_model_2.delete()
        self.assertFalse(os.path.isfile(get_file_path(test_file)))

    def test_overwrite_storage(self):

        # files w/ different names should co-exist
        # files w/ same names should be overwritten
        test_file_1_content = "test file one"
        test_file_2_content = "test file two"
        test_file_3_content = "test file three"
        test_file_1 = SimpleUploadedFile("same_name", test_file_1_content.encode())
        test_file_2 = SimpleUploadedFile("different_name", test_file_2_content.encode())
        test_file_3 = SimpleUploadedFile("same_name", test_file_3_content.encode())

        # begin w/ an empty directory...
        test_file_dir = get_file_path()
        self.assertEqual(len(os.listdir(test_file_dir)), 0)
        test_file_field_model = TestFileFieldModel()

        # assign test_file_1;
        # the file should be copied to the correct path
        test_file_field_model.file = test_file_1
        test_file_field_model.save()
        self.assertTrue(os.path.isfile(get_file_path(test_file_1)))
        self.assertEqual(len(os.listdir(test_file_dir)), 1)
        self.assertEqual(test_file_field_model.file.read(), test_file_1_content.encode())

        # assign test_file_2;
        # the file should be copied to the correct path
        # but the previous file should still exist
        test_file_field_model.file = test_file_2
        test_file_field_model.save()
        self.assertTrue(os.path.isfile(get_file_path(test_file_2)))
        self.assertEqual(len(os.listdir(test_file_dir)), 2)
        self.assertEqual(test_file_field_model.file.read(), test_file_2_content.encode())

        # assign test_file_3;
        # the file should be copied to the correct path
        # and should replace the existing file w/ the same name
        test_file_field_model.file = test_file_3
        test_file_field_model.save()
        self.assertTrue(os.path.isfile(get_file_path(test_file_3)))
        self.assertEqual(len(os.listdir(test_file_dir)), 2)
        self.assertEqual(test_file_field_model.file.read(), test_file_3_content.encode())

    #################
    # QVersionField #
    #################

    def test_version_field(self):

        test_version_field_model = TestVersionFieldModel(name="test")
        test_version_field_model.version = "1.5"
        test_version_field_model.save()
        test_version_field_model.refresh_from_db()

        self.assertEqual(test_version_field_model.version.string, "1.5.0")
        self.assertEqual(test_version_field_model.version.major(), 1)
        self.assertEqual(test_version_field_model.version.minor(), 5)
        self.assertEqual(test_version_field_model.version.patch(), 0)
        self.assertTrue(test_version_field_model.version == "1.5")
        self.assertTrue(test_version_field_model.version > "0.5")
        self.assertTrue(test_version_field_model.version >= "1.5")
        self.assertTrue(test_version_field_model.version < "1.50")
        self.assertTrue(test_version_field_model.version <= "2.5")

        with self.assertRaises(ValueError):
            test_version_field_model.version = "not a version"
            test_version_field_model.save()

        with self.assertRaises(NotImplementedError):
            test_version_field_model.version = "1.2.3.4"
            test_version_field_model.save()

    def test_version_field_contribute_to_class(self):
        test_version_field_model = TestVersionFieldModel(name="test")
        test_version_field_model.version = "1.2.3"
        test_version_field_model.save()
        test_version_field_model.refresh_from_db()

        major = test_version_field_model.get_version_major()
        self.assertEqual(major, 1)

        minor = test_version_field_model.get_version_minor()
        self.assertEqual(minor, 2)

        patch = test_version_field_model.get_version_patch()
        self.assertEqual(patch, 3)

    def test_version_field_underspecified(self):
        test_version_field_model = TestVersionFieldModel(name="test")
        test_version_field_model.version = "1.2"
        test_version_field_model.save()
        test_version_field_model.refresh_from_db()

        fully_specified_version = Version("1.2.0")
        self.assertEqual(fully_specified_version, test_version_field_model.version)

        patch = test_version_field_model.get_version_patch()
        self.assertEqual(patch, 0)
