"""Single internal HD resolution policy for both DS displays."""
MIN_WIDTH=768
MAX_WIDTH=960
DEFAULT_WIDTH=960
MAX_HEIGHT=MAX_WIDTH*3//4
SCREEN_RGBA_BYTES=MAX_WIDTH*MAX_HEIGHT*4

def clamp_width(width):
    return max(MIN_WIDTH,min(MAX_WIDTH,round(int(width)/32)*32))
