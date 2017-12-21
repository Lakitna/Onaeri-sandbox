from Onaeri.lamp import Lamp
from Onaeri.logger import log
import random

log("Creating network:", end=" ")

devices = []
cycles = [
    "Alpha", "Beta", "Gamma", "Delta",
    "Epsilon", "Zeta", "Eta", "Theta",
    "Iota", "Kappa", "Lambda", "Mu",
    "Nu", "Xi", "Omnicron", "Pi",
    "Rho", "Sigma", "Tau", "Upsilon",
    # "Phi", "Chi", "Psi", "Omega"
]
for c in cycles:
    for i in range(random.randrange(1, 10)):
        devices.append(Lamp(name="%s %s" % (c, i)))

# Get list of all controllable lamps
light_objects = [dev for dev in devices]

# Key list of controllable lamps with their lamp name
light_ids = {}
for l in light_objects:
    if l.name in light_ids:
        log.error("Two lamps have the exact same name. " +
                  "Please make all lamp names unique and try again.")
        exit()
    light_ids[l.name] = l

log.success("Done", end="\n\n")
