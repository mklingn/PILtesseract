WANDtesseract
=======

Simple Tesseract wrapper for converting WAND Images to text.

**This is heavily based on [PILtesseract](https://github.com/Digirolamo/PILtesseract) by [Christopher Digirolamo](https://github.com/Digirolamo).**

I merely changed a few lines and the name.

**Warning:** WANDtesseract is intended to only work with tesseract 3.03+,
one awesome feature added in 3.03 is the ability to pipe images via stdin,
WANDtesseract utilizes this feature.

Here is a simple example:

    >>> from wand.image import Image
    >>> from wandtesseract import get_text_from_image
    >>> image = Image(filename='quickfox.png')
    >>> get_text_from_image(image)
    'The quick brown fox jumps over the lazy dog'

Requirements
------------
 - [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract): 3.03 or higher
   - First install either from source or from [binaries](https://github.com/tesseract-ocr/tesseract/wiki).
   - Ensure that the tesseract binary folder is on your [PATH](https://en.wikipedia.org/wiki/PATH_(variable)).
 - [WAND](http://wand.readthedocs.io/en/0.4.4/)
 - [Six](https://pythonhosted.org/six/)
   - ```$ pip install six```
 - python3 (I have not tested python2)

Install
------------
Global install:
 
    $ python3 setup.py

User install:

    $ python3 setup.py --user



