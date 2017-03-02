"""This module contains image-to-text tests and helper functions.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import difflib
import os
import sys
from unittest import TestCase, TestSuite, TextTestRunner
from wand.image import Image
import six
from piltesseract import get_text_from_image


#Tests fail if OCR doesn't meet this threshold of similarity
IMAGE_RATIO_THRESHOLD = 0.8


def get_test_image_path(image_name):
    """Gets the test image path from the test folder.
    
    Returns:
        str: The image path.

    """
    test_dir = "tests"
    image_path = os.path.join(test_dir, image_name)
    assert os.path.exists(image_path)
    return image_path


def get_test_image(image_name):
    """Gets the test image from the test folder.
    
    Returns:
        Image.Image: The PIL Image instance.

    """
    test_dir = "tests"
    image_path = get_test_image_path(image_name)
    image = Image(filename=image_path)
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
    def test_simple_sentence(self):
        actual_text = "The quick brown fox jumps over the lazy dog"
        quick_fox_image = get_test_image('quickfox.bmp')
        text = get_text_from_image(quick_fox_image)
        assert isinstance(text, six.text_type)
        assert check_similarity_ratio(text, actual_text)

    def test_simple_sentence_png(self):
        actual_text = "The quick brown fox jumps over the lazy dog"
        quick_fox_image = get_test_image('quickfox.png')
        text = get_text_from_image(quick_fox_image)
        assert isinstance(text, six.text_type)
        assert check_similarity_ratio(text, actual_text)

    def test_simple_sentence_from_file(self):
        actual_text = "The quick brown fox jumps over the lazy dog"
        image_path = get_test_image_path('quickfox.bmp')
        text = get_text_from_image(image_path)
        assert isinstance(text, six.text_type)
        assert check_similarity_ratio(text, actual_text)

    def test_options(self):
        quick_fox_image = get_test_image('quickfox.png')
        text = get_text_from_image(
            quick_fox_image, 
            psm=10  #single character
            )
        assert isinstance(text, six.text_type)
        assert len(text) == 1

    def test_configs(self):
        allowed_chars = "0123456789-"
        white_list_set = set(allowed_chars)
        alphanum_image = get_test_image('alphanumeric.png')
        #default with alphas
        text = get_text_from_image(alphanum_image)
        assert isinstance(text, six.text_type)
        assert not all(char in white_list_set for char in text if char != ' ')
        #digits config file
        text = get_text_from_image(alphanum_image, config_name='digits')
        assert isinstance(text, six.text_type)
        assert all(char in white_list_set for char in text if char != ' ')
        #manual config
        allowed_chars = "123"
        white_list_set = set(allowed_chars)
        text = get_text_from_image(
            alphanum_image,
            tessedit_char_whitelist=allowed_chars,
            )
        assert isinstance(text, six.text_type)
        assert all(char in white_list_set for char in text if char != ' ')
