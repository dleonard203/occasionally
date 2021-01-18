#!/bin/bash

function get_version() {
    res=$(grep version setup.py | cut -d '=' -f 2 | sed 's/\"//g;s/v//;s/,//')
    echo $res
}

version=`get_version`

# start clean
rm -rf build dist occasionally.egg-info

python setup.py  bdist_wheel
pip uninstall --yes occasionally
pip install dist/occasionally-$version-py2-none-any.whl
pytest -v -m "not slow"
