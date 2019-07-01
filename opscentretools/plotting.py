import holoviews as hv
import geoviews as gv
import cartopy.crs as ccrs
import cartopy.feature as cf
from holoviews.operation.datashader import regrid
import panel as pn
pn.extension()
hv.extension('bokeh')

def interactive_plot(cube, cmap='viridis', coastlines=False , coastline_color='white', projection=ccrs.PlateCarree, tools=['hover'], min_height=600, **opts):
    # Generate an interactive Bokeh image of a cube with various plotting options
    
    # Convert cube to GeoViews dataset
    dataset = gv.Dataset(cube, [coord.name() for coord in cube.dim_coords], label=cube.name())
    
    # Generate an image object which will dynamically render as the interactive view changes
    image = regrid(dataset.to(gv.Image, ['longitude', 'latitude'], dynamic=True))
    
    # Options for plotting
    options = {
        'cmap': cmap,        
        'responsive': True,
        'projection': projection(),
        'colorbar': True,
        'min_height': min_height,
        'aspect': 2,
        'tools': tools
    }
    
    # Include coastlines if needed
    if coastlines:
        return gv.feature.ocean * gv.feature.land * image.opts(**options, **opts) * gv.feature.coastline.opts(line_color=coastline_color)
    else:
        return image.opts(**options, **opts)
    
def two_plot_linked_slider(plot1, plot2):
    # Generate a Panel dashboard of two plots with a shared slider
    
#     from holoviews.plotting.links import RangeToolLink
    
#     RangeToolLink(plot1, plot2)
    
    # Create a Panel object to host our plots
    app = pn.GridSpec(sizing_mode='stretch_both')
    
    # Arrange plots in a column
    plots = pn.Column(plot1, plot2)
    
    # Pull out the sliders from each plot and link them
    slider1 = plots[0][1][0]
    slider2 = plots[1][1][0]
    slider1.link(slider2, value='value')
    slider1.name = slider1.name.capitalize()
    
    # Arrange the plots vertically with a shared slider in the right hand quarter
    app[0, 0:4]=plots[0][0]
    app[1, 0:4]=plots[1][0]
    app[0, 4]=slider1
    
    return app