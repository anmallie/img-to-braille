# brailleart.py
Python script to convert an image to copy and paste-able Braille Unicode, created by [anmallie](https://github.com/anmallie/).

## Dependencies & Installation

This script uses Python3 with the Pillow and NumPy libraries.

Commands given below for those who use `pip`, see each library's linked installation pages if needed

[Pillow](https://pillow.readthedocs.io/en/stable/installation.html)

    $ python3 -m pip install --upgrade pip
    $ python3 -m pip install --upgrade Pillow
    
[NumPy](https://numpy.org/install/)

    $ pip install numpy
    
 ## Usage
 
    $ python3 brailleart.py -i <image-file>
    
### Optional Arguments
* `-h                     display usage and options`
* `-o <output-file>       save the output to given file`
* `-p <pixels-per-dot>    lower number gives larger resolution Braille art (default=6)`
* `-t <threshold>         pixel value threshold (0-255)`

