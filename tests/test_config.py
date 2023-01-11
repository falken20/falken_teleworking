import unittest

from falken_teleworking import config

class TestConfig(unittest.TestCase):

    def test_get_settings(self):
        settings = config.get_settings()
        self.assertIsInstance(settings, config.Settings)
