from room3D import Room
from wall3D import Wall
from transmitter3D import Transmitter
import math


mmur1 = Wall(0.3, (-1,-1,0), (17,-1,0), (-1,-1,4.40), "cloison",[0,1])
mmur2 = Wall(0.3, (-1,9,0), (10.5,9,0), (-1,9,2.20), "cloison",[0])
mmur3 = Wall(0.3, (11,9,0), (17,9,0), (11,9,2.20), "cloison",[0])
mmur4 = Wall(0.3, (-1,-1,0), (-1,9,0), (-1,-1,4.40), "cloison",[0,1])
mmur5 = Wall(0.3, (17,-1,0), (17,9,0), (17,-1,4.40), "cloison",[0,1])
mmur6 = Wall(0.3, (5,9,0), (5,15,0), (5,9,2.20), "cloison",[0])
mmur7 = Wall(0.3, (11,9,0), (11,15,0), (11,9,2.20), "cloison",[0])
mmur8 = Wall(0.3, (5,15,0), (11,15,0), (5,15,2.20), "cloison",[0])
mmur9 = Wall(0.3, (5,9,0), (5,15,0), (5,9,2.20), "cloison",[0])
mmur10 = Wall(0.2, (-1,5,0), (1,5,0), (-1,5,2.20), "brique",[0])
mmur11 = Wall(0.2, (1.5,5,0), (3,5,0), (1.5,5,2.20), "brique",[0])
mmur12 = Wall(0.2, (5,5,0), (12,5,0), (5,5,2.20), "brique",[0])
mmur13 = Wall(0.2, (12.5,5,0), (17,5,0), (12.5,5,2.20), "brique",[0])
mmur14 = Wall(0.2, (5,5,0), (5,5.5,0), (5,5,2.20), "brique",[0])
mmur15 = Wall(0.2, (5,6,0), (5,9,0), (5,6,2.20), "brique",[0])
mmur16 = Wall(0.2, (11,5,0), (11,5.5,0), (11,5,2.20), "brique",[0])
mmur17 = Wall(0.2, (11,6,0), (11,9,0), (11,6,2.20), "brique",[0])
mmur18 = Wall(0.2, (5,6.80,0), (5.60,6.80,0), (5,6.60,2.20), "brique",[0])
mmur19 = Wall(0.2, (6.10,6.80,0), (11,6.80,0), (6.10,6.80,2.20), "brique",[0])
mmur20 = Wall(0.2, (2,-1,0), (2,5,0), (2,-1,2.20), "brique",[0])


mmur101 = Wall(0.3, (-1,9,2.20), (17,9,2.20), (-1,9,4.40), "cloison",[1])
mmur102 = Wall(0.2, (2,-1,2.20), (2,5,2.20), (2,-1,4.40), "brique",[1])
mmur103 = Wall(0.2, (2,5.80,2.20), (2,9,2.20), (2,5.80,4.40), "brique",[1])
mmur104 = Wall(0.2, (5,-1,2.20), (5,4.5,2.20), (5,-1,4.40), "brique",[1])
mmur105 = Wall(0.2, (8,-1,2.20), (8,4.5,2.20), (8,-1,4.40), "brique",[1])
mmur106 = Wall(0.2, (11,-1,2.20), (11,4.5,2.20), (11,-1,4.40), "brique",[1])
mmur107 = Wall(0.2, (-1,4.5,2.20), (1,4.5,2.20), (-1,4.5,4.40), "brique",[1])
mmur108 = Wall(0.2, (1.5,4.5,2.20), (4,4.5,2.20), (1.5,4.5,4.40), "brique",[1])
mmur109 = Wall(0.2, (4.5,4.5,2.20), (7,4.5,2.20), (4.5,4.5,4.40), "brique",[1])
mmur1010 = Wall(0.2, (7.5,4.5,2.20), (10,4.5,2.20), (7.5,4.5,4.40), "brique",[1])
mmur1011 = Wall(0.2, (10.5,4.50,2.20), (11.25,4.50,2.20), (10.5,4.50,4.40), "brique",[1])
mmur1012 = Wall(0.2, (11.75,4.50,2.20), (12.5,4.50,2.20), (11.75,4.50,4.40), "brique",[1])
mmur1013 = Wall(0.2, (13,4.50,2.20), (17,4.50,2.20), (13,4.50,4.40), "brique",[1])
mmur1014 = Wall(0.2, (2,6.30,2.20), (3.5,6.30,2.20), (2,6.30,4.40), "brique",[1])
mmur1015 = Wall(0.2, (4,6.30,2.20), (5,6.30,2.20), (4,6.30,4.40), "brique",[1])
mmur1016 = Wall(0.2, (5.50,6.30,2.20), (7,6.30,2.20), (5.50,6.30,4.40), "brique",[1])
mmur1017 = Wall(0.2, (7.50,6.30,2.20), (12.5,6.30,2.20), (7.50,6.30,4.40), "brique",[1])
mmur1018 = Wall(0.2, (13,6.30,2.20), (17,6.30,2.20), (13,6.30,4.40), "brique",[1])
mmur1019 = Wall(0.2, (12,4.50,2.20), (12,9,2.20), (12,4.50,4.40), "brique",[1])
mmur1020 = Wall(0.2, (4.70,6.30,2.20), (4.70,7.65,2.20), (4.70,6.30,4.40), "brique",[1])
mmur1021 = Wall(0.2, (4.70,7.65,2.20), (6,7.65,2.20), (4.70,7.65,4.40), "brique",[1])
mmur1022 = Wall(0.2, (6,6.30,2.20), (6,9,2.20), (6,6.30,4.40), "brique",[1])

ssol = Wall(0.1, (-1,-1,0), (17,-1,0), (-1,15,0), "sol", [-1])
pplafond1 = Wall(0.2, (-1,-1,2.20), (17,-1,2.20), (-1,9,2.20), "brique",[-3])
pplafond12 = Wall(0.3, (5,9,2.20), (5,15,2.20), (11,9,2.20), "cloison",[-3])
pplafond2 = Wall(0.3, (-1,-1,4.40), (17,-1,4.40), (-1,9,4.40), "cloison",[-3])

m = [mmur101,mmur102,mmur103,mmur104,mmur105,
     mmur106,mmur107,mmur108,mmur109,mmur1010,
     mmur1011,mmur1012,mmur1013,mmur1014,mmur1015,
     mmur1016,mmur1017,mmur1018,mmur1019,mmur1020,
     mmur1021,mmur1022,mmur1,mmur2,mmur3,mmur4,mmur5,
     mmur6,mmur7,mmur8,mmur9,mmur10,mmur11,mmur12,mmur13,
     mmur14,mmur15,mmur16,mmur17,mmur18,mmur19,mmur20,
     ssol,pplafond1,pplafond12,pplafond2]

room1 = Room()

room1.list_of_walls = m
room1.list_of_transmitters.append(Transmitter((math.pi/6-1, math.pi-1, 1), "lambda-demi"))


room1.ray_and_power_distribution(2, 16, 18, 1)
