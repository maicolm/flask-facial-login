#!/usr/bin/env bash
echo "Usando Python $(python --version)"
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt