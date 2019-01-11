#!/bin/sh
cp header.rst README.rst

poetry run jupyter nbconvert --stdout --to rst readme.ipynb >> README.rst
sed 's/code:: ipython3/code:: python/' -i README.rst
