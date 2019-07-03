[![Binder](https://binder.pangeo.io/badge_logo.svg)](https://binder.pangeo.io/v2/gh/informatics-lab/windshear_hero_demo/master?urlpath=lab/tree/wind_shear.ipynb)

# Windshear Hero Demo
Example of how to use the latest Informatics Lab tools to communicate a weather forecast.

## Setup
First, clone this repository:

```
git clone https://github.com/informatics-lab/windshear_hero_demo.git
cd windshear_hero_demo
```

Create a conda environment with the accompanied `environment.yml`:

```conda create --name windshear_hero_demo --file environment.yml --yes```

If you are using Jupyter Lab then you also need to install the an extension:

```
jupyter labextension install /
@jupyter-widgets/jupyterlab-manager \
@pyviz/jupyterlab_pyviz \
dask-labextension \
itk-jupyter-widgets \
jupyter-matplotlib \
jupyterlab-datawidgets \
jupyterlab_bokeh 
```

## Launch demo using Binder
This notebook can be run from the [Pangeo Binder](https://binder.pangeo.io/) service at:

https://binder.pangeo.io/v2/gh/informatics-lab/windshear_hero_demo/binder?urlpath=lab/tree/wind_shear.ipynb

If you wish to run it locally, first clone this git repository (see above) then:

```jupyter notebook windshear_hero_demo.ipynb```

Or if you are using Jupyter Lab:

```jupyter lab```
