import solar_sistem as z
import numpy as np

p1 = z.Universe("Sunce","Zemlja","Merkur","Venera","Mars","Jupiter")
p1.komet(14**17,np.array([10000,-14000,0]),np.array([-7.486E11*1.5,7.486E11,0]))
p1.anima()
p1.reset()

