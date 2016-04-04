
Advanced Example
================

In this example we will parse pypi version numbering from images.

| We will do some manual image preprocessing using PIL.
| You will need to have tesseract on your PATH and already done the
  ``pip install`` for both ``piltesseract`` and ``requests``.

.. code:: python

    # This cell is for imports and helper functions.
    
    import copy
    
    # For python 2/3 compatability.
    try:
        from StringIO import StringIO as BytesIO
    except ImportError:
        from io import BytesIO
        
    from PIL import Image, ImageFilter
    from piltesseract import get_text_from_image
    import requests
    
    
    def get_image_from_url(url):
        """Gets an image from a url string. 
            
        Args:
            url (str): The url to the image.
            
        Returns:
            Image: The image downloaded from the url.
        
        """
    
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        return image
    
    
    def scale_image_from_width(image, new_width):
        """Rescales an image based on a new width.
       
        Args:
            image (PIL.Image): The image to scale.
            new_width (int): The new width to scale to.
       
        Returns:
            PIL.Image: The new scaled image.
           
        """
        width, height = image.size
        if new_width == width:
             return copy.copy(image)
        width_percent = new_width / float(width)
        new_height = int(height * width_percent)
        new_size = (new_width, new_height)
        image = image.resize(new_size, Image.ANTIALIAS)
        return image

First, we download the pypi image that contains the version.

.. code:: python

    url = u'https://img.shields.io/pypi/v/piltesseract.png?branch=master'
    pypi_image = get_image_from_url(url)
    pypi_image




.. image:: output_4_0.png



Now we crop out the information we do not care about.

.. code:: python

    margin_crop = 1
    left_crop = 33
    
    width, height = pypi_image.size
    left = left_crop
    upper = margin_crop
    right = width - margin_crop
    lower = height - margin_crop
    crop_box = (left, upper, right, lower)
    
    version_image = pypi_image.crop(box=crop_box)
    version_image




.. image:: output_6_0.png



If we simply get the text at this point, the result will not be very
accurate. The size is smaller than desired and the white on orange does
not help.

.. code:: python

    text = get_text_from_image(version_image)
    text




.. parsed-literal::

    'van:'



Because we know versions are numbers + periods and a "v", we can use a
tesseract white list, the results are more accurate.

.. code:: python

    white_list = 'v0123456789.'
    text = get_text_from_image(version_image,
                              tessedit_char_whitelist=white_list)
    text




.. parsed-literal::

    'v002'



Although we can do better by manually changing the image. We should
scale and smooth the image.

.. code:: python

    width = 200
    preprocessed_image = scale_image_from_width(version_image, width)
    preprocessed_image = preprocessed_image.filter(ImageFilter.SMOOTH_MORE)
    preprocessed_image




.. image:: output_12_0.png



.. code:: python

    text = get_text_from_image(preprocessed_image)
    text




.. parsed-literal::

    'v0.0.2'



The new result is accurate! We can add on the white list for good
measure and reliability.

.. code:: python

    white_list = 'v0123456789.'
    text = get_text_from_image(preprocessed_image,
                              tessedit_char_whitelist=white_list)
    text




.. parsed-literal::

    'v0.0.2'


