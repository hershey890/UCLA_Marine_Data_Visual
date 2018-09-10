# module DataMapper.py
# To map a specific region, check out these links:
# https://stackoverflow.com/questions/25428512/draw-a-map-of-a-specific-country-with-cartopy
# https://github.com/SciTools/cartopy/issues/1048

# TODO: have a background img/map
# TODO: use folium to have dynamic maps
# TODO: make a GUI that allows for more flexible movement of the plot (this may require folium)
# TODO: increased res on the borders
# TODO: labels on the map
# TODO: hq map of LA/CA region

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
# from matplotlib.offsetbox import AnchoredText
import cartopy.io.img_tiles as cimgt

class DataMapper:
    ''' Plots all the data points for a particular attribute (ex. (lat, long, temp), (lat, long, conductivity) '''

    # Remember that there are data points with NaN

    def __init__(self, file='SampleData.txt'):
        ''' Only used for initializing member variables '''
        self.file = file
        self.is_heading_plotted = False
        self.is_course_plotted = False

        stamen_terrain = cimgt.StamenTerrain()

        # Changes the display size
        fig = plt.figure(figsize=(10, 6))

        self.ax = fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)

        # Sets the margins for the plot
        # TODO: make the margins flexible and based on the data points
        self.ax.set_extent([-124, -113, 31, 38], crs=ccrs.Geodetic())

        self.ax.add_image(stamen_terrain, 8)


        # self.ax = plt.axes(projection=ccrs.PlateCarree())

    def plot_GPS(self):
        ''' Plots only location data with no other attributes '''

        # READING/SAVING DATA FROM FILE
        #################################################################
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
                # TODO: I can prob just use the index/column instead of a for loop this big
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

        # MAP FORMATTING
        #################################################################
        # Background stock image
        # describes the how to add a background img, it requires a .json file http://earthpy.org/cartopy_backgroung.html
        # self.ax.stock_img()
        # TODO: have a better background stock

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

        # Plots all the points
        self.ax.plot(fLong_list, fLat_list, 'bo', markersize=2, transform=ccrs.Geodetic())

        plt.show() # I can prob remove this and have a display function at the end/

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
