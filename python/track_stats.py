from glob import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from sklearn.neighbors import KernelDensity
from scipy.interpolate import griddata
from scipy.stats.kde import gaussian_kde
from netCDF4 import Dataset

# gather the track files and compile into dataframe
files = glob('/Users/deanabaron/StrideSearch/build/*track*.txt')
#files = glob('/Users/deanabaron/Desktop/dataTemp/NewNorthAmericanTesting_1004/data/*track*.txt')

df = pd.read_csv(files[0], sep=';', skiprows=[0], header=None)

trks = df.append([pd.read_csv(files[i], sep=';', skiprows=[0], header=None) for i in range(1, 282)])

# add header
trks.columns = ['datetime', 'lat', 'lon', 'min(SLP)', 'max(avg(PRESGRAD))']

# convert datetime and extract month
trks['datetime'] = pd.to_datetime(trks.datetime)
print(trks[trks['min(SLP)'] < 96000.0])
# trks['month'] = trks['datetime'].apply(lambda x: x.month)
# #
# # #print(trks)
# #
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
# # monthly.loc[5] = [0]
# # monthly.index = monthly.index + 1
# # monthly = monthly.sort_index()
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
# plt.show()
# ---------------------------------------------------------------------------
# track density using KDE?

# plot coastlines with basemap
# fig = plt.figure()
#
# def kde2D(x, y, bandwidth, xbins=100j, ybins=100j, **kwargs):
#     """Build 2D kernel density estimate (KDE)."""
#
#     # create grid of sample locations (default: 100x100)
#     xx, yy = np.mgrid[x.min():x.max():xbins,
#                       y.min():y.max():ybins]
#
#     xy_sample = np.vstack([yy.ravel(), xx.ravel()]).T
#     xy_train  = np.vstack([y, x]).T
#
#     kde_skl = KernelDensity(bandwidth=bandwidth, **kwargs)
#     kde_skl.fit(xy_train)
#
#     # score_samples() returns the log-likelihood of the samples
#     z = np.exp(kde_skl.score_samples(xy_sample))
#     return xx, yy, np.reshape(z, xx.shape)
#
# m = Basemap(llcrnrlat=10.0, llcrnrlon=255.0, urcrnrlat=65.0, urcrnrlon=330.0,
#             projection='merc', resolution='l')
# m.drawcoastlines()
# m.drawcountries()
# #m.fillcontinents(color='white', lake_color='white')
# m.drawmeridians(np.arange(-95, -35, 10), labels=[0, 0, 0, 1])
# m.drawparallels(np.arange(15, 65, 10), labels=[1, 0, 0, 0])
#
# # x, y = trks.lon, trks.lat
# xx, yy, zz = kde2D(trks.lon, trks.lat, 1.0, xbins=50j, ybins=50j)
# #m.scatter(xx, yy, latlon=True)
#
# CS = m.contourf(xx, yy, zz, cmap='Reds', latlon=True)
# cbar = m.colorbar(CS)
# cbar.ax.get_yaxis().labelpad = 15
# cbar.ax.set_ylabel("Probability density", rotation=270)
#
#
# plt.title("Extratropical Storm Track Density in the North Atlantic, 2005-2008")
# plt.show()
# # ---------------------------------------------------------------------------
# plotting pressure changes over time per track

# fig = plt.figure()
# fig.hold(True)
#
# for i in range(len(files)):
#     fig = plt.figure()
#     df = pd.read_csv(files[i], sep=';')
#     pressure = [df['min(SLP)'][j] for j in range(len(df['min(SLP)']))]
#     time = [df['datetime'][i] for i in range(len(df['datetime']))]
#     plt.ylim((trks['min(SLP)'].min(), trks['min(SLP)'].max()))
#     plt.plot(time, pressure)
#     fig.autofmt_xdate()
#     plt.title("Pressure Over Time for Track " + str(df['datetime'][0]) + "-" + str(df['datetime'][len(df)-1]))
#     plt.savefig('/Users/deanabaron/Desktop/dataTemp/NewNorthAmericanTesting_LONGERTRACKS/' +
#                 str(df['datetime'][0]) + "-" + str(df['datetime'][len(df)-1]) + '.png')


# ---------------------------------------------------------------------------
# calculating the deepening of the storms

# df = pd.read_csv(files[0], sep=';')
# df = df.set_index('datetime')
# diff = df.diff()
# diff = diff.drop(columns=['lat', 'lon', 'max(avg(PRESGRAD))'])
# diff['lat'] = df['lat']
# diff['lon'] = df['lon']
#
# mean = [((diff['min(SLP)'].mean())/6)/100]
# maxi = [((diff['min(SLP)'].max())/6)/100]
#
# for i in range(1,282):
#     df = pd.read_csv(files[i], sep=';')
#     df = df.set_index('datetime')
#     dff = df.diff()
#     dff = dff.drop(columns=['lat', 'lon', 'max(avg(PRESGRAD))'])
#     dff['lat'] = df['lat']
#     dff['lon'] = df['lon']
#     diff = diff.append(dff)
#     maxi.append(((dff['min(SLP)'].max())/6)/100)
#     mean.append(((dff['min(SLP)'].mean(skipna=True))/6)/100)
#
# diff['dp/dt'] = diff['min(SLP)']
# diff = diff.drop(columns=['min(SLP)'])
#
# def convert_to_hPa(x):
#     return (x / 6) / 100
#
# diff['dp/dt'] = diff['dp/dt'].apply(convert_to_hPa)
#
# raw_max_vals = diff['dp/dt'].to_list()
# # plt.show()
#
# #print(mean)
# # def minmax(val_list):
# #     min_val = np.nanmin(val_list)
# #     max_val = np.nanmax(val_list)
# #
# #     return (min_val, max_val)
# #
# # print(minmax(raw_vals))
#
# maxi_range = list(np.linspace(-2,5,29))
# mean_range = list(np.linspace(-2,4,25))
# raw_range = list(np.linspace(-3,4,29))
#
# # plt.hist(raw_vals, raw_range, ec='black')
# # plt.xlabel('dp/dt (hPa/hr)')
# # plt.ylabel('Count')
# # plt.title('Histogram of Deepening Rate')
# # plt.grid(True)
# # plt.show()
# #
# # plt.hist(maxi, maxi_range, ec='black')
# # plt.xlabel('dp/dt (hPa/hr)')
# # plt.ylabel('Count')
# # plt.title('Histogram of Max Deepening Rate')
# # plt.grid(True)
# # plt.show()
# #
# # plt.hist(mean, mean_range, ec='black')
# # plt.xlabel('dp/dt (hPa/hr)')
# # plt.ylabel('Count')
# # plt.title('Histogram of Mean Deepening Rate')
# # plt.grid(True)
# # plt.show()
#
# KDE based on dp/dt?
# fig = plt.figure()
#
# m = Basemap(llcrnrlat=10.0, llcrnrlon=255.0, urcrnrlat=65.0, urcrnrlon=330.0,
#             projection='merc', resolution='l')
# m.drawcoastlines()
# m.drawcountries()
# #m.fillcontinents(color='white', lake_color='white')
# m.drawmeridians(np.arange(-95, -35, 10), labels=[0, 0, 0, 1])
# m.drawparallels(np.arange(15, 65, 10), labels=[1, 0, 0, 0])
#
# diff2 = diff.dropna()
#
# x = diff2.lon
# y = diff2.lat
# z = diff2['dp/dt']
#
# xx, yy = np.mgrid[x.min():x.max():50j, y.min():y.max():50j]
# zz = griddata((x,y), z, (xx, yy),method='nearest')
#
# #m.scatter(xx, yy, latlon=True)
#
# CS = m.contourf(xx, yy, zz, cmap='RdBu', latlon=True)
# cbar = m.colorbar(CS)
# cbar.ax.get_yaxis().labelpad = 15
# cbar.ax.set_ylabel("Deepening rate (hPa/hr)", rotation=270)
#
#
# plt.title("Extratropical Storm Track Tendency \n in the North Atlantic, 2005-2008")
# plt.show()