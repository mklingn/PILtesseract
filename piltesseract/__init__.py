"""The piltesseract package is a Tesseract-OCR command line wrapper.

piltesseract allows quick conversion of PIL Image.Image instances to text using
Tesseract-OCR.

Note:
    piltesseract uses stdin of tesseract to stream images to it. This only works
    in Tesseract-OCR version 3.03+.

Examples:
    >>> from piltesseract import get_text_from_image
    >>> image = Image.open("stop_sign.png")

    >>> print(get_text_from_image(stop_sign))
    'Stop'
    >>> print(get_text_from_image(stop_sign), psm=10)  #single character
    'S'

    Without a config file, you can set config variables using optional keywords.
    >>> text = get_text_from_image(
            stop_sign,
            tessedit_ocr_engine_mode=1,  #cube mode enum found in Tesseract-OCR docs
            cube_debug_level=1
            )

"""
import sys
from piltesseract.tesseractwrapper import get_text_from_image

__all__ = [get_text_from_image]
