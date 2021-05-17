from tletools import pandas as tlepd
from pyorbital.orbital import Orbital
from datetime import datetime
import pandas as pd

compteur = 0

def setCoords(name,date):
    global compteur
    print(">>>",compteur)
    compteur += 1
    try:
        orb = Orbital(name)
    except NotImplementedError:
        return None
    coords = orb.get_lonlatalt(now)
    return coords

df = tlepd.load_dataframe("SATS.txt")

now = datetime.utcnow()
print(now)

df['coords'] = df['name'].apply(lambda x: setCoords(x,now))
data = df[df['coords'].notna()]
highOrbits = df[df['coords'].isna()]
print(datetime.utcnow(),"\n\n")

data.to_csv('data.csv', sep = ',')