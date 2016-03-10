"""The piltesseract module is a Tesseract-OCR wrapper.

This module allows quick conversion of PIL Image.Image instances to text using
Tesseract-OCR.

Note:
    This module uses stdin of tesseract to stream images to it. This only works
    in Tesseract-OCR version 3.03+.

Examples:
    >>> from piltesseract import get_text_from_image
    >>> image = Image.open("stop_sign.png"
    >>> print(get_text_from_image(stop_sign))
    'Stop'
    >>> print(get_text_from_image(stop_sign), psm=10)  #single character
    'S'

Attributes:
    tesseract_dir_path (unicode): The path to the tesseract install directory.
    tesseract_stderr (): Where to pipe tesseract stderr stream. Defaults to
        sys.stdin. If None, errors are ignored.

"""
import os
import subprocess
import sys
from PIL import Image

#If tesseract binary is not on os.environ["PATH"] the put the path below.
tesseract_dir_path = ""
tesseract_stderr = sys.stdout


#variables for finding and setting up the paths for the tesseract binary
_tesseract_bin_path = 'tesseract'
_tess_cwd = None
_tess_env = None
if tesseract_dir_path:
    _tesseract_bin_path = os.path.join(tesseract_dir_path, 'tesseract')
    _tess_cwd = tesseract_dir_path
    _tess_env = {'path': tesseract_dir_path}
#So console window does not popup
_console_startup_info = subprocess.STARTUPINFO()
_console_startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
_console_startup_info.wShowWindow = subprocess.SW_HIDE


def get_text_from_image(image, psm=3, lang="eng", tessdata_dir_path=None,
                        user_words_path=None, user_patterns_path=None,
                        config_name=None, **config_variables):
    """Uses tesseract to get single line from an image
    
    The arguments mirror the official command line's usage. See
    https://tesseract-ocr.googlecode.com/svn/trunk/doc/tesseract.1.html

    Args:
        image (Image.Image): The image to find text from.
        psm (int): Page Segmentation Mode. Limits Tesseracts layout
            analysis (see the Tesseract docs). Default is full page analysis.
        lang (unicode): The language to use. Default is English.
        tessdata_dir_path (unicode): The path to the tessdata directory.
        user_words_path (unicode): The path to user words file.
        user_patterns_path (unicode): The path to the user patterns file.
        **config_variables: The config variables for tesseract.

    Returns:
        unicode: The parsed text.

    """
    if not isinstance(image, Image.Image):
        raise ValueError("image must be of type Image, not {}."
                         "".format(type(image)))
    bin_path = _tesseract_bin_path
    image_input = "stdin"
    commands = ["{} {} stdout -psm {} -l {}".format(bin_path, image_input, psm, lang)]
    if tessdata_dir_path is not None:
        commands.append('--tessdata-dir"{}"'.format(tessdata_dir_path))
    if user_words_path is not None:
        commands.append('--user-words"{}"'.format(user_words_path))
    if user_patterns_path is not None:
        commands.append('--user-patterns"{}"'.format(user_patterns_path))
    for config_var, value in config_variables.items():
        commands.append('-c {}={}'.format(config_var, value))
    if config_name is not None:
        commands.append(config_name)
    command = ' '.join(commands)
    pipe = subprocess.Popen(
        command,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        cwd=_tess_cwd,
        env=_tess_env,
        startupinfo=_console_startup_info,
        )
    image.save(pipe.stdin, format='bmp')
    pipe.stdin.close()
    text = pipe.stdout.read()
    error = pipe.stderr.read()
    if error and tesseract_stderr is not None:
        tesseract_stderr.write(error)
    text =  unicode(text, "utf-8", errors="ignore")
    return text
