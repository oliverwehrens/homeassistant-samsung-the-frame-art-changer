import os
import sys
import unittest
from unittest.mock import Mock


sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.utils import Utils


class ArtModeTests(unittest.TestCase):
    def test_art_mode_on_shows_image(self):
        art = Mock()
        art.get_artmode.return_value = 'on'

        self.assertTrue(Utils.is_art_mode_on(art))

    def test_watching_tv_does_not_show_image(self):
        art = Mock()
        art.get_artmode.return_value = 'off'

        self.assertFalse(Utils.is_art_mode_on(art))

    def test_unknown_art_mode_does_not_show_image(self):
        art = Mock()
        art.get_artmode.side_effect = Exception('timeout')

        with self.assertLogs(level='WARNING'):
            self.assertFalse(Utils.is_art_mode_on(art))


if __name__ == '__main__':
    unittest.main()
