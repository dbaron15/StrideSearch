#from Event import print_copyright
#from Track import TrackList
from datetime import datetime, timedelta
from glob import glob
from dateutil.parser import parse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset

#print_copyright()

dataDir = '/Users/deanabaron/StrideSearch/build'

datafilename = '/Users/deanabaron/StrideSearch/testData/ERAinterim_extratrop_grad.nc'
#ss_trackfilename = dataDir + '/' + 'ssResults/ssProfiled_era_extratrop1.h5'

#dstore = pd.HDFStore(ss_trackfilename)
files = glob('/Users/deanabaron/StrideSearch/build/*track*.txt')

#trks = [dstore['trk5'], dstore['trk6'], dstore['trk7']]
trks = []
for trk in files:
    #trkname = trk;
    trk = pd.read_csv(trk, sep=';')
    trks.append(trk)

ncd = Dataset(datafilename, "r")
lons, lats = np.meshgrid(ncd.variables['lon'][:], ncd.variables['lat'][:])

#data_time_ind = 70
#dts = [datetime(1900, 1, 1, 0) + timedelta(hours = td) for td in ncd['time'][:]]
#plotDate = dts[data_time_ind]

#ctr_data = 0.01 * ncd.variables['PS'][data_time_ind][:][:]

# fig = plt.figure()
# fig.hold(True)
# #m = Basemap(projection="ortho", lat_0 = 30, lon_0 = 200, resolution = 'l')
# m = Basemap(llcrnrlat = 15.0, llcrnrlon = 265.0, urcrnrlat = 55.0, urcrnrlon = 315.0, projection = 'merc', resolution = 'l')
#
# m.drawcoastlines()
# m.drawcountries()
# m.fillcontinents(color='white', lake_color='white')
# # m.drawmapboundary(fill_color='aqua')
# m.drawmeridians(np.arange(-95,-35,10), labels=[0,0,0,1])
# m.drawparallels(np.arange(15,55,10), labels=[1,0,0,0])

#cp = m.contourf(lons, lats, ctr_data, np.arange(-0.003, 0.003, 0.00005), cmap='RdBu_r', latlon=True)
#cp = m.contourf(lons, lats, ctr_data, np.arange(960.0, 1030.0), cmap='RdBu', latlon=True)
#cb = m.colorbar(cp)
#cb.set_label('hPa')

for df in trks:
    fig = plt.figure()
    fig.hold(True)
    # m = Basemap(projection="ortho", lat_0 = 30, lon_0 = 200, resolution = 'l')
    m = Basemap(llcrnrlat=20.0, llcrnrlon=265.0, urcrnrlat=50.0, urcrnrlon=315.0, projection='merc', resolution='l')

    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color='white', lake_color='white')
    # m.drawmapboundary(fill_color='aqua')
    m.drawmeridians(np.arange(-95, -35, 10), labels=[0, 0, 0, 1])
    m.drawparallels(np.arange(15, 55, 10), labels=[1, 0, 0, 0])
    trkLon = [df['lon'][j] for j in range(len(df['lon']))]
    trkLat = [df['lat'][i] for i in range(len(df['lat']))]
    m.plot(trkLon, trkLat, linewidth=2, latlon=True)
    plt.title(str(df.datetime[0]) + "-" + str(df.datetime[len(df)-1]))

plt.show()
#plt.title("PS " + str(plotDate))
#fig.savefig('ssDemoPlot.png', bbox_inches='tight')




