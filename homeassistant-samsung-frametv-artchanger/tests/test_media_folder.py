from pathlib import Path
import os
import sys
import tempfile
import unittest


sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sources import media_folder


class MediaFolderTests(unittest.TestCase):
    def test_generated_preview_is_not_used_as_a_source(self):
        original_path = media_folder.folder_path
        try:
            with tempfile.TemporaryDirectory() as temp_directory:
                media_folder.folder_path = temp_directory
                Path(temp_directory, 'art.JPG').touch()
                Path(temp_directory, 'latest.jpg').touch()
                Path(temp_directory, 'uploaded_files.json').touch()

                self.assertEqual(
                    media_folder.get_media_folder_images(),
                    [str(Path(temp_directory, 'art.JPG'))],
                )
        finally:
            media_folder.folder_path = original_path

    def test_staged_file_is_selected_even_after_it_was_sent(self):
        original_path = media_folder.folder_path
        try:
            with tempfile.TemporaryDirectory() as temp_directory:
                media_folder.folder_path = temp_directory
                Path(temp_directory, 'other.jpg').touch()
                Path(temp_directory, 'selected_frame_art.jpg').touch()

                self.assertEqual(
                    media_folder.get_image_url(None, {'selected_frame_art.jpg'}),
                    'selected_frame_art.jpg',
                )
        finally:
            media_folder.folder_path = original_path

    def test_only_staged_file_skips_upload_cache(self):
        self.assertTrue(media_folder.skip_upload_cache('selected_frame_art.jpg'))
        self.assertFalse(media_folder.skip_upload_cache('other.jpg'))

    def test_previously_sent_images_are_not_selected(self):
        original_path = media_folder.folder_path
        try:
            with tempfile.TemporaryDirectory() as temp_directory:
                media_folder.folder_path = temp_directory
                Path(temp_directory, 'sent.jpg').touch()
                Path(temp_directory, 'new.jpg').touch()

                self.assertEqual(
                    media_folder.get_image_url(None, {'sent.jpg'}),
                    'new.jpg',
                )
                self.assertIsNone(
                    media_folder.get_image_url(None, {'sent.jpg', 'new.jpg'}),
                )
        finally:
            media_folder.folder_path = original_path

    def test_nested_images_use_a_stable_relative_path(self):
        original_path = media_folder.folder_path
        try:
            with tempfile.TemporaryDirectory() as temp_directory:
                media_folder.folder_path = temp_directory
                nested_directory = Path(temp_directory, 'museum')
                nested_directory.mkdir()
                Path(nested_directory, 'art.png').touch()

                self.assertEqual(
                    media_folder.get_image_url(None),
                    'museum/art.png',
                )
        finally:
            media_folder.folder_path = original_path


if __name__ == '__main__':
    unittest.main()
