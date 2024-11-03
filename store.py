import os
import inspect
from models import Pilot

# Determine the path and parent directory of this script
script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
script_dir = os.path.dirname(script_path)
store_path = os.path.join(script_dir,"pilots.txt")

class Store:
    def __init__(self):
        self.pilots = self.get_pilots_from_file()

    def get_pilots_from_file(self):
        if not os.path.exists(store_path):
            return []
        with open(store_path, "r") as f:
            lines = f.readlines()
            if len(lines) > 0:
                pilots = []
                for line in lines:
                    line = line.strip("\n").split(",")
                    if line != '':
                        pilots.append(Pilot(line[0], line[1:]))
                return pilots
        return []

    def save_pilots_to_file(self):
        with open(store_path, "w") as f:
            for pilot in self.pilots:
                f.write(pilot.name)
                if pilot.alts != [] and pilot.name != '':
                    f.write("," + ",".join(pilot.alts))
                f.write("\n")
        return    