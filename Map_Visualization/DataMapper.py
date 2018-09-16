# module DataMapper.py
# To map a specific region, check out these links:
# https://stackoverflow.com/questions/25428512/draw-a-map-of-a-specific-country-with-cartopy
# https://github.com/SciTools/cartopy/issues/1048
# Code for downloading tiles for mapping online: https://scitools.org.uk/cartopy/docs/latest/gallery/eyja_volcano.html

# TODO: make a GUI that allows for more flexible movement of the plot
# TODO: get a high quality map of LA/CA region
# TODO: add a label to the colorbar
# TODO: add vectors/arrows for ship heading and ship course
# TODO: add descriptions/text to the GUI at the start
# TODO: add a error dialogue box if there are issues
# TODO: add something to the GUI that allows you to select a file through there
# TODO: change the name of the window for the map, i.e. more descriptive than "Figure 1"

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

# Libraries used for the tkinter GUI that pops up before the map pops up
import tkinter as tk

# Libraries used for displaying the map
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy.io.img_tiles import OSM

class DataAttributes(int):
    """ Substitute for enumeration """
    NO_DATA             = -1
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
    GPS                 = 12


class DataMapper:
    """ Plots all the data points for a particular attribute (ex. (lat, long, temp), (lat, long, conductivity) """

    # TODO: add a method of inputting the file
    def __init__(self, file='SampleData.txt'):
        self.file = file
        self.is_heading_plotted = False
        self.is_course_plotted = False
        self.transformation = ccrs.PlateCarree()
        self.color_mapping = 'viridis' # TODO: psure I can use a class and ____.viridis

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
        # * MAP SETUP
        # ***********************************************************************

        # Get map tiles from the OpenStreetMap Server, map tiles allow for maps to be loaded from servers
        osm_tiles = OSM()

        # Changes the display size - specifically figsize=(x,y)
        fig = plt.figure(figsize=(12, 6))

        # Create a GeoAxes in the tile's projection
        self.ax = plt.axes(projection=osm_tiles.crs)

        # Reduces the margin sizes
        fig.tight_layout()

        # Limit the extent of the map to a specific region based on latitude/longitude
        # TODO: make the margins flexible and based on the data points
        self.ax.set_extent([-118.54, -118.35, 33.715, 34.02], crs=ccrs.PlateCarree())

        # Add the Stamen data at zoom level 12. Zoom level 1 is the most zoomed out while Zoom level 14 would be
        # most zoomed in. The most I've gotten to work is 12. Additionally, the higher the zoom level, the longer
        # the amount of time required to load the mao Finally, interpolation='spline36' makes the map render
        # better for some reason.
        self.ax.add_image(osm_tiles, 12, interpolation='spline36')

    # TODO: can simplify this function, there's no need to pass so many lists to it, I can return multiple lists!
    def __data_parser(self, data_attribute:DataAttributes=DataAttributes.NO_DATA):
        """ Reads the data from the .txt file and stores it in a list for longitude and one for latitude

        :param file: string containing the name of the file with the sensor data (must contain the file extension .txt)
        :param fLongitude_list: pass an empty list that will be filled with all the longitudinal data points
        :param fLatitude_list: pass an empty list that will be filled with all the latitude data points
        :param fData_list: stores an optional data attribute to be displayed (i.e. temperature, salinity,
               conductivity, fluorescence), ex. DataAttributes.SALINITY
        :param iData_Attribute: pass a member variables (8-11) from DataAttributes to determine which one is plotted
        :return: void - modifies the lists passed to the function
        """

        # Opens, closes and reads the file
        with open(self.file, 'r') as data:
            # Iterates through lines in the file
            for line in data:
                iNumber_commas = 0
                fLongitude = ''
                fLatitude = ''
                fData = ''
                error_flag = False

                # Reads through a single line to save the latitude and longitude
                for char in line:
                    # ERROR: if the line contains NaN just skip it
                    if char == 'N':
                        error_flag = True
                        break
                    if char == ',':
                        iNumber_commas += 1
                    elif iNumber_commas == 3 and (char.isnumeric() or char == '.' or char == '+' or char == '-'):
                        fLongitude += char
                    elif iNumber_commas == 4 and (char.isnumeric() or char == '.' or char == '+' or char == '-'):
                        fLatitude += char
                    # If there is another data attribute specified, it will be saved in this form
                    elif data_attribute != DataAttributes.NO_DATA and iNumber_commas == data_attribute and \
                            (char.isnumeric() or char == '.' or char == '+' or char == '-'):
                        fData += char

                if error_flag:
                    continue

                # Adds the data points to the list
                self.fLat_list.append(float(fLatitude))
                self.fLong_list.append(float(fLongitude))

                # If there are any other data attributes to be displayed, will add it to the list here
                if data_attribute == DataAttributes.TEMPERATURE:
                    self.fTemperature_list.append(float(fData))
                elif data_attribute == DataAttributes.SALINITY:
                    self.fSalinity_list.append(float(fData))
                elif data_attribute == DataAttributes.FLUORESCENCE:
                    self.fFluorescence_list.append(float(fData))
                elif data_attribute == DataAttributes.CONDUCTIVITY:
                    self.fConductivity_list.append(float(fData))
                elif data_attribute == DataAttributes.SHIP_SPEED_GROUND:
                    self.fShip_speed_list.append(float(fData))
                elif data_attribute == DataAttributes.SHIP_HEADING_DEG:
                    self.fShip_heading_list.append(float(fData))
                elif data_attribute == DataAttributes.SHIP_COURSE_GROUND:
                    self.fShip_course_list.append(float(fData))


    def plot_GPS(self):
        """ Plots only location data with no other attributes """

        # Creates lists of longitude and latitude to be passed to self.ax.plot() to be plotted
        # self.__data_parser(self.file, self.fLong_list, self.fLat_list)
        self.__data_parser()

        # Plots all the points
        # self.ax.plot(self.fLong_list, self.fLat_list, color='b', markersize=2, transform=ccrs.PlateCarree())
        plt.scatter(self.fLong_list, self.fLat_list, s=6, transform=self.transformation)



    def plot_ship_heading(self):
        """ Plots GPS data and ship heading in degrees as a vector on top of other data """

        # Creates lists of longitude and latitude to be passed to self.ax.plot() for plotting along with the ship's course
        # self.__data_parser(self.file, self.fLong_list, self.fLat_list, self.fShip_heading_list,
        #             DataAttributes.SHIP_COURSE_GROUND)

        self.__data_parser(data_attribute=DataAttributes.SHIP_HEADING_DEG)

        # Plots the data
        # Parameter 1 - x, param 2 - y, param 3 - point size (pixels), param 4 - colors, param 5 - color mapping
        plt.scatter(self.fLong_list, self.fLat_list, s=6, c=self.fShip_heading_list, cmap=self.color_mapping,
                    transform=self.transformation)
        # Displays the colorbar
        plt.colorbar()


    def plot_ship_course(self):
        """ Plots GPS data and ship course over ground as a vector on top of other data """

        # Creates lists of longitude and latitude to be passed to self.ax.plot() for plotting along with the ship's course
        self.__data_parser(data_attribute=DataAttributes.SHIP_COURSE_GROUND)

        # Plots the data
        # Parameter 1 - x, param 2 - y, param 3 - point size (pixels), param 4 - colors, param 5 - color mapping
        plt.scatter(self.fLong_list, self.fLat_list, s=6, c=self.fShip_course_list, cmap=self.color_mapping,
                    transform=self.transformation)

        # Displays the colorbar
        plt.colorbar()


    def plot_speed(self):
        """ Plots GPS data and speed """

        # Creates lists of longitude and latitude to be passed to self.ax.plot() to be plotted along with speed
        self.__data_parser(data_attribute=DataAttributes.SHIP_SPEED_GROUND)

        # Plots the data
        # Parameter 1 - x, param 2 - y, param 3 - point size (pixels), param 4 - colors, param 5 - color mapping
        plt.scatter(self.fLong_list, self.fLat_list, s=6, c=self.fShip_speed_list, cmap=self.color_mapping,
                    transform=self.transformation)

        # Displays the colorbar
        plt.colorbar()

    def plot_temperature(self):
        """ Plots GPS data and temperature """

        # Creates lists of longitude and latitude to be passed to self.ax.plot() to be plotted along with temperature
        self.__data_parser(data_attribute=DataAttributes.TEMPERATURE)

        # Plots the data
        # Parameter 1 - x, param 2 - y, param 3 - point size (pixels), param 4 - colors, param 5 - color mapping
        plt.scatter(self.fLong_list, self.fLat_list, s=6, c=self.fTemperature_list, cmap=self.color_mapping,
                    transform=self.transformation)

        # Displays the colorbar
        plt.colorbar()

    def plot_salinity(self):
        """ Plots GPS data and salinity """

        # Creates lists of longitude and latitude to be passed to self.ax.plot() to be plotted along with salinity
        self.__data_parser(data_attribute=DataAttributes.SALINITY)

        # Plots the data
        # Parameter 1 - x, param 2 - y, param 3 - point size (pixels), param 4 - colors, param 5 - color mapping
        plt.scatter(self.fLong_list, self.fLat_list, s=6, c=self.fSalinity_list, cmap=self.color_mapping,
                    transform=self.transformation)

        # Displays the colorbar
        plt.colorbar()

    def plot_conductivity(self):
        """ Plots GPS data and conductivity """

        # Creates lists of longitude and latitude to be passed to self.ax.plot() to be plotted along with conductivity
        self.__data_parser(data_attribute=DataAttributes.CONDUCTIVITY)

        # Plots the data
        # Parameter 1 - x, param 2 - y, param 3 - point size (pixels), param 4 - colors, param 5 - color mapping
        plt.scatter(self.fLong_list, self.fLat_list, s=6, c=self.fConductivity_list, cmap=self.color_mapping,
                    transform=self.transformation)

        # Displays the colorbar
        plt.colorbar()

    def plot_fluorescence(self):
        """ Plots GPS data and fluorescence """

        # Creates lists of longitude and latitude to be passed to self.ax.plot() to be plotted along with fluorescence
        self.__data_parser(data_attribute=DataAttributes.FLUORESCENCE)

        # Plots the data
        # Parameter 1 - x, param 2 - y, param 3 - point size (pixels), param 4 - colors, param 5 - color mapping
        plt.scatter(self.fLong_list, self.fLat_list, s=6, c=self.fFluorescence_list, cmap=self.color_mapping,
                    transform=self.transformation)
        # Displays the colorbar
        plt.colorbar()

    def display_map(self):
        """ Call after using all plotting functions to display the map """
        plt.show()


class GUI(tk.Frame):
    """Creates a GUI to allow the user to use the functions from the DataMapper class without having to look at code.

    Code based on examples from: https://docs.python.org/3/library/tkinter.html
    """

    def __init__(self, master=tk.Tk()):
        super().__init__(master)
        self.pack()
        self.Map = DataMapper()
        self.create_widgets()
        self.master=master


        self.is_pressed = False
        self.is_GPS_pressed = False
        self.is_temperature_pressed = False
        self.is_fluorescence_pressed = False
        self.is_speed_pressed = False
        self.is_salinity_pressed = False
        self.is_conductivity_pressed = False
        self.is_ship_heading_pressed = False
        self.is_ship_course_pressed = False


    def create_widgets(self):
        # Creates Button Instances
            # text: defines the text to be displayed on the button
            # command: defines the function to be executed when the button is pressed
        self.plot_GPS_button = tk.Button(self, text="GPS", command=(lambda: self.display_map(DataAttributes.GPS)))
        self.plot_temperature_button = tk.Button(self, text="Temperature",
                                                 command=(lambda: self.display_map(DataAttributes.TEMPERATURE)))
        self.plot_fluorescence_button = tk.Button(self, text="Fluorescence",
                                                  command=(lambda: self.display_map(DataAttributes.FLUORESCENCE)))
        self.plot_speed_button = tk.Button(self, text="Speed",
                                           command=(lambda: self.display_map(DataAttributes.SHIP_SPEED_GROUND)))
        self.plot_salinity_button = tk.Button(self, text="Salinity",
                                              command=(lambda: self.display_map(DataAttributes.SALINITY)))
        self.plot_conductivity_button = tk.Button(self, text="Conductivity",
                                                  command=(lambda: self.display_map(DataAttributes.CONDUCTIVITY)))
        self.plot_ship_heading_button = tk.Button(self, text="Ship Heading",
                                                  command=(lambda: self.display_map(DataAttributes.SHIP_HEADING_DEG)))
        self.plot_ship_course_button = tk.Button(self, text="Ship Course",
                                                 command=(lambda: self.display_map(DataAttributes.SHIP_COURSE_GROUND)))

        # Positions the buttons within the window
        self.plot_GPS_button.pack(side="left", padx=5, pady=5)
        self.plot_temperature_button.pack(side="left", padx=5, pady=5)
        self.plot_fluorescence_button.pack(side="left", padx=5, pady=5)
        self.plot_speed_button.pack(side="left", padx=5, pady=5)
        self.plot_salinity_button.pack(side="left", padx=5, pady=5)
        self.plot_conductivity_button.pack(side="left", padx=5, pady=5)
        self.plot_ship_heading_button.pack(side="left", padx=5, pady=5)
        self.plot_ship_course_button.pack(side="left", padx=5, pady=5)

        # Button for quitting(ending) the application
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom", padx=5, pady=5)


    def plot_GPS(self):
        if not self.is_GPS_pressed:
            print("button pressed")
            # root.destroy()
            self.Map.plot_GPS()
            self.Map.display_map()
            self.is_GPS_pressed = True
        else:
            print("button pressed 2")
            del self.Map
            self.Map = DataMapper()
            self.Map.plot_GPS()
            self.Map.display_map()

    def display_map(self, data_attribute:int):
        """ Displays a map corresponding to the the button pressed

        :param data_attribute: pass a member variable from class DataAttributes to specify the data attribute
        to be displayed
        :return: nothing
        """
        # Matplotlib/cartopy somehow has issues plotting things multiple times, therefore after a button
        # is clicked once, the previous Map = DataMapper() instance is deleted and a new one is created
        if self.is_pressed:
            del self.Map
            self.Map = DataMapper()
        else:
            self.is_pressed = True

        # Plots the data depending on what DataAttribute is passed to the function
        if data_attribute == DataAttributes.GPS:
            self.Map.plot_GPS()
        elif data_attribute == DataAttributes.TEMPERATURE:
            self.Map.plot_temperature()
        elif data_attribute == DataAttributes.FLUORESCENCE:
            self.Map.plot_fluorescence()
        elif data_attribute == DataAttributes.SALINITY:
            self.Map.plot_salinity()
        elif data_attribute == DataAttributes.CONDUCTIVITY:
            self.Map.plot_conductivity()
        elif data_attribute == DataAttributes.SHIP_HEADING_DEG:
            self.Map.plot_ship_heading()
        elif data_attribute == DataAttributes.SHIP_COURSE_GROUND:
            self.Map.plot_ship_course()
        elif data_attribute == DataAttributes.SHIP_SPEED_GROUND:
            self.Map.plot_ship_course()
        else:
            print(data_attribute, "ERROR")
            # TODO: raise arn error/error dialogue box here

        # Displays the map
        self.Map.display_map()

# root = tk.Tk()
# app = GUI(master=root)
# app.mainloop()