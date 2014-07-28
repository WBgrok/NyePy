#! /usr/bin/python

###########################
# TODO
# Sort out whitespace

print "############################################################################"
print "###  INITIALISATION SEQUENCE"
import picamera
print "INIT:: picamera package import successful"
import io
print "INIT:: io package import successful"
import pygame
import pygame.image
from pygame.locals import *
print "INIT:: pygame packages import successful"
from PIL import Image
print "INIT:: PIL Image package import successful"
from time import sleep
print "INIT:: time package import successsful"
import resource
print "INIT:: resource package import successful"


## CONSTANTS
# NB "Screen" in this code means "active display area".
# This might be smaller than the resolution of the display device

FULL_SCREEN = False
SHOW_LOAD = True
FONT_SIZE = 40
FONT_SPACING = 0.75
TEXT_TRANSPARENCY = 0
TEXT_COLOUR = (0,200,0)

SC_WIDTH  = 640  ## Screen width
SC_HEIGHT = 480  ## Screen height
MIX_FAC   = 0.30 ## Mix factor
WAIT      = 5   ## wait duration in seconds
print "INIT:: display resolution " + str(SC_WIDTH) + "x" + str(SC_HEIGHT)

QUADRANTS = 1    ## 1 is a single image, 2 is 4 quadrants, 3 is 9. etc/
print "INIT:: displaying " + str(QUADRANTS) + " by " + str(QUADRANTS)
## Initialisation

## Globals

img_w = SC_WIDTH / QUADRANTS
img_h = SC_HEIGHT / QUADRANTS
img_size = (img_w, img_h)

N_LINES = int(img_h / (FONT_SPACING * FONT_SIZE)) # number of lines of text displayed per iteration
print "INIT:: line count = " + str(N_LINES)
# Quadrant iterators
quad_i = 0
quad_j = 0 

# Camera stuff
camera = picamera.PiCamera()
print "INIT:: piCamera initialised"
camera.resolution = (img_w,img_h)
print "INIT:: cam resolution " + str(img_w) + "x" + str(img_h)

# pygame init for screen handling
pygame.init()
pygame.mouse.set_visible(False)
print "INIT:: pygame package initialised"
sc_size = (SC_WIDTH,SC_HEIGHT)
screen = pygame.display.set_mode(sc_size)
print "INIT:: screen initialised at  " + str(SC_WIDTH) + "x" + str(SC_HEIGHT) 

# Handling full screen
# we get the flags and bits from the windowed screens, and pass them back
tmp = pygame.display.get_surface()
flags = tmp.get_flags()
bits = tmp.get_bitsize()

## UNCOMMENT BELOW FOR FULL SCREEN
if FULL_SCREEN:
    pygame.display.set_mode(sc_size,flags^FULLSCREEN,bits)
    print "INIT:: switching to full screen"


def test_disp():
    "Call this to test display"
    import random
    rr = random.randrange
    screen.fill((rr(0,256),rr(0,256),rr(0,256)),(rr(0,SC_WIDTH),rr(0,SC_HEIGHT),32,32))

def get_img():
    "Returns a PIL image from picamera"
    stream = io.BytesIO()
    camera.capture(stream, format="jpeg")
#    print "CAPTURE:: captured steam"
    stream.seek(0)
    return Image.open(stream)

def make_pigame_img(pil_image):
    "returns a pigame image from a PIL image"
    mode = pil_image.mode
    size = pil_image.size
    data = pil_image.tostring()
#    print "CONVERT:: converted to PIL, in mode " + str(mode) + " and size " + str(size)
    return pygame.image.fromstring(data,size,mode)

def blend(old, new):
    return Image.blend(old,new , MIX_FAC)

def graceful_exit():
    # if we're here, we're quitting the program.
    print ""
    print "############################################################################"
    print ""
    print "####################### SHUTDOWN COMPLETE ##################################"
    print ""
    print "############################################################################"
    pygame.display.quit()
    pygame.quit()
    exit(0)


# new image object for our working image 
current_image = get_img()
print "INIT:: Captured first image"

# our working pigame display buffer
# initialised as the current image
disp = make_pigame_img(current_image)
print "INIT:: display buffer initialised"

# first image
screen.blit(disp,(0,0))
pygame.display.flip()
print "INIT:: first image up"
working_image = current_image.copy()

basicfont = pygame.font.SysFont(None,FONT_SIZE)
print "INIT:: font initialised"

print "###  INITIALISATION COMPLETE"
print "############################################################################"

# get load stats
mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
ucpu = resource.getrusage(resource.RUSAGE_SELF).ru_utime
scpu = resource.getrusage(resource.RUSAGE_SELF).ru_stime


print "###  INITIALISATION COMPLETE"
print "###  LOAD: " + str(ucpu) + " - " + str(scpu) + " - " + str(mem)
print "############################################################################"

# Main Loop
if __name__ == "__main__":
    _quit = False
    while not _quit:
        print "###  LOAD: " + str(ucpu) + " - " + str(scpu) + " - " + str(mem)
        sleep(1)
        # Handle interrupts (esc to quit)
        for e in pygame.event.get():
            if e.type is QUIT: _quit = True
            if e.type is KEYDOWN and e.key == K_ESCAPE: _quit = True
         

        # average and display the image
        current_image = get_img()
        working_image = blend(working_image, current_image)
        disp = make_pigame_img(working_image)
        screen.blit(disp,(quad_i * img_w ,quad_j * img_h))
        sleep(WAIT)

        # get load stats
        if (SHOW_LOAD):
            mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
	    ucpu = resource.getrusage(resource.RUSAGE_SELF).ru_utime
            scpu = resource.getrusage(resource.RUSAGE_SELF).ru_stime
	    stats = str(ucpu) + " - " + str(scpu) + " - " + str(mem)
	    stext = basicfont.render(stats,False, TEXT_COLOUR)
	    screen.blit(stext,(0,SC_HEIGHT - FONT_SIZE))

        # Render the buffer to screen
        pygame.display.flip()

        #move to the next quadrant
        quad_i += 1
        if quad_i == QUADRANTS:
            quad_i = 0
            quad_j += 1
            if quad_j == QUADRANTS:
                quad_j = 0
graceful_exit()
