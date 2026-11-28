#!/usr/bin/env bash
set -e

echo "#####################################"
echo "#                                   #"
echo "#         gui2terminal              #"
echo "#                                   #"
echo "#####################################"
echo ""
echo ""
echo "Installaition..."
echo ""

read -r -p "do u want to install Phython (Y / n): " answer

case "$answer" in
    [Yy]|[Yy][Ee][Ss]|"")
        echo "Installing Phython"
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-tk

        echo "Installing abhänigkeit"
        echo "Installing"
        python3 -m pip install --break-system-packages psutil
        ;;
    [Nn]|[Nn][Oo])
        echo "Skipping Python installation."
        ;;
    *)
        echo "Invalid input. Please run again and enter Y or n."
        exit 1
        ;;
esac