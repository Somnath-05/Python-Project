import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import main


class GameFlowTests(unittest.TestCase):
    def test_main_menu_exit(self):
        responses = iter(['5'])
        with unittest.mock.patch('builtins.input', side_effect=lambda *args: next(responses, '5')):
            main.main()

    def test_character_selection_uses_existing_keys(self):
        import characters
        char = characters.choose_character()
        self.assertIn('key', char)


if __name__ == '__main__':
    unittest.main()
