# Low-Earth-Orbit-occupation

This project is part of a Datathon project within a team of 4 people.

SATS.txt contains the TLE (static, at the time of download) coordinates of approximately 4,000 objects in Earth orbit, available on CelesTrak.

acquisition.py calculates the x, y, z (latitude, longitude, altitude) coordinates of approximately 3,000 objects in low orbit, normalizes it in a pandas DataFrame and saves it in the data.csv file. This operation currently takes about 2 hours.

vizualization.py allows to view the position (latitude, longitude) of objects on a globe and their altitude on antoher plot. These 2 visual objects allow the appearance of a pop-up with the name and altitude, a highlighting of the STARLINK, FLOCK and ISS objects, and a zoom.

This visualization is done with Plotly and available in Objects.html 
