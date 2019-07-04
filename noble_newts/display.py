import matplotlib.pyplot as plt
from csvReader import merge_set, monthly_data
from Stations import Stations

# This is shitty Proof of concept code, I'll update it later
# selects a random file from the gsoy-latest directory

fileList = Stations().getStations()
print(fileList)

data = monthly_data('gsom-latest/' + fileList[0] + '.csv')

for file in fileList:
    file += '.csv'
    data2 = monthly_data('gsom-latest/' + file)
    data = merge_set(data, data2)


plt.axis('off')
plt.plot(data.keys(), data.values(), '-')
plt.show()

"""
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
"""
