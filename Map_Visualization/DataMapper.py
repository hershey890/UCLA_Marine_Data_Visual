# module DataMapper.py
# To map a specific region, check out these links:
# https://stackoverflow.com/questions/25428512/draw-a-map-of-a-specific-country-with-cartopy
# https://github.com/SciTools/cartopy/issues/1048
# Code for downloading tiles for mapping online: https://scitools.org.uk/cartopy/docs/latest/gallery/eyja_volcano.html

# TODO: use folium to have dynamic maps
# TODO: make a GUI that allows for more flexible movement of the plot (this may require folium)
# TODO: labels on the map
# TODO: get a high quality map of LA/CA region

###########################################################################
#   DATA FORMAT - .txt file
#   Column 1: year, month day hour minute decimal second.
#   Column 2: day month year
#   Column 3: hour minute second
#   Column 4: longitude
#   Column 5: Latitude
#   Column 6: ships heading in degrees
#   Column 7: Ships course over ground
#   Column 8: ships speed over ground
#   Column 9: Temperature
#   Column 10: Salinity
#   Column 11: Conductivity
#   Column 12: Fluorescence
###########################################################################

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import cartopy.io.img_tiles as cimgt

# Colorbar
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np


class DataAttributes:
    """ Substitute for enumeration """
    DATE                = 1
    TIME                = 2
    GPS_LONGITUDE       = 3
    GPS_LATITUDE        = 4
    SHIP_HEADING_DEG    = 5
    SHIP_COURSE_GROUND  = 6
    SHIP_SPEED_GROUND   = 7
    TEMPERATURE         = 8
    SALINITY            = 9
    CONDUCTIVITY        = 10
    FLUORESCENCE        = 11

def data_parser(file:str, fLongitude_list:list=[], fLatitude_list:list=[], fData_list:list=[], iData_Attribute:int=0,
                fVector_Data_list:list=[], iVector_Data_Type:int=0):
    """ Reads the data from the .txt file and stores it in a list for longitude and one for latitude

    :param file: string containing the name of the file with the sensor data (must contain the file extension .txt)
    :param fLongitude_list: pass an empty list that will be filled with all the longitudinal data points
    :param fLatitude_list: pass an empty list that will be filled with all the latitude data points
    :param fData_list: stores an optional data attribute to be displayed (i.e. temperature, salinity,
           conductivity, fluorescence), ex. DataAttributes.SALINITY
    :param iData_Attribute: pass a member variables (8-11) from DataAttributes to determine which one is plotted
    :return: void - modifies the lists passed to the function
    """

    # Clears the data in the lists (using fLongitude_list = [] redeclares the list which causes issues)
    fLongitude_list[:]     = []
    fLatitude_list[:]      = []
    fData_list[:]          = []
    fVector_Data_list[:]   = []

    # Opens, closes and reads the file
    with open(file, 'r') as data:
        # Iterates through lines in the file
        for line in data:
            iNumber_spaces = 0
            fLongitude = ''
            fLatitude = ''
            fData = ''
            fVector_Data = ''
            error_flag = False

            # Reads through a single line to save the latitude and longitude
            for char in line:
                # ERROR: if the line contains NaN just skip it
                if char == 'N':
                    error_flag = True
                    break
                if char == ' ':
                    iNumber_spaces += 1
                elif iNumber_spaces == 3 and (char.isnumeric() or char == '.' or char == '+' or char == '-'):
                    fLongitude += char
                elif iNumber_spaces == 4 and (char.isnumeric() or char == '.' or char == '+' or char == '-'):
                    fLatitude += char
                # If there is another data attribute specified, it will be saved in this form
                elif iData_Attribute != 0 and iNumber_spaces == iData_Attribute and (char.isnumeric() or char == '.' or char == '+' or char == '-'):
                    fData += char
                # If there is another vector data attribute specified, it will be saved in this form
                if iVector_Data_Type != 0 and iNumber_spaces == iVector_Data_Type and (char.isnumeric() or char == '.' or char == '+' or char == '-'):
                    fVector_Data += char

            if error_flag:
                continue

            # Adds the data points to the list
            fLongitude_list.append(float(fLongitude)) # x-coord
            fLatitude_list.append(float(fLatitude))   # y-coord
            # If there are any other data attributes to be displayed, will add it to the list here
            if iData_Attribute != 0:
                fData_list.append(float(fData))
            # If there is any vector data to be displayed, will add it to the list here
            if iVector_Data_Type != 0:
                fVector_Data_list.append(float(fVector_Data))


def data_color_mapping(data_point:float):
    """

    :param data_point:
    :return:
    """
    pass

# def color_bar():
#     im = ax.imshow(np.arange(100).reshape((10,10)))
#     divider = make_axes_locatable(ax)
#     cax = divider.append_axes("right", size="5%", pad=0.05)
#     plt.colorbar(im, cax=cax)

class DataMapper:
    """ Plots all the data points for a particular attribute (ex. (lat, long, temp), (lat, long, conductivity) """

    # Remember that there are data points with NaN

    # TODO: add a method of inputting the file
    def __init__(self, file='SampleData.txt'):
        self.file = file
        self.is_heading_plotted = False
        self.is_course_plotted = False

        self.iDate_list = []
        self.fTime_list = []
        self.fLong_list = []  # x coord
        self.fLat_list = []  # y coord
        self.fShip_heading_list = []
        self.fShip_course_list = []
        self.fShip_speed_list = []
        self.fTemperature_list = []
        self.fSalinity_list = []
        self.fConductivity_list = []
        self.fFluorescence_list = []

        # ***********************************************************************
        # * MAP TILING
        # * https://scitools.org.uk/cartopy/docs/latest/gallery/eyja_volcano.html
        # * https://scitools.org.uk/cartopy/docs/v0.15/examples/eyja_volcano.html
        # * https://scitools.org.uk/cartopy/docs/v0.13/examples/eyja_volcano.html
        # ***********************************************************************
        # TODO: explore the different kinds of map tiling

        # Create a Stamen Terrain instance
        stamen_terrain = cimgt.StamenTerrain()

        # Changes the display size - specifically figsize=(x,y)
        fig = plt.figure(figsize=(10, 6))

        # Create a GeoAxes in the tile's projection
        self.ax = fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)

        # Limit the extent of the map to a specific region based on latitude/longitude
        # TODO: make the margins flexible and based on the data points
        self.ax.set_extent([-124, -113, 31, 38], crs=ccrs.Geodetic())

        # Add the Stamen data at zoom level 9
        self.ax.add_image(stamen_terrain, 8)
        # self.ax = plt.axes(projection=ccrs.PlateCarree())

        # ***********************************************************************
        # * MAP FORMATTING
        # ***********************************************************************
        # Province borders
        states_provinces = cfeature.NaturalEarthFeature(
            category='cultural',
            name='admin_1_states_provinces_lines',
            scale='50m',
            facecolor='none')
        self.ax.add_feature(states_provinces, edgecolor='gray')

        # Adding coastlines
        self.ax.coastlines(resolution='10m', color='black', linewidth=1)
            # These also work but the resolution seems to be lower
            # self.ax.add_feature(cfeature.LAND)
            # self.ax.add_feature(cfeature.COASTLINE)

        # Plots country borders
        self.ax.add_feature(cfeature.BORDERS)


    def plot_GPS(self):
        """ Plots only location data with no other attributes """

        # ***********************************************************************
        # * READING/SAVING DATA FROM FILE
        # ***********************************************************************

        # Creates lists of longitude and latitude to be passed to self.ax.plot() to be plotted
        data_parser(self.file, self.fLong_list, self.fLat_list, self.fSalinity_list, DataAttributes.SALINITY)

        # Plots all the points
        # self.ax.plot(self.fLong_list, self.fLat_list, color='b', markersize=2, transform=ccrs.PlateCarree())
        # the 3rd parameter specifies color
        # s - size, c - color
        self.ax.scatter(self.fLong_list, self.fLat_list, s=4, c=self.fSalinity_list, cmap='viridis', transform=ccrs.PlateCarree())


        # # Colorbar code - IN PROGRESS
        # # TODO: implement colorbar
        # ax2 = plt.subplot(111)
        # im = ax2.imshow(np.arange(100).reshape((10, 10)))
        # # create an axes on the right side of ax. The width of cax will be 5%
        # # of ax and the padding between cax and ax will be fixed at 0.05 inch.
        # divider = make_axes_locatable(ax2)
        # cax = divider.append_axes("right", size="5%", pad=0.05)
        # plt.colorbar(im, cax=cax)
        # p = self.ax.contourf(self.fLong_list, self.fLat_list, self.fSalinity_list[i, ...], transform=ccrs.PlateCarree(), cmap='RdBu')
        # plt.colorbar(p)



    def plot_ship_heading(self):
        """ Plots GPS data and ship heading in degrees as a vector on top of other data """
        pass

    def remove_ship_heading(self):
        ''' Removes ship's heading vectors '''
        # TODO: add check to see if the ships heading is even plotted
        pass

    def plot_ship_course(self):
        ''' Plots GPS data and ship course over ground as a vector on top of other data '''
        pass

    def remove_ship_course(self):
        """ Removes ship's course vectors """
        # TODO: add check to see if the ships course is even plotted
        pass

    def plot_speed(self):
        """ Plots GPS data and speed """
        pass

    def plot_temperature(self):
        """ Plots GPS data and temperature """
        pass

    def plot_salinity(self):
        """ Plots GPS data and salinity """
        pass

    def plot_conductivity(self):
        """ Plots GPS data and conductivity """
        pass

    def plot_fluorescence(self):
        """ Plots GPS data and fluorescence """
        pass

    def display_map(self):
        """ Call after using all plotting functions to display the map """
        plt.show()