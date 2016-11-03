import random
import unicornhat as unicorn

from monitor import lightshow

if __name__ == "__main__":
    while True:
        try:
            x = random.randint(0,7)
            y = random.randint(0,7)
            lightshow.sleep(x,y)
        except KeyboardInterrupt:
            break
    unicorn.off()
