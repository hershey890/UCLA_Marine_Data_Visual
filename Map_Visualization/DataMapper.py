# module DataMapper.py

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


class DataMapper:
    ''' Plots all the data points for a particular attribute (ex. (lat, long, temp), (lat, long, conductivity) '''

    # TODO: rember that there are data points with NaN

    def __init__(self):
        self.is_heading_plotted = False
        self.is_course_plotted = False

    def plot_GPS(self):
        ''' Plots only location data with no other attributes '''
        pass

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
