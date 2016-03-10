"""This module contains all of the tesseract wrapping and image-to-text code.

Attributes:
    tesseract_dir_path (unicode): The path to the tesseract install directory.
    tesseract_stderr (file object): Where to pipe tesseract stderr stream. Defaults to
        sys.stdin. If None, errors are ignored.

"""
import difflib
import os
import sys
from unittest import TestCase, TestSuite, TextTestRunner
from PIL import Image
from piltesseract import get_text_from_image


#Tests fail if OCR doesn't meet this threshold of similarity
IMAGE_RATIO_THRESHOLD = 0.8


def get_test_image(image_name):
    """Gets the test image from the test folder.
    
    Returns:
        Image.Image: The PIL Image instance.

    """
    test_dir = 'tests'
    image_path = os.path.join(test_dir, image_name)
    assert os.path.exists(image_path)
    image = Image.open(image_path)
    return image


def get_similarity_ratio(parsed_text, actual_text):
    """Gets the difflib ratio of two sets of text.

    The ratio equation is:
    t = total characters of both strings combined
    m = total character matches in order
    ratio = m * 2 / t

    Args:
        parsed_text (str): The text parsed via ocr.
        actual_text (str): The true text contained in the image.

    Returns:
        float: the ratio.

    """
    s = difflib.SequenceMatcher(None, parsed_text, actual_text)
    ratio = s.ratio()
    return ratio


def check_similarity_ratio(parsed_text, actual_text, threshold_ratio=IMAGE_RATIO_THRESHOLD):
    """Checks if two images meet a similarity ratio.
    
    Gets the difflib ratio of two sets of text and checks against
    the threshold.

    The ratio equation is:
    t = total characters of both strings combined
    m = total character matches in order
    ratio = m * 2 / t

    Args:
        parsed_text (str): The text parsed via ocr.
        actual_text (str): The true text contained in the image.
        threshold_ratio (float): The threshold the ratio must be to return
            True.

    Returns:
        bool: Whether or not the similarity threshold ratio is met.

    """
    ratio = get_similarity_ratio(parsed_text, actual_text)
    return ratio >= threshold_ratio


class TesserTestCase(TestCase):
    def runTest(self):
        actual_text = "The quick brown fox jumps over the lazy dog"
        quick_fox_image = get_test_image('quickfox.png')
        text = get_text_from_image(quick_fox_image)
        assert isinstance(text, unicode)
        assert check_similarity_ratio(text, actual_text)
