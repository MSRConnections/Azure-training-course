import matplotlib
matplotlib.use('AGG') # save png files
from pylab import *
import os.path

def graph(sheet = '', image_name = None, clear_image = True, **image_args):
    if not sheet:
        # use active sheet by default
        sheet = active_sheet()

    filepath = img_path() # get an unused filepath
    savefig(filepath, bbox_inches = 'tight') # store temp file
    x = all_images(sheet)

    if not image_name:
        # if no name is passed:
        # update the last image in x by default, or add an image if
        # there isn't one
        if x:
            img = x[-1]
            img.update(filepath)
        else:
            img = Image(filepath, name = image_name, sheet = sheet, **image_args)
    else:
        image_found = False
        for img in x:
            # update image with image_name if it's there; add a new
            # image if it's not
            if img.name == image_name:
                img.update(filepath)
                image_found = True
                break
        if not image_found:
            # add new image
            img = Image(filepath, name = image_name, sheet = sheet, **image_args)
    if clear_image:
        os.remove(filepath) # cleanup the file
    return img

def img_path():
    # gets a temp filepath for the image
    name = 'temp'
    filepath = os.getcwd() + '\\' + name + '.png'
    # check that filepath doesn't already exist
    while os.path.isfile(filepath):
        name += '1'
        filepath = os.getcwd() + '\\' + name + '.png'
    return filepath
    
def show(*args, **kwargs):
    raise NotImplementedError("show doesn't work in nitroplot; use 'graph'")
