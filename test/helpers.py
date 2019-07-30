import unittest
from unittest import mock


class TestCase(unittest.TestCase):
    def set_up_patch(self, topatch, themock=None, **kwargs):
        """
        Patch a function or class
        :param topatch: string The class to patch
        :param themock: optional object to use as mock
        :return: mocked object
        """
        if themock is None:
            themock = mock.Mock()

        if "return_value" in kwargs:
            themock.return_value = kwargs["return_value"]

        patcher = mock.patch(topatch, themock)
        self.addCleanup(patcher.stop)
        return patcher.start()
