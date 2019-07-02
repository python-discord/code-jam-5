import numpy as np
import matplotlib.pyplot as plt
from csvReader import getData
import random
import os

# This is shitty Proof of concept code, I'll update it later

# selects a random file from the gsoy-latest directory
this_dir = os.path.dirname(os.path.realpath(__file__))
random_file = random.choice(open('Temp_Data.txt', 'r').readlines())[:-1]
path = this_dir + '/gsoy-latest/' + random_file
print(path)
# converts the file to a dict of {Year: Temp}
data = getData(path)
print(data)
data = list(data.values())

# converts data to a stack so it can be used in plt.imshow
img_data = np.stack((data, data))
plt.figure(figsize=(6, 18))

# Displays the Data as a gradient image based on temp
# https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.pyplot.imshow.html
plt.imshow(img_data, cmap='RdBu_r', aspect=40)
plt.axis('off')

plt.show()
# saves cropped Image
plt.savefig('figure.png', bbox_inches='tight', dpi=400)
