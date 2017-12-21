import random
from Onaeri.lamp import Lamp
from Onaeri import helper
from Onaeri.settings.Global import valRange
from network import light_objects
from pytradfri import error


briRange = (1, 254)  # [min, max] brightness. Unsigned int
colorRange = (454, 250)  # [min, max] color temp. Unsigned int
metrics = {'total': 0, 'success': 0, 'timeout': 0}


def poll():
    """
    Get info from all lamps from gateway.
    """
    metrics['total'] += 1

    ret = []
    for device in light_objects:
        rand = random.randrange(1000)
        brightness = None
        color = None
        if rand == 1:
            brightness = random.randrange(briRange[0], briRange[1])
            color = random.randrange(colorRange[1], colorRange[0])

        ret.append(Lamp(
                   helper.scale(brightness, briRange, valRange),
                   helper.scale(color, colorRange, valRange),
                   power=True,
                   name=device.name)
                   )

    metrics['success'] += 1
    return ret
