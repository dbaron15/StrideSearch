from glob import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from sklearn.neighbors import KernelDensity
from netCDF4 import Dataset

# gather the track files and compile into dataframe
files = glob('/Users/deanabaron/StrideSearch/build/*track*.txt')

df = pd.read_csv(files[0], sep=';', skiprows=[0], header=None)

trks = df.append([pd.read_csv(files[i], sep=';', skiprows=[0], header=None) for i in range(1, 263)])

# add header
trks.columns = ['datetime', 'lat', 'lon', 'min(SLP)', 'max(avg(PRESGRAD))']

# convert datetime and extract month
trks['datetime'] = pd.to_datetime(trks.datetime)
trks['month'] = trks['datetime'].apply(lambda x: x.month)
#
# #print(trks)
#
# # monthly frequency with storms
#
# # extract start of every track
# temp = trks[trks.index==0]
#
# # group events by the month
# monthly = temp.groupby(['month']).count()
# monthly['numstorms'] = monthly['datetime']
# monthly = monthly.drop(columns=['datetime', 'lat', 'lon', 'min(SLP)', 'max(avg(PRESGRAD))'])
#
# # insert May
# monthly.loc[5] = [0]
# monthly.index = monthly.index + 1
# monthly = monthly.sort_index()
# #print(monthly)
#
# # insert month names for labeling
# monthly['monthname'] = monthly.index
# monthly['monthname'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
#
# # Figure 1: Number of Storms per Month
# ax1 = monthly.plot(kind='bar', title="Number of ECC Storms Found per Month, 2005-2008",
#                   legend=False, x='monthname', y='numstorms', rot=0)
# ax1.set_xlabel("Month",fontsize=12)
# ax1.set_ylabel("Number of Storms",fontsize=12)
# #plt.show()

# track density using KDE?
datafilename = '/Users/deanabaron/StrideSearch/testData/ERAinterim_extratrop_grad.nc'
ncd = Dataset(datafilename, "r")
Y, X = np.meshgrid(ncd.variables['lon'][:], ncd.variables['lat'][:])

# combine lats and lons together
trks['latlon'] = zip(trks.lon, trks.lat)

# Set up the data grid for the contour plot
#X, Y = trks.lon, trks.lat
xy = np.vstack([X.ravel(), Y.ravel()]).T

# plot coastlines with basemap
m = Basemap(llcrnrlat=10.0, llcrnrlon=255.0, urcrnrlat=65.0, urcrnrlon=330.0,
            projection='merc', resolution='l')
m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='white', lake_color='white')
m.drawmeridians(np.arange(-95, -35, 10), labels=[0, 0, 0, 1])
m.drawparallels(np.arange(15, 65, 10), labels=[1, 0, 0, 0])

# construct a spherical kernel density estimate of the distribution
kde = KernelDensity(bandwidth=0.03, metric='haversine')
kde.fit(np.radians(zip(trks.lon, trks.lat)))

Z = np.exp(kde.score_samples(xy))
Z = Z.reshape(X.shape)

# plot contours of the density
levels = np.linspace(0, 0.5, 10)
m.contourf(X, Y, Z, levels=levels, cmap='Reds')
plt.title("Extratropical Storm Track Density in the North Atlantic, 2005-2008", fontsize=14)
plt.show()
pass