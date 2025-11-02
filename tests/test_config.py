"""
Tests for configuration module.
"""

import unittest
import os
from src.config import Config, config


class TestConfig(unittest.TestCase):
    """
    Test cases for configuration.
    """
    
    def test_config_defaults(self):
        """
        Test configuration default values.
        """
        self.assertEqual(Config.APP_NAME, 'FlowForge')
        self.assertEqual(Config.PORT, 8000)
    
    def test_config_validation(self):
        """
        Test configuration validation.
        """
        self.assertTrue(Config.validate())
    
    def test_config_instance(self):
        """
        Test global config instance.
        """
        self.assertIsNotNone(config)
        self.assertIsInstance(config, Config)


if __name__ == '__main__':
    unittest.main()

