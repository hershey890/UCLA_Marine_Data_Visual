# module DataMapper.py
# To map a specific region, check out these links:
# https://stackoverflow.com/questions/25428512/draw-a-map-of-a-specific-country-with-cartopy
# https://github.com/SciTools/cartopy/issues/1048

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

class DataMapper:
    ''' Plots all the data points for a particular attribute (ex. (lat, long, temp), (lat, long, conductivity) '''

    # Remember that there are data points with NaN

    def __init__(self, file='SampleData.txt'):
        ''' Only used for initializing member variables '''
        self.file = file
        self.is_heading_plotted = False
        self.is_course_plotted = False

        self.ax = plt.axes(projection=ccrs.Mollweide())
        self.ax.coastlines()
        # plt.show()
        # TODO: implement a method of zooming into a particular region

        # TODO: see if there's anything I can do to zoom into the area of interest

    def plot_GPS(self):
        ''' Plots only location data with no other attributes '''

        fLong_list = []  # x coord
        fLat_list = []  # y coord

        with open(self.file, 'r') as data:
            # Iterates through lines in the file
            for line in data:

                num_space = 0
                fLongitude = ''
                fLatitude = ''
                error_flag = False

                # Reads through a single line to save the latitude and longitude
                for char in line:
                    # ERROR: if the line contains NaN just skip it
                    if char == 'N':
                        error_flag = True
                        break
                    if char == ' ':
                        num_space += 1
                    if num_space == 3:
                        fLongitude += char
                    elif num_space == 4:
                        fLatitude += char
                    elif num_space == 5:
                        break

                if error_flag:
                    continue

                # Remove the trailing comma, convert long and lat to floats, and append to the list
                fLong_list.append(float(fLongitude[:-1]))  # x-coord
                fLat_list.append(float(fLatitude[:-1]))  # y-coord

        self.ax.plot(fLong_list, fLat_list, 'bo', markersize=5, transform=ccrs.Geodetic())
        plt.show()

    def plot_ship_heading(self):
        ''' Plots GPS data and ship heading in degrees as a vector on top of other data '''
        pass

    def remove_ship_heading(self):
        ''' Removes ship's heading vectors '''
        # TODO: add check to see if the ships heading is even plotted
        pass

    def plot_ship_course(self):
        ''' Plots GPS data and ship course over ground as a vector on top of other data '''
        pass

    def remove_ship_course(self):
        ''' Removes ship's course vectors '''
        # TODO: add check to see if the ships course is even plotted
        pass

    def plot_speed(self):
        ''' Plots GPS data and speed '''
        pass

    def plot_temperature(self):
        ''' Plots GPS data and temperature '''
        pass

    def plot_salinity(self):
        ''' Plots GPS data and salinity '''
        pass

    def plot_conductivity(self):
        ''' Plots GPS data and conductivity '''
        pass

    def plot_fluorescence(self):
        ''' Plots GPS data and fluorescence '''
        pass
