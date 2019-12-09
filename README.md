# COMPAS viewers

Standalone viewers for COMPAS based on PySide2 and PyOpenGL.

The package provides base functionality for making viewers and minimal CAD-style applications.
It also implements this base functionality in the following pre-configured viewers/apps:

* `MeshViewer`: A viewer for individual COMPAS meshes.
* `MultiMeshViewer`: A viewer for multiple mesh objects with a first draft of an object manager for selecting and working with individual mesh objects.

The goal is to provide an environment for testing and prototyping code for 3D applications without restrictions on functionality due to limited availability of Python packages or external libraries (as for example in IronPython), and without the need for integration in CAD software.

**Note that the functionality in this package is under active development and still quite experimental and therefore subject to frequent change.**

## Installation

The recommended way to install `compas_viewers` is with [Anaconda/conda](https://conda.io/docs/) in a dedicated environment.

1. Create an environment

   If you don't have an environment set up, create a new one first.

   ```bash
   conda create -n viewers python=3.7
   ```

2. Activate environment

   Activate the environment in which you want to install `compas_viewers`.

   ```bash
   conda activate viewers
   ```

3. Install COMPAS

   `compas_viewers` builds upon `compas`, so make sure you have a recent version installed in the environment.

   ```bash
   conda install COMPAS
   ```

   Or install `compas` from source.

   ```bash
   cd path/to/compas
   pip install -e .
   ```

4. Install requirements

   ```bash
   conda install PySide2 PyOpenGL
   ```

   > <https://block.arch.ethz.ch/blog/2016/10/pyopengl-glut-error/>

5. Install `compas_viewers`

   ```bash
   cd path/to/compas_viewers
   pip install -e .
   ```

## Verify installation

To verify your installation, start Python from the command line and run the following:

```python
>>> import compas
>>> import compas_viewers
```

## Getting started

Have a look at [the examples](https://github.com/compas-dev/compas_viewers/tree/master/examples) to get going.

## Issue tracker

If you find a bug, please help us solve it by [filing a report](https://github.com/compas-dev/compas_viewers/issues).

## Contributing

Contributions are very welcome and highly appreciated. Also feature requests or suggestions for future development are helpful.

## License

`compas_viewers` is released under the MIT License.
