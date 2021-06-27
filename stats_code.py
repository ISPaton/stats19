import pandas as pd
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
from shapely.geometry import Point
%matplotlib inline

vehicles_df = pd.read_csv("http://data.dft.gov.uk/road-accidents-safety-data/dftRoadSafetyData_Vehicles_2018.csv")
casualties_df = pd.read_csv("http://data.dft.gov.uk/road-accidents-safety-data/dftRoadSafetyData_Casualties_2018.csv")
accidents_df = pd.read_csv("http://data.dft.gov.uk/road-accidents-safety-data/dftRoadSafetyData_Accidents_2018.csv")
vehicles_df.head()
casualties_df.head()
accidents_df.head()
accidents_df_scotland = accidents_df[accidents_df.Police_Force >=91]
accidents_df.describe()
accidents_df_scotland.describe()
road_safety_1 = accidents_df_scotland.join(casualties_df, lsuffix='Accident_Index', rsuffix='Accident_Index')
road_safety_scotland = road_safety_1.join(vehicles_df,lsuffix='Accident_Index', rsuffix='Accident_Index')
road_safety_scotland.head()
lookup_df = pd.read_excel("http://data.dft.gov.uk/road-accidents-safety-data/variable%20lookup.xls", sheet_name="Accident Severity")
road_safety_scotland_merge = pd.merge(left=road_safety_scotland, right=lookup_df, left_on='Accident_Severity', right_on='code')
road_safety_scotland_merge = road_safety_scotland_merge.drop('code',1)
road_safety_scotland_merge = road_safety_scotland_merge.drop('Accident_Severity',1)
road_safety_scotland_merge.head()
road_safety_geometry = [Point(xy) for xy in zip(road_safety_scotland_merge['Location_Easting_OSGR'], road_safety_scotland_merge['Location_Northing_OSGR'])]
crs = {'init':'epsg:27700'}
safety_map = gpd.GeoDataFrame(road_safety_scotland_merge, crs=crs, geometry = road_safety_geometry)
safety_map.plot(column = 'label',cmap='RdYlGn',figsize=(18,16),edgecolor='black', legend=True).set_axis_off()
plt.title('Road Safety in Scotland 2018')
