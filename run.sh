#!/usr/bin/env bash

pushd ui

  pyuic5 mainwindow.ui -o mainwindow.py

popd

python ./main.py