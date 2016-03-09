import time
import unicornhat as unicorn

def set_light(check, x, y):
    # print "%s: %s, %d/%d" % (check.name, check.status, x, y)
    if check.status:
        unicorn.set_pixel(x, y, 0, 175, 0)
    else:
        unicorn.set_pixel(x, y, 175, 0, 0)
        if len(check.children) > 0:
            for child in check.children:
                set_light(child, x, y+1)

def set_lights(status):
    x = 7
    for check in status.checks:
        set_light(check, x, 0)
        x -= 1
    unicorn.show()

# This class controls the actual light modes
def fade(self):
    print "this function fades an LED"

def fade_column(self):
    print "this function fades a column"

def fade_row(self):
    print "this function fades a row"

def blink(self):
    print "this function blinks an LED"

def equalizer(self):
    print "this function fades out columns like an equalizer"

def diagonal(self):
    print "this function will wipe the screen diagonally"

def wipe(self):
    print "this function will wipe the screen horizontally"

def spiral(self):
    print "this function will show a spiral"

def random_out(self):
    print "this function will clear the screen at random"

def rainfall(self):
    print "this function will fill the screen like the matrix"

def column_single_row(x, on):
    for y in range(8):
        unicorn.set_pixel(x, y, 0, 0, 0)
    unicorn.set_pixel(x, on, 100, 0, 100)
    unicorn.show()

def blink_spread(self):
    print "this function will blink the center and then fill in"

