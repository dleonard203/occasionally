#!/bin/bash

python setup.py  bdist_wheel
pip uninstall --yes occasionally
pip install dist/occasionally-0.0.0-py2-none-any.whl
pytest -v