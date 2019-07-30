from test.helpers import TestCase


class TestLineinfile(TestCase):
    def setUp(self):
        self.mock_open = self.set_up_patch('src.main.src')

    def test_lineinfile_adds_line_to_end_of_file_by_default(self):
        pass
