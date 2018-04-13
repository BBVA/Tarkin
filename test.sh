#!/bin/bash

flake8
PYTHONPATH=$(pwd) py.test --cov-report term-missing --cov=Tarkin
