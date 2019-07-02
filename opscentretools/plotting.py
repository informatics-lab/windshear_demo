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

def dashboard_column(plots, shared_slider=False):
    # Generate a Panel dashboard from a list of interactive plots
    
    # Create a Panel object to host our plots
    app = pn.GridSpec(sizing_mode='stretch_both')
    
    # Arrange plots in a column
    column = pn.Column(*plots)
    
    # Add plots and sliders to Panel app
    if shared_slider:
        # Link all the sliders to one slider
        # TODO: Add check for whether sliders can be linked
        slider1 = column[0][1][0]
        for plot in column[1:]:
            slider = plot[1][0]
            slider1.link(slider, value='value')
        # Append all the plots to the app (using 3/4 of the horizontal space)
        for i, plot in enumerate(column):
            app[i, 0:4] = plot[0]
        # Add the linked slider (using the last 1/4 of the horizontal space)
        app[0, 4] = slider1
    else:
        # Append whole column (with individual sliders) to the app
        app[0, 0] = column
    
    return app
