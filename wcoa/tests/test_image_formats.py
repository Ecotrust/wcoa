import unittest
from wagtail.images.formats import Format, unregister_image_format

class ImageFormatsTestCase(unittest.TestCase):
    def test_register_image_formats(self):
        # Check if the image formats are registered correctly
        self.assertIsNone(Format.get_format("square-small"))
        self.assertIsNone(Format.get_format("square-medium"))
        self.assertIsNone(Format.get_format("square-large"))
        self.assertIsNone(Format.get_format("square-xl"))
        self.assertIsNone(Format.get_format("square-original"))

    # def test_unregister_image_format(self):
        # Check if unregistering an image format works correctly
        # unregister_image_format("square-382")
        # self.assertEqual(len(Format.get_all_formats()), 9)
        # self.assertIsNone(Format.get_format("square-382"))

if __name__ == '__main__':
    unittest.main()