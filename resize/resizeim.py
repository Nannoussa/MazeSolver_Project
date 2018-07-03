import os, sys
from PIL import Image
from resizeimage import resizeimage

basewidth = 800

for infile in sys.argv[1:]:
    outfile = os.path.splitext(infile)[0] + ".jpeg"
    if infile != outfile:
        try:
            img = Image.open(infile)
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            img.save(outfile)
            print ("image to %s" % (str(img.size)))
        except IOError:
            print ("cannot create thumbnail for '%s'" % infile)