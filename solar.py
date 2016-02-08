# -*- coding: utf-8 -*-
"""
utci calculator

partially borrowed from:
https://github.com/pingswept/pysolar
"""

import math
import time

earth_axis_inclination = 23.45 # degrees

def get_radiation_cloud(when, altitude_deg, cloud_ratio):
    # http://www.shodor.org/os411/courses/_master/tools/calculators/solarrad/
    rad_direct = get_radiation_direct(when, altitude_deg)
    return rad_direct*(1 - 0.75*pow(cloud_ratio, 3.4))

def get_radiation_direct(when, altitude_deg):
    # from Masters, p. 412
    if(altitude_deg < 0): return 0.0
    
    day = when.utctimetuple().tm_yday
    flux = get_apparent_extraterrestrial_flux(day)
    optical_depth = get_optical_depth(day)
    air_mass_ratio = get_air_mass_ratio(altitude_deg)
    return flux * math.exp(-1 * optical_depth * air_mass_ratio)

def get_air_mass_ratio(altitude_deg):
    # from Masters, p. 412
    try :
        result = 1 / math.sin(math.radians(altitude_deg))
    except ZeroDivisionError :
        result = float("inf")
    #end try
    return result

def get_optical_depth(day):
    # from Masters, p. 412
    return 0.174 + (0.035 * math.sin(2 * math.pi / 365 * (day - 100)))

def get_apparent_extraterrestrial_flux(day):
    # from Masters, p. 412
    return 1160 + (75 * math.sin(2 * math.pi / 365 * (day - 275)))

def get_altitude(latitude_deg, longitude_deg, when):
    # expect 19 degrees for solar.get_altitude(42.364908,-71.112828,datetime.datetime(2007, 2, 18, 20, 13, 1, 130320))
    day = when.utctimetuple().tm_yday
    declination_rad = math.radians(get_declination(day))
    latitude_rad = math.radians(latitude_deg)
    hour_angle = get_hour_angle(when, longitude_deg)
    first_term = math.cos(latitude_rad) * math.cos(declination_rad) * math.cos(math.radians(hour_angle))
    second_term = math.sin(latitude_rad) * math.sin(declination_rad)
    return math.degrees(math.asin(first_term + second_term))

def get_declination(day):
    '''The declination of the sun is the angle between
    Earth's equatorial plane and a line between the Earth and the sun.
    The declination of the sun varies between 23.45 degrees and -23.45 degrees,
    hitting zero on the equinoxes and peaking on the solstices.
    '''
    return earth_axis_inclination * math.sin((2 * math.pi / 365.0) * (day - 81))

def get_hour_angle(when, longitude_deg):
    # http://www.pveducation.org/pvcdrom/properties-of-sunlight/suns-position
    solar_time = get_solar_time(longitude_deg, when)
    #print solar_time
    return 15 * (solar_time - 12)

def get_solar_time(longitude_deg, when):
    '''returns solar time in hours for the specified longitude and time,
    accurate only to the nearest minute.'''
    when = when.utctimetuple()
    #return ((when.tm_hour * 60 + when.tm_min + 4 * longitude_deg + equation_of_time(when.tm_yday))/60)
    dt_gmt = -time.timezone/3600    
    lstm_deg = 15*dt_gmt
    eot = equation_of_time(when.tm_yday)
    tc = 4*(longitude_deg - lstm_deg) + eot
    #print dt_gmt, lstm_deg, eot, tc
    return (when.tm_hour*60 + when.tm_min + when.tm_sec/60 + tc/60)/60

def equation_of_time(day):
    #returns the number of minutes to add to mean solar time to get actual solar time.
    b = 2 * math.pi / 364.0 * (day - 81)
    return 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)