# COMPAS viewers

Standalone viewers for COMPAS based on PySide2 and PyOpenGL

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

## Questions and feedback

## Issue tracker

If you find a bug, please help us solve it by [filing a report](https://github.com/compas-dev/compas_viewers/issues).

## Contributing

## Changelog

## License
