#!/usr/bin/env python

import matplotlib.pyplot as pl
import cartopy
import cartopy.crs as ccrs

# co-ordinates taken from Wikipedia article on BiSON 2017-11-20 11:27
coords = {'Mount Wilson': (34.22, -118.07),
          'Las Campanas': (-29.01597, -70.69208),
          'Teide Observatory': (28.3, -16.5097),
          # 'SAAO': (-33.9347, 18.4776),
          'Sutherland': (-32.376006, 20.810678),
          'Carnarvon': (-24.869167, 113.704722),
          'Paul Wild Observatory': (-30.314, 149.562),
          'University of Birmingham': (52.450556, -1.930556)}

lat0 = 0
for i, lon0 in enumerate([-45, 135]):
    ax = pl.subplot(1, 2, i+1, projection=ccrs.Orthographic(lon0, lat0)) # (lon, lat)
    ax.set_global()

    ax.add_feature(cartopy.feature.OCEAN, zorder=0)
    ax.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')

    for lat, lon in coords.values():
        if lon0-90 < lon < lon0+90:
            ax.plot(lon, lat, 'ro', transform=ccrs.PlateCarree())

pl.show()
