"""This module contains all of the tesseract wrapping and image-to-text code.

Attributes:
    tesseract_dir_path (unicode): The path to the tesseract install directory.
    tesseract_stderr (file object): Where to pipe tesseract stderr stream. Defaults to
        sys.stdin. If None, errors are ignored.

"""
import os
import subprocess
import sys
from PIL import Image


#If tesseract binary is not on os.environ["PATH"] the put the path below.
tesseract_dir_path = ""
tesseract_stderr = sys.stdout


def get_text_from_image(image, psm=3, lang="eng", tessdata_dir_path=None,
                        user_words_path=None, user_patterns_path=None,
                        config_name=None, **config_variables):
    """Uses tesseract to get single line from an image
    
    The arguments mirror the official command line's usage. A list of
    the command line options can be found here:
    https://tesseract-ocr.googlecode.com/svn/trunk/doc/tesseract.1.html

    Args:
        image (Image.Image): The image to find text from.
        psm (int): Page Segmentation Mode. Limits Tesseracts layout
            analysis (see the Tesseract docs). Default is full page analysis.
        lang (unicode): The language to use. Default is English.
        tessdata_dir_path (unicode): The path to the tessdata directory.
        user_words_path (unicode): The path to user words file.
        user_patterns_path (unicode): The path to the user patterns file.
        config_name (unicode): The name of a config file.
        **config_variables: The config variables for tesseract.
            A list of config variables can be found here:
            http://www.sk-spell.sk.cx/tesseract-ocr-parameters-in-302-version

    Returns:
        unicode: The parsed text.

    Examples:
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
    if not isinstance(image, Image.Image):
        raise ValueError("image must be of type Image, not {}."
                         "".format(type(image)))
    #process environment variables
    bin_path = 'tesseract'
    tess_cwd = None
    tess_env = None
    if tesseract_dir_path:
        bin_path = os.path.join(tesseract_dir_path, 'tesseract')
        tess_cwd = tesseract_dir_path
        tess_env = {'path': tesseract_dir_path}
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
    #So console window does not popup
    console_startup_info = subprocess.STARTUPINFO()
    console_startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    console_startup_info.wShowWindow = subprocess.SW_HIDE
    pipe = subprocess.Popen(
        command,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        cwd=tess_cwd,
        env=tess_env,
        startupinfo=console_startup_info,
        )
    image.save(pipe.stdin, format='bmp')
    pipe.stdin.close()
    text = pipe.stdout.read()
    error = pipe.stderr.read()
    if error and tesseract_stderr is not None:
        tesseract_stderr.write(error)
    text =  unicode(text, "utf-8", errors="ignore")
    return text
