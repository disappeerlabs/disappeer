"""
test_gpgcontroller.py

Tests for GPG component widget controller
"""

import unittest
from unittest.mock import MagicMock, patch 
from disappeer.components.gpg import gpgcontroller, gpgframe, gpgmodel
import tkinter


class TestBasics(unittest.TestCase):

    def setUp(self):
        self.root = tkinter.Tk()
        self.mock_view = gpgframe.GPGFrame(MagicMock())
        self.mock_view.bind_home_dir_entry = MagicMock()
        self.mock_model = gpgmodel.GPGModel(args=MagicMock(), root=self.root, queue=MagicMock())
        self.x = gpgcontroller.GPGController(self.root, self.mock_view, self.mock_model)
    
    def test_instance(self):
        self.assertIsInstance(self.x, gpgcontroller.GPGController)
    
    def test_config_data_contex_adds_view_home_dir_observer_to_model(self):
        self.assertIn(self.mock_view.home_dir_entry_var, self.mock_model.home_dir_observable.observer_list)

    def test_view_home_dir_entry_bind_called(self):
        self.mock_view.bind_home_dir_entry.assert_called_with(self.x.button_release_1, self.x.home_dir_entry_clicked)

    def test_homedir_entry_clicked_attribute(self):
        name = 'home_dir_entry_clicked'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    @patch('tkinter.filedialog.askdirectory')
    def test_home_dir_entry_clicked_launches_ask_dir(self, mocked):
        self.x.home_dir_entry_clicked(None)
        self.assertTrue(mocked.called)

    @patch('tkinter.filedialog.askdirectory')
    def test_home_dir_entry_clicked_sets_home_dir_observable_on_dir_selection(self, mocked):
        val = '324yh5eg3'
        mocked.return_value = val
        self.x.home_dir_entry_clicked(None)
        self.assertEqual(self.x.model.home_dir_observable.get(), val)

    @patch('tkinter.filedialog.askdirectory')
    def test_home_dir_entry_clicked_does_not_set_home_dir_observable_on_cancel_dir_selection(self, mocked):
        before_val = self.x.model.home_dir_observable.get()
        mocked.return_value = ()
        self.x.home_dir_entry_clicked(None)
        self.assertEqual(self.x.model.home_dir_observable.get(), before_val)
