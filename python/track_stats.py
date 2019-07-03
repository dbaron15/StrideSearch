from glob import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from sklearn.neighbors import KernelDensity
from scipy.stats.kde import gaussian_kde
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

# plot coastlines with basemap
fig = plt.figure()

def kde2D(x, y, bandwidth, xbins=100j, ybins=100j, **kwargs):
    """Build 2D kernel density estimate (KDE)."""

    # create grid of sample locations (default: 100x100)
    xx, yy = np.mgrid[x.min():x.max():xbins,
                      y.min():y.max():ybins]

    xy_sample = np.vstack([yy.ravel(), xx.ravel()]).T
    xy_train  = np.vstack([y, x]).T

    kde_skl = KernelDensity(bandwidth=bandwidth, **kwargs)
    kde_skl.fit(xy_train)

    # score_samples() returns the log-likelihood of the samples
    z = np.exp(kde_skl.score_samples(xy_sample))
    return xx, yy, np.reshape(z, xx.shape)

m = Basemap(llcrnrlat=10.0, llcrnrlon=255.0, urcrnrlat=65.0, urcrnrlon=330.0,
            projection='merc', resolution='l')
m.drawcoastlines()
m.drawcountries()
#m.fillcontinents(color='white', lake_color='white')
m.drawmeridians(np.arange(-95, -35, 10), labels=[0, 0, 0, 1])
m.drawparallels(np.arange(15, 65, 10), labels=[1, 0, 0, 0])

# x, y = trks.lon, trks.lat
xx, yy, zz = kde2D(trks.lon, trks.lat, 1.0, xbins=50j, ybins=50j)
#m.scatter(xx, yy, latlon=True)

CS = m.contourf(xx, yy, zz, cmap='Reds', latlon=True)
cbar = m.colorbar(CS)
cbar.ax.get_yaxis().labelpad = 15
cbar.ax.set_ylabel("Probability density", rotation=270)


plt.title("Extratropical Storm Track Density in the North Atlantic, 2005-2008")
plt.show()