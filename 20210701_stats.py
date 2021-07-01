# 1 import packages
#some of these are unused but useful to know about

import numpy as np
import pandas as pd
import geopandas as gpd
from pandas import Series, DataFrame
from shapely.geometry import Point
from scipy import stats
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

# 2 imports a CSV file that has been prepared earlier by joining 3 tables

stats_data = pd.read_csv('C:/Users/paton/Documents/_CODE/STATS19/STATS19_Scotland.csv')
stats_df = pd.DataFrame(stats_data)
list(stats_df)

# 3 turning the above into spatial data
# Coordinate reference system : BNG
crs = {'init': 'epsg:27700'}
geometry = [Point(xy) for xy in zip(stats_df['location_e'], stats_df['location_n'])]
stats_df = gpd.GeoDataFrame(stats_df, crs=crs, geometry=geometry)
stats_df.plot(column = 'casualty_severity',cmap = 'RdYlGn',figsize =(18,16))
plt.show()

# 4 reading in SIMD data which is already spatial
simdmap_df = gpd.read_file('C:/Users/paton/Documents/_CODE/STATS19/SG_SIMD_2016.shp')
simdmap_df.head()
simdmap_df = simdmap_df.to_crs({'init': 'epsg:27700'})
simdmap_df.plot(column='Decile',figsize =(18,16))


# 5 Joining the two datasets - spatial intersection
stats_simd_join = gpd.sjoin(stats_df, simdmap_df, how='inner',op = 'intersects')
stats_simd_join.head()

# 6 selecting a subset of urban data
stats_simd_urban= stats_simd_join[stats_simd_join.urban_rural_location == 'Urban']
stats_simd_urban["urban_rural_location"]
stats_simd_urban.plot(column='Decile',figsize =(18,16))

# 7 Someone got there first!
from IPython.display import Image
Image("C:/Users/paton/Documents/_CODE/STATS19/sustrans.png")


# 8 Updated resources - obtain the data from source
vehicles_df = pd.read_csv("http://data.dft.gov.uk/road-accidents-safety-data/dftRoadSafetyData_Vehicles_2018.csv")
casualties_df = pd.read_csv("http://data.dft.gov.uk/road-accidents-safety-data/dftRoadSafetyData_Casualties_2018.csv")
accidents_df = pd.read_csv("http://data.dft.gov.uk/road-accidents-safety-data/dftRoadSafetyData_Accidents_2018.csv")
accidents_df.describe()

# 8 select a scotland subset
accidents_df_scotland = accidents_df[accidents_df.Police_Force >=91]
accidents_df_scotland.describe()

# 8 two table joins to create a composite table out of the three
road_safety_1 = accidents_df_scotland.join(casualties_df, lsuffix='Accident_Index', rsuffix='Accident_Index')
road_safety_scotland = road_safety_1.join(vehicles_df,lsuffix='Accident_Index', rsuffix='Accident_Index')
road_safety_scotland

#8 lookup table for values
lookup_df = pd.read_excel("http://data.dft.gov.uk/road-accidents-safety-data/variable%20lookup.xls", sheet_name="Accident Severity")
lookup_df

#8 merging the lookup table with the table data
road_safety_scotland_merge = pd.merge(left=road_safety_scotland, right=lookup_df, left_on='Accident_Severity', right_on='code')
road_safety_scotland_merge