Installation
====================
Installing PILtesseract is very simple, but before installing it, 
you should make sure you install the requirements.

Tesseract-OCR
------------
PILtesseract call the Tesseract-OCR command line tool, the tool
must be installed and on your PATH variable before using PILtesseract.

*Make sure you install version 3.03 or higher.*

 - Install either:  
 
   -  `from source`_  
     .. _`from source`: https://github.com/tesseract-ocr/tesseract 
	 
   -  `from binaries`_  
     .. _`from binaries`: https://github.com/tesseract-ocr/tesseract/wiki 
	 
      - Windows users may have to download from third-party installers like `UB Mannheim`_  
	  .. _`UB Mannheim`: https://github.com/UB-Mannheim/tesseract/wiki).
	  
 - Ensure that the tesseract binary folder is on your PATH_.
  .. _PATH: https://en.wikipedia.org/wiki/PATH_(variable)
 
 
Pillow
------------
The fork of the Python Image Library ("PIL")

 - Pillow_
  .. _Pillow: https://pillow.readthedocs.org/en/latest/ 
   
   - ``$ pip install Pillow``

*Note* The Pillow library installs as PIL, so you import it like:
``import PIL``
   
   
Six
------------
Library for python 2 and 3 compatibility

 - Six_
  .. _Six: https://pythonhosted.org/six/

   - ``$ pip install six``

   
PILtesseract
------------
Finally you can now install this library.

 - Installing from pip:
   - ``$ pip install piltesseract``
