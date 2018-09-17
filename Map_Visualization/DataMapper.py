# module DataMapper.py
#
# Hersh Joshi, 2018
# UCLA Electrical Engineering Class of 2021
# To contact me for any projects or opportunities, email me at hersh.joshi1@gmail.com

# TODO: add a label to the colorbar
# TODO: add vectors/arrows for ship heading and ship course
# TODO: error - 2 matplotlib instances are opened the first time anything is plotted

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
from tkinter import filedialog
from tkinter import messagebox

# Libraries used for displaying the map
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy.io.img_tiles import OSM

# Used to check internet connection
import socket

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

    def __init__(self, file:str):
        self.file = file
        # self.title = tk.
        self.is_heading_plotted = False
        self.is_course_plotted = False
        self.transformation = ccrs.PlateCarree()
        self.color_mapping = 'viridis' # TODO: psure I can use a class and ____.viridis
        self.fMin_latitude = -1
        self.fMax_latitude = -1
        self.fMin_longitude = -1
        self.fMax_longitude = -1
        self.fMap_margins = 0.05

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
        self.osm_tiles = OSM()

        # Changes the display size - specifically figsize=(x,y)
        self.fig = plt.figure(figsize=(12, 6))

        # Create a GeoAxes in the tile's projection
        self.ax = plt.axes(projection=self.osm_tiles.crs)

        # Reduces the margin sizes
        # fig.tight_layout()


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

        count = 0
        # Opens, closes and reads the file
        with open(self.file, 'r') as data:
            # Iterates through lines in the file
            for line in data:
                iNumber_commas = 0
                fLongitude = ''
                fLatitude = ''
                fData = ''
                error_flag = False
                count += 1

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
                    elif (data_attribute != DataAttributes.NO_DATA or DataAttributes.GPS) and \
                            iNumber_commas == data_attribute and \
                            (char.isnumeric() or char == '.' or char == '+' or char == '-'):
                        fData += char

                if error_flag:
                    continue

                fLatitude = float(fLatitude)
                fLongitude = float(fLongitude)

                # Sets min and max latitude/longitude bounds to be used for the map margins
                if count == 1:
                    self.fMax_latitude = fLatitude
                    self.fMin_latitude = fLatitude
                    self.fMax_longitude =fLongitude
                    self.fMin_longitude = fLongitude
                else:
                    if fLatitude > self.fMax_latitude:
                        self.fMax_latitude = fLatitude
                    elif fLatitude < self.fMin_latitude:
                        self.fMin_latitude = fLatitude
                    if fLongitude > self.fMax_longitude:
                        self.fMax_longitude = fLongitude
                    elif fLongitude < self.fMin_longitude:
                        self.fMin_longitude = fLongitude

                # Adds the data points to the list
                self.fLat_list.append(fLatitude)
                self.fLong_list.append(fLongitude)

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


    def plot_data(self, data_attribute:DataAttributes=DataAttributes.NO_DATA):
        # Parses data from file into lists such as fLong_list and fShip_speed_list
        self.__data_parser(data_attribute)

        # Limit the extent of the map to a specific region based on latitude/longitude
        self.ax.set_extent([self.fMin_longitude - self.fMap_margins, self.fMax_longitude + self.fMap_margins,
                            self.fMin_latitude - self.fMap_margins, self.fMax_latitude + self.fMap_margins],
                           crs=ccrs.PlateCarree())

        # Add the Stamen data at zoom level 12. Zoom level 1 is the most zoomed out while Zoom level 14 would be
        # most zoomed in. The most I've gotten to work is 12. Additionally, the higher the zoom level, the longer
        # the amount of time required to load the mao Finally, interpolation='spline36' makes the map render
        # better for some reason.
        self.ax.add_image(self.osm_tiles, 12, interpolation='spline36')

        # Parameter 1 - x, param 2 - y, param 3 - point size (pixels), param 4 - colors (optional),
        # param 5 - color mapping (optional)
        if data_attribute == DataAttributes.NO_DATA or data_attribute == DataAttributes.GPS:
            plt.scatter(self.fLong_list, self.fLat_list, s=6, transform=self.transformation)
            plt.title("GPS Mapping")
        elif data_attribute == DataAttributes.TEMPERATURE:
            plt.scatter(self.fLong_list, self.fLat_list, s=6, c=self.fTemperature_list, cmap=self.color_mapping,
                        transform=self.transformation)
            plt.title("Temperature")
        elif data_attribute == DataAttributes.SALINITY:
            plt.scatter(self.fLong_list, self.fLat_list, s=6, c=self.fSalinity_list, cmap=self.color_mapping,
                        transform=self.transformation)
            plt.title("Salinity")
        elif data_attribute == DataAttributes.FLUORESCENCE:
            plt.scatter(self.fLong_list, self.fLat_list, s=6, c=self.fFluorescence_list, cmap=self.color_mapping,
                        transform=self.transformation)
            plt.title("Fluorescence")
        elif data_attribute == DataAttributes.CONDUCTIVITY:
            plt.scatter(self.fLong_list, self.fLat_list, s=6, c=self.fConductivity_list, cmap=self.color_mapping,
                        transform=self.transformation)
            plt.title("Conductivity")
        elif data_attribute == DataAttributes.SHIP_SPEED_GROUND:
            plt.scatter(self.fLong_list, self.fLat_list, s=6, c=self.fShip_speed_list, cmap=self.color_mapping,
                        transform=self.transformation)
            plt.title("Ship's Speed Over Ground")
        elif data_attribute == DataAttributes.SHIP_HEADING_DEG:
            plt.scatter(self.fLong_list, self.fLat_list, s=6, c=self.fShip_heading_list, cmap=self.color_mapping,
                        transform=self.transformation)
            plt.title("Ship's Heading in Degrees")
        elif data_attribute == DataAttributes.SHIP_COURSE_GROUND:
            plt.scatter(self.fLong_list, self.fLat_list, s=6, c=self.fShip_course_list, cmap=self.color_mapping,
                        transform=self.transformation)
            plt.title("Ship's Course Over Ground")

        # Plots the colorbar for all data attributes except for GPS only
        if data_attribute != DataAttributes.NO_DATA and data_attribute != DataAttributes.GPS:
            plt.colorbar()

        # Reduces the margin sizes
        self.fig.tight_layout()

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
        self.create_widgets()
        self.master=master
        self.master.title("DataMapper")

        self.is_pressed = False
        self.is_GPS_pressed = False
        self.is_temperature_pressed = False
        self.is_fluorescence_pressed = False
        self.is_speed_pressed = False
        self.is_salinity_pressed = False
        self.is_conductivity_pressed = False
        self.is_ship_heading_pressed = False
        self.is_ship_course_pressed = False

        # Checking if connected to internet
        if not self.__connected_to_internet():
            messagebox.showerror("Error - DataMapper", "Not Connected to Internet, "
                                         "Application will not function without an internet connection")


    def create_widgets(self):
        self.message_author = tk.Message(text="_____________________________________________________________"
                                              "___________________________________________________________\n"
                                              "Created by Hersh Joshi for the UCLA Marine Operations Program, 2018"
                                              " - hersh.joshi1@gmail.com", width=600)
        self.message_author.pack(side="bottom")
        self.message2 = tk.Message(text="Plotting the map can take up to a minute. Please be patient after plotting a"
                                        "particular data attribute as a black screen will be displayed until the"
                                        "plotting is complete.", width=600)
        self.message2.pack(side="bottom")
        self.message = tk.Message(text="Please select file before beginning mapping.", width=600)
        self.message.pack(side="bottom")

        # Button for selecting the *.txt file containing the data to be inputted
        # Gets the file name as self.filename
        self.choose_file_button = tk.Button(self, text="Input File", command=self.__file_dialog)
        self.choose_file_button.pack(side="bottom")

        # Creates Button Instances
            # text: defines the text to be displayed on the button
            # command: defines the function to be executed when the button is pressed
        self.plot_GPS_button = tk.Button(self, text="GPS", state="disabled",
                                         command=(lambda: self.display_map(DataAttributes.GPS)))
        self.plot_temperature_button = tk.Button(self, text="Temperature", state="disabled",
                                                 command=(lambda: self.display_map(DataAttributes.TEMPERATURE)))
        self.plot_fluorescence_button = tk.Button(self, text="Fluorescence", state="disabled",
                                                  command=(lambda: self.display_map(DataAttributes.FLUORESCENCE)))
        self.plot_speed_button = tk.Button(self, text="Speed", state="disabled",
                                           command=(lambda: self.display_map(DataAttributes.SHIP_SPEED_GROUND)))
        self.plot_salinity_button = tk.Button(self, text="Salinity", state="disabled",
                                              command=(lambda: self.display_map(DataAttributes.SALINITY)))
        self.plot_conductivity_button = tk.Button(self, text="Conductivity", state="disabled",
                                                  command=(lambda: self.display_map(DataAttributes.CONDUCTIVITY)))
        self.plot_ship_heading_button = tk.Button(self, text="Ship Heading", state="disabled",
                                                  command=(lambda: self.display_map(DataAttributes.SHIP_HEADING_DEG)))
        self.plot_ship_course_button = tk.Button(self, text="Ship Course", state="disabled",
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


    def display_map(self, data_attribute:int):
        """ Displays a map corresponding to the the button pressed

        :param data_attribute: pass a member variable from class DataAttributes to specify the data attribute
        to be displayed
        :return: nothing
        """

        # Checking if connected to internet
        if not self.__connected_to_internet():
            messagebox.showerror("Error - DataMapper", "Not Connected to Internet, "
                                                       "Application will not function without an internet connection")

        # Matplotlib/cartopy somehow has issues plotting things multiple times, therefore after a button
        # is clicked once, the previous Map = DataMapper() instance is deleted and a new one is created
        if self.is_pressed:
            del self.Map
        else:
            self.is_pressed = True

        self.Map = DataMapper(self.filename)

        # Plots the data depending on what DataAttribute is passed to the function
        if data_attribute == DataAttributes.GPS:
            self.Map.plot_data(data_attribute=DataAttributes.GPS)
        elif data_attribute == DataAttributes.TEMPERATURE:
            self.Map.plot_data(data_attribute=DataAttributes.TEMPERATURE)
        elif data_attribute == DataAttributes.FLUORESCENCE:
            self.Map.plot_data(data_attribute=DataAttributes.FLUORESCENCE)
        elif data_attribute == DataAttributes.SALINITY:
            self.Map.plot_data(data_attribute=DataAttributes.SALINITY)
        elif data_attribute == DataAttributes.CONDUCTIVITY:
            self.Map.plot_data(data_attribute=DataAttributes.CONDUCTIVITY)
        elif data_attribute == DataAttributes.SHIP_HEADING_DEG:
            self.Map.plot_data(data_attribute=DataAttributes.SHIP_HEADING_DEG)
        elif data_attribute == DataAttributes.SHIP_COURSE_GROUND:
            self.Map.plot_data(data_attribute=DataAttributes.SHIP_COURSE_GROUND)
        elif data_attribute == DataAttributes.SHIP_SPEED_GROUND:
            self.Map.plot_data(data_attribute=DataAttributes.SHIP_SPEED_GROUND)
        else:
            print(data_attribute, "ERROR")
            # TODO: raise arn error/error dialogue box here

        # Displays the map
        self.Map.display_map()


    def __file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir = "/", title = "Select file",
                                                   filetypes=(("txt files","*.txt"),("all files","*.*")))
        self.Map = DataMapper(self.filename)
        self.plot_GPS_button.config(state="normal")
        self.plot_conductivity_button.config(state="normal")
        self.plot_salinity_button.config(state="normal")
        self.plot_fluorescence_button.config(state="normal")
        self.plot_ship_course_button.config(state="normal")
        self.plot_ship_heading_button.config(state="normal")
        self.plot_speed_button.config(state="normal")
        self.plot_temperature_button.config(state="normal")
        self.choose_file_button.config(state="disabled")

        self.file_chosen_message = tk.Message(text="File chosen: {0}".format(self.filename), width = 700)
        self.file_chosen_message.pack(side="bottom")
        self.message.destroy()


    def __connected_to_internet(self, host="8.8.8.8", port=53, timeout=3):
        """
        ...   Host: 8.8.8.8 (google-public-dns-a.google.com)
        ...   OpenPort: 53/tcp
        ...   Service: domain (DNS/TCP)
        ...   """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except Exception as ex:
            return False