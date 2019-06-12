import intake
import iris
import datetime
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import holoviews as hv
import geoviews as gv
import cartopy.crs as ccrs
import cartopy.feature as cf
import numpy as np

def boundry_presure_levels(cube):
    upper = cube.extract(
                iris.Constraint(
                    pressure=lambda p:p < cube.coord('pressure').points[0]))
    lower = cube.extract(
                    iris.Constraint(
                        pressure=lambda p:p > cube.coord('pressure').points[-1]))
    
    new_levels = (upper.coord('pressure').points +  lower.coord('pressure').points )/2
    for cube in [upper, lower]:
        cube.coord('pressure').points = new_levels
        cube.coord('pressure').bounds = None
    return upper, lower


def calculate_shear(wind_speed, wind_dir):
    # Calculate the cross-product of wind vectors between consecutive pressure levels
    
    # lets ensure we are working on the same coords on both cubes
    assert wind_speed.coord_dims('pressure') == wind_dir.coord_dims('pressure')
    
    # make copies of cubes
    speed = wind_speed.copy()
    direction = wind_dir.copy()
    
    # work out the parameters for the 
    speed_lower, speed_upper = boundry_presure_levels(speed)
    dir_lower, dir_upper = boundry_presure_levels(direction)
    
    x_lower = speed_lower * iris.analysis.maths.apply_ufunc(np.cos, dir_lower)
    y_lower = speed_lower * iris.analysis.maths.apply_ufunc(np.sin, dir_lower)
    x_upper = speed_upper * iris.analysis.maths.apply_ufunc(np.cos, dir_upper)
    y_upper = speed_upper * iris.analysis.maths.apply_ufunc(np.sin, dir_upper)

    x_diff = x_upper - x_lower
    y_diff = y_upper - y_lower
    shear = (x_diff**2 + y_diff**2)**0.5
    
    # rename cube and add units
    shear.long_name = "Wind Shear"
    shear.units = "m s-1"
    
    return shear