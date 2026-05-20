"""
Unit tests for the memory reader module.
Uses mocking to simulate process memory.
"""

import unittest
from unittest.mock import MagicMock, patch
from src.memory_reader import BD2MemoryReader


class TestBD2MemoryReader(unittest.TestCase):
    """Test cases for BD2MemoryReader."""

    def setUp(self):
        """Set up test fixtures."""
        self.reader = BD2MemoryReader()

        # Mock pymem
        self.mock_pm = MagicMock()
        self.mock_pm.process_handle = 12345
        self.reader.pm = self.mock_pm

        # Mock process info
        self.mock_process = MagicMock()
        self.mock_process.lpBaseOfDll = 0x400000
        self.reader.process = self.mock_process
        self.reader.base_address = 0x400000

    def test_attach_success(self):
        """Test successful process attachment."""
        with patch("pymem.Pymem") as mock_pymem, \
             patch("pymem.process.module_from_name") as mock_module:
            mock_pymem.return_value = self.mock_pm
            mock_module.return_value = self.mock_process

            result = BD2MemoryReader().attach()
            self.assertTrue(result)

    def test_attach_failure(self):
        """Test failed process attachment."""
        with patch("pymem.Pymem", side_effect=Exception("Process not found")):
            reader = BD2MemoryReader()
            result = reader.attach()
            self.assertFalse(result)

    def test_read_int(self):
        """Test reading integer from memory."""
        self.mock_pm.read_int.return_value = 42
        result = self.reader.read_int(0x400000)
        self.assertEqual(result, 42)
        self.mock_pm.read_int.assert_called_once_with(0x400000)

    def test_write_int(self):
        """Test writing integer to memory."""
        self.reader.write_int(0x400000, 100)
        self.mock_pm.write_int.assert_called_once_with(0x400000, 100)

    def test_read_float(self):
        """Test reading float from memory."""
        self.mock_pm.read_float.return_value = 3.14
        result = self.reader.read_float(0x400000)
        self.assertAlmostEqual(result, 3.14)
        self.mock_pm.read_float.assert_called_once_with(0x400000)

    def test_write_float(self):
        """Test writing float to memory."""
        self.reader.write_float(0x400000, 2.71)
        self.mock_pm.write_float.assert_called_once_with(0x400000, 2.71)

    def test_get_gold(self):
        """Test retrieving gold value."""
        self.mock_pm.read_int.return_value = 5000
        gold = self.reader.get_gold()
        expected_addr = 0x400000 + BD2MemoryReader.GOLD_OFFSET
        self.assertEqual(gold, 5000)
        self.mock_pm.read_int.assert_called_with(expected_addr)

    def test_set_gold(self):
        """Test setting gold value."""
        self.reader.set_gold(99999)
        expected_addr = 0x400000 + BD2MemoryReader.GOLD_OFFSET
        self.mock_pm.write_int.assert_called_with(expected_addr, 99999)

    def test_set_level(self):
        """Test setting level."""
        self.reader.set_level(99)
        expected_addr = 0x400000 + BD2MemoryReader.LEVEL_OFFSET
        self.mock_pm.write_int.assert_called_with(expected_addr, 99)

    def test_set_job_points(self):
        """Test setting job points."""
        self.reader.set_job_points(9999)
        expected_addr = 0x400000 + BD2MemoryReader.JOB_POINTS_OFFSET
        self.mock_pm.write_int.assert_called_with(expected_addr, 9999)

    def test_detach(self):
        """Test detaching from process."""
        self.reader.detach()
        self.assertIsNone(self.reader.pm)
        self.assertIsNone(self.reader.process)
        self.assertIsNone(self.reader.base_address)
        self.mock_pm.close_process.assert_called_once()

    def test_read_int_no_attach(self):
        """Test read_int raises error when not attached."""
        reader = BD2MemoryReader()
        with self.assertRaises(RuntimeError):
            reader.read_int(0)

    def test_write_int_no_attach(self):
        """Test write_int raises error when not attached."""
        reader = BD2MemoryReader()
        with self.assertRaises(RuntimeError):
            reader.write_int(0, 0)


if __name__ == "__main__":
    unittest.main()
