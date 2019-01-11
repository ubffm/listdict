#!/bin/sh
cp header.rst README.rst

poetry run jupyter nbconvert --stdout --to rst readme.ipynb >> README.rst
