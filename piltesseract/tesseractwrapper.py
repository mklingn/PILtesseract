"""This module contains all of the tesseract wrapping and image-to-text code.

Attributes:
    tesseract_dir_path (unicode): The path to the tesseract install directory.

"""
import os
import subprocess
import sys
from PIL import Image


#If tesseract binary is not on os.environ["PATH"] the put the path below.
tesseract_dir_path = ""


def get_text_from_image(image, stderr=None,
                        psm=3, lang="eng", tessdata_dir_path=None,
                        user_words_path=None, user_patterns_path=None,
                        config_name=None, **config_variables):
    """Uses tesseract to get single line from an image
    
    Outside of image and stderr, the arguments mirror the official 
    command line's usage. A list of the command line options can be found here:
    https://tesseract-ocr.googlecode.com/svn/trunk/doc/tesseract.1.html

    Args:
        image (Image.Image): The image to find text from.
        stderr (Optional[file]): The file like object (impliments `write`) 
            the tesseract stderr stream will write to. Defaults to None. 
            You can set it to sys.stdin to see all output easily.
        psm (Optional[int]): Page Segmentation Mode. Limits Tesseracts layout
            analysis (see the Tesseract docs). Default is 3, full analysis.
        lang (Optional[unicode]): The language to use. Default is 'eng' for
            English.
        tessdata_dir_path (Optional[unicode]): The path to the tessdata 
            directory.
        user_words_path (Optional[unicode]): The path to user words file.
        user_patterns_path (Optional[unicode]): The path to the user 
            patterns file.
        config_name (Optional[unicode]): The name of a config file.
        **config_variables: The config variables for tesseract.
            A list of config variables can be found here:
            http://www.sk-spell.sk.cx/tesseract-ocr-parameters-in-302-version

    Returns:
        unicode: The parsed text.

    Examples:
        Examples assume "image" is a picture of the text "ABC123". 
        See piltesseract tests for working code.

        >>> get_text_from_image(image)
        'ABC123'
        >>> get_text_from_image(image, psm=10)  #single character psm
        'A'

        You can use tesseract's default configs or your own:
        >>> get_text_from_image(image, config_name='digits')
        '13123'

        Without a config file, you can set config variables using optional keywords:
        >>> text = get_text_from_image(
                image,
                tessedit_char_whitelist='1'
                tessedit_ocr_engine_mode=1,  #cube mode enum found in Tesseract-OCR docs
                )
        '1  11 '

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
    if error and stderr is not None:
        stderr.write(error)
    text =  unicode(text, "utf-8", errors="ignore")
    text = text.rstrip(u'\r\n ')
    return text
