"""Imports mock and it's commonly used libraries for use in testing."""
from unittest import TestCase

from mock import Mock, call, mock_open, patch
from webtest import TestApp

from app import application


__all__ = ('Mock', 'call', 'mock_open', 'patch')


class BaseTestCase(TestCase):
    app = TestApp(application)

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.addCleanup(patch.stopall)
