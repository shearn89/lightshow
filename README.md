# Lightshow #

This repo contains the python scripts to run some extremely simple 
monitoring from a Raspberry Pi. It's designed to go with a 
[unicorn hat](https://shop.pimoroni.com/products/unicorn-hat)
from Pi Moroni.

# Installation #

If you have a Unicorn Hat, it requires the `unicornhat` module:

    sudo pip install unicornhat

Otherwise, you'll need to comment out the references to `lightshow`
in `controller.py`, and maybe tweak a few things.

You'll also need `lighttpd` installed so it can present a web interface.

# Usage #
The script assumes that `lighttpd` is serving files out of 
`/var/www/html/`. **WARNING**: this script will overwrite any `index.html`
file in that directory!

Run the script as root, it'll write `index.html` and fire up the Hat if
present. Browse to the IP of the pi, and you'll see a list of checks.

# Checks #
Checks are configured in `monitor\checks.py` and run from `controller.py`. I've not got 
around to building a config file system yet...
