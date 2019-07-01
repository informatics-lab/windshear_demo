import holoviews as hv
import geoviews as gv
import cartopy.crs as ccrs
import cartopy.feature as cf
from holoviews.operation.datashader import regrid
import panel as pn
pn.extension()
hv.extension('bokeh')

def interactive_plot(cube, cmap='viridis', coastlines=True, coastline_color='grey', projection=ccrs.PlateCarree, tools=['hover'], min_height=600, **opts):
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