import time
import unicornhat as unicorn

# TODO: define a 'colour' class?
# should have arithmetic values.

def setpixel(x, y, c, show=False):
    if len(c) != 3:
        raise Exception
    unicorn.set_pixel(x, y, c[0], c[1], c[2])
    if show:
        unicorn.show()

def set_row(x, c):
    if len(c) != 3:
        raise Exception
    for y in range(8):
        unicorn.set_pixel(x, y, c[0],c[1],c[2])
    unicorn.show()

def set_light(check, x, y):
    if check.status:
        unicorn.set_pixel(x, y, 0, 175, 0)
        # Clear the rest of the row/column
        for p in range(8)[y+1:]:
            unicorn.set_pixel(x, p, 0, 0, 0)
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

def fade_in(x,y):
    colour = 0
    while colour < 150:
        setpixel(x, y, (0, colour, 0), True)
        time.sleep(0.05)
        colour += 5

def fade_ins(xs,ys):
    colour = 0
    while colour < 150:
        for (x,y) in zip(xs,ys):
            setpixel(x, y, (0, colour, 0))
        unicorn.show()
        time.sleep(0.05)
        colour += 5

def fade_out(x,y):
    colour = 150
    while colour > 0:
        setpixel(x, y, (0, colour, 0), True)
        time.sleep(0.05)
        colour -= 5

def fade_outs(xs,ys):
    colour = 150
    while colour > 0:
        for (x,y) in zip(xs,ys):
            setpixel(x, y, (0, colour, 0))
        unicorn.show()
        time.sleep(0.05)
        colour -= 5

def sleep(x,y):
    fade_in(x,y)
    time.sleep(0.3)
    fade_out(x,y)
    time.sleep(1)

def sleeps(xs,ys):
    fade_ins(xs,ys)
    time.sleep(0.3)
    fade_outs(xs,ys)
    time.sleep(1)

def sleep_column(x):
    fade_ins([x]*8, range(8))
    time.sleep(0.3)
    fade_outs([x]*8, range(8))
    time.sleep(1)

def sleep_row(y):
    fade_ins(range(8),[y]*8)
    time.sleep(0.3)
    fade_outs(range(8),[y]*8 )
    time.sleep(1)

def blink(x,y):
    setpixel(x,y,(0,100,0),True)
    time.sleep(2)
    setpixel(x,y,(0,0,0),True)
    time.sleep(2)

def wipe():
    for x in range(8):
        set_row(x, (100,0,80))
        time.sleep(0.1)
    for x in range(8):
        set_row(x, (0,0,0))
        time.sleep(0.1)

def wipe_rev():
    for x in reversed(range(8)):
        set_row(x, (100,0,80))
        time.sleep(0.1)
    for x in reversed(range(8)):
        set_row(x, (0,0,0))
        time.sleep(0.1)


def spiral(self):
    print "this function will show a spiral"

def equalizer(self):
    print "this function fades out columns like an equalizer"

def diagonal(self):
    print "this function will wipe the screen diagonally"

def random_out(self):
    print "this function will clear the screen at random"

def rainfall(self):
    print "this function will fill the screen like the matrix"

def blink_spread(self):
    print "this function will blink the center and then fill in"

def tracer_row(x, on):
    for y in range(8):
        unicorn.set_pixel(x, y, 0, 0, 0)
    unicorn.set_pixel(x, on, 100, 0, 100)
    unicorn.show()

if __name__ == "__main__":
    unicorn.rotation(180)
    while True:
        blink(0,0)
        sleep_row(0)
        wipe()
