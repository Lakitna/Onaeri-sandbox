"""
Sandbox wrapper for Onaeri API
"""

__version__ = '0.1.0'

import sys
import os
import traceback
import atexit
from time import sleep, strftime, time
from Onaeri.logger import log
from Onaeri import Onaeri, settings, __version__ as onaeriVersion
import lampdata
import network

onaeri = Onaeri(lampdata.poll())
updateCounter = 0

log()
log.row()
log("RUNTIME STARTED")
log("Onaeri v%s" % (onaeriVersion))
log.error("Onaeri Sandbox v%s" % __version__)
log.row()
log()


def summaryBuild():
    def colorSuccessRate(val):
        if val < 80:
            return "%s #superLow" % val
        if val < 90:
            return "%s #low" % val
        if val < 95:
            return "%s #ok" % val
        if val > 98:
            return "%s #awesome" % val
        if val >= 95:
            return "%s #good" % val
        return val

    version = {}
    import Onaeri
    version['Onaeri API'] = Onaeri.__version__
    version['Onaeri Sandbox'] = __version__

    time = {}
    time['timecodes'] = onaeri.time.runtime
    time['minutes'] = round(onaeri.time.runtime
                            * settings.Global.minPerTimeCode, 2)
    time['hours'] = round((onaeri.time.runtime
                          * settings.Global.minPerTimeCode) / 60, 2)

    observer = lampdata.metrics
    observer["success rate"] = round((observer['success']
                                     / observer['total']) * 100, 2)
    observer['success rate'] = colorSuccessRate(observer['success rate'])

    log.summary({
        'Versions': version,
        'Program runtime': time,
        'Observer calls': observer,
        'Updates handled': updateCounter,
        'Cycles handled': [cycle.name for cycle in onaeri.cycles],
    })


atexit.register(summaryBuild)


while True:
    try:
        start = time()
        lampData = lampdata.poll()

        # Progress all cycles and pass the current state of all lamps
        onaeri.tick(lampData)

        if onaeri.update:
            updateCounter += 1
            print("[%s]:" % (strftime("%H:%M:%S")))

            for cycle in onaeri.cycles:
                for id in cycle.lamp:
                    if not cycle.lamp[id].isEmpty(['brightness',
                                                   'color',
                                                   'power']):
                        print("\t%s: %s" % (cycle.name, cycle.lamp[id]))

        log.warn("Loop took %s seconds" % (time() - start))

        # Slow down a bit, no stress brah
        sleep(settings.Global.mainLoopDelay)
    except KeyboardInterrupt:
        log()
        log("Keyboard interrupt. Exiting.")
        exit()
    except Exception:
        log()
        log("An error occurred:")
        log(traceback.format_exc())
        exit()
