
Recipes
=======

Threading multiple images
-------------------------

Because most of the work is not completed in Python and is done via IO
and the tesseract binary, we can utilize threading.

.. code:: python

    from multiprocessing.pool import ThreadPool
    from piltesseract import get_text_from_image
    
    
    thread_pool = ThreadPool(10)
    
    
    def get_lines_from_images(image_list):
        """Gets text from a list of images.
    
        Uses threads to speed up the process
        
        Args:
            image_list (list[Image]): The list of images to use
                ocr on.
        
        Returns
            list[str]: The text from the images.
    
        """
        return thread_pool.map(get_text_from_image, image_list)
