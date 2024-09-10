#!/bin/bash

# Set the variable
local=false

if [ "$local" = false ]; then
    python_bin="/usr/local/bin/python3"
else
    python_bin="python3" 
fi

echo "Using Python binary: $python_bin"

$python_bin Step2-Login.py
$python_bin Step3-GetDate.py
$python_bin Step4-GetOrders.py
$python_bin Step5-UploadOrders.py