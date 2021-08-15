#!/bin/bash

# TEST
pytest --cov=bt_button --cov-branch --cov-report=term-missing --cov-report=html

# LINT
flake8
