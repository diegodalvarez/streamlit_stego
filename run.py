from stego import *
import numpy as np
from PIL import Image

image = Stego("mushroom.png", "test1234")

test = image.Encode()
test = image.Decode()