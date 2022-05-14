from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import sys
import getopt

def main(argv):
    infile, outfile = None, None
    dot_size, threshold = 6, 127
    if len(argv) == 1:
        return usage(argv[0])
    try:
        opts, args = getopt.getopt(argv[1:], "hi:o:p:t:")
    except getopt.GetoptError:
        return usage(argv[0])
    for opt, arg in opts:
        if opt == '-h':
            return usage(argv[0])
        elif opt == '-i':
            infile = arg
        elif opt == '-o':
            outfile = arg
        elif opt == '-p':
            dot_size = int(arg)
        elif opt == '-t':
            threshold = int(arg)
            if threshold < 0 or threshold > 255:
                return print("Threshold must be between 0 and 255")
            
    if infile is None:
        print("You must specify an input file")
        return usage(argv[0])

    try:
        img = Image.open(infile)
    except FileNotFoundError:
        return print(f"File {infile} not found")
    except PIL.UnidentifiedImageError:
        return print(f"{infile} cannot be opened. Please specify a valid image file")


    # Greyscale the image and enhance edges
    img = img.convert('L')
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE).filter(ImageFilter.SHARPEN)
    
    # Create 2D np.array from image
    pixels = np.asarray(img)
    
    # Turn the image from greyscale to black and white
    pixels[pixels >= threshold] = 255
    pixels[pixels < threshold] = 0
    
    # Create an np.array representing each dot, ignoring leftover pixels on right and bottom
    width, height = len(pixels[0]) // dot_size, len(pixels) // dot_size
    if len(pixels[0]) - width*dot_size <= dot_size:
        width -= 1
    if len(pixels) - height*dot_size <= dot_size:
        height -= 1
    dots = np.zeros((height, width), dtype=int)

    # Get upper leftmost pixel of each dot, ignore any remaining pixels on right and bottom
    row_idxs = np.array([i*dot_size for i in range(height)])
    col_idxs = np.array([i*dot_size for i in range(width)])

    # Add value of pixel to its respective dot, 
    for y in range(dot_size):
        for x in range(dot_size):
            vals = pixels[:, col_idxs+x][row_idxs+y, :]
            dots += vals

    # If the average value of the pixels makes the threshold, that dot is shown
    raw_threshold = (threshold) * (dot_size ** 2)
    dots_shown = dots >= raw_threshold
    output = ''
    # Braille character is a 3x2 grid of dots
    for y in range(height//3):
        for x in range(width//2):
            shown, row, col = [], y*3, x*2
            shown = list(dots_shown[row:row+3, col])
            shown.extend(list(dots_shown[row:row+3, col+1]))
            output += get_braille(shown)
        output += '\n'

    if outfile is None:
        return print(output)

    try:
        with open(outfile, "w") as file:
            file.write(output)
    except:
        return print(f"Unable to create or write to {outfile}")
        

# Takes a boolean array representing a Braille character
def get_braille(shown: list):
    # Braille unicode U+2800 - U+283F
    code = 0x2800
    # represented as 6 bits, column by column with UL as LSB, BR as MSB
    offset = 0b000000
    shown.reverse()
    for dot in shown:
        offset = offset << 1
        offset = offset | 0b1 if dot else offset   # Set bit if dot is shown
        
    return chr(code + offset)
    
def usage(path):
    print(f"Usage: {path} [opts]")
    options = ["Options:",
               "-i <input_image>",
               "-o <output-file>",
               "-p <pixels-per-dot>",
               "-t <threshold>"]
    print("\n    ".join(options))
    

if __name__ == '__main__':
    argv = sys.argv
    main(argv)
