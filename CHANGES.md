### 0.1.0

* Provide `moreshell` package with:

  * `IPython_magic_module` wrapper class and accomanying
    `load_magic_modules` function, the latter to be used in
    `load_ipython_extension` handler functions
  * `IPython_magic` and `IPython_cell_magic` function decorators for
    creating the actual magic, accompanied by the `with_arguments`
    helper function for defining magic command line options based on
    `argparse.ArgumentParser`
  * `IPythonMagicExit` exception, raised on magic argument errors
