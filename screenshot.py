from PIL import ImageGrab
im = ImageGrab.grabclipboard()
im.save('images/maze2.png','PNG')