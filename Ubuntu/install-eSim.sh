#!/bin/bash 
#=============================================================================
#          FILE: install-eSim.sh
# 
#         USAGE: ./install-eSim.sh --install 
#                            OR
#                ./install-eSim.sh --uninstall
#                
#   DESCRIPTION: Installation script for eSim EDA Suite
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#       AUTHORS: Fahim Khan, Rahul Paknikar, Saurabh Bansode,
#                Sumanto Kar, Partha Singha Roy
#  ORGANIZATION: eSim Team, FOSSEE, IIT Bombay
#       CREATED: Wednesday 15 July 2015 15:26
#      REVISION: Thursday 29 June 2023 12:50
#=============================================================================

# All variables go here
config_dir="$HOME/.esim"
config_file="config.ini"
eSim_Home=`pwd`
ngspiceFlag=0

## All Functions go here

error_exit()
{
    echo -e "\n\nError! Kindly resolve the above error(s) and try again."
    echo -e "\nAborting Installation...\n"
}

function createConfigFile
{
    # Creating config.ini file and adding configuration information
    # Check if config file is present
    if [ -d $config_dir ];then
        rm $config_dir/$config_file && touch $config_dir/$config_file
    else
        mkdir $config_dir && touch $config_dir/$config_file
    fi
    
    echo "[eSim]" >> $config_dir/$config_file
    echo "eSim_HOME = $eSim_Home" >> $config_dir/$config_file
    echo "LICENSE = %(eSim_HOME)s/LICENSE" >> $config_dir/$config_file
    echo "KicadLib = %(eSim_HOME)s/library/kicadLibrary.tar.xz" >> $config_dir/$config_file
    echo "IMAGES = %(eSim_HOME)s/images" >> $config_dir/$config_file
    echo "VERSION = %(eSim_HOME)s/VERSION" >> $config_dir/$config_file
    echo "MODELICA_MAP_JSON = %(eSim_HOME)s/library/ngspicetoModelica/Mapping.json" >> $config_dir/$config_file
}

function installNghdl
{
    echo "Installing NGHDL..........................."
    unzip -o nghdl.zip
    cd nghdl/
    chmod +x install-nghdl.sh

    # Do not trap on error of any command. Let NGHDL script handle its own errors.
    trap "" ERR

    ./install-nghdl.sh --install       # Install NGHDL
        
    # Set trap again to error_exit function to exit on errors
    trap error_exit ERR

    ngspiceFlag=1
    cd ../
}

function installSky130Pdk
{
    echo "Installing SKY130 PDK......................"
    
    # Extract SKY130 PDK
    tar -xJf library/sky130_fd_pr.tar.xz

    # Remove any previous sky130-fd-pr instance, if any
    sudo rm -rf /usr/share/local/sky130_fd_pr

    # Copy SKY130 library
    echo "Copying SKY130 PDK........................."

    sudo mkdir -p /usr/share/local/
    sudo mv sky130_fd_pr /usr/share/local/

    # Change ownership from root to the user
    sudo chown -R $USER:$USER /usr/share/local/sky130_fd_pr/
}

function installKicad
{
    echo "Installing KiCad..........................."

    kicadppa="kicad/kicad-6.0-releases"
    findppa=$(grep -h -r "^deb.*$kicadppa*" /etc/apt/sources.list* > /dev/null 2>&1 || test $? = 1)
    if [ -z "$findppa" ]; then
        echo "Adding KiCad-6 ppa to local apt-repository"
        sudo add-apt-repository -y ppa:kicad/kicad-6.0-releases
        sudo apt-get update
    else
        echo "KiCad-6 is available in synaptic"
    fi

    sudo apt-get install -y --no-install-recommends kicad kicad-footprints kicad-libraries kicad-symbols kicad-templates
}

function installDependency
{
    set +e      # Temporary disable exit on error
    trap "" ERR # Do not trap on error of any command

    # Update apt repository
    echo "Updating apt index files..................."
    sudo apt-get update
    
    set -e      # Re-enable exit on error
    trap error_exit ERR
    
    echo "Installing Xterm..........................."
    sudo apt-get install -y xterm
    
    echo "Installing Psutil.........................."
    sudo apt-get install -y python3-psutil
    
    echo "Installing PyQt5..........................."
    sudo apt-get install -y python3-pyqt5

    echo "Installing Matplotlib......................"
    sudo apt-get install -y python3-matplotlib

    echo "Installing Distutils......................."
    sudo apt-get install -y python3-distutils

    # Install NgVeri Dependencies
    echo "Installing Pip3............................"
    sudo apt install -y python3-pip

    echo "Installing Watchdog........................"
    pip3 install watchdog

    echo "Installing Hdlparse........................"
    pip3 install --upgrade https://github.com/hdl/pyhdlparser/tarball/master

    echo "Installing Makerchip......................."
    pip3 install makerchip-app

    echo "Installing SandPiper Saas.................."
    pip3 install sandpiper-saas

    echo "Installing LLVM-15.........................."
    sudo apt-get install -y llvm-15 llvm-15-dev
}

function copyKicadLibrary
{
    # Extract custom KiCad Library
    tar -xJf library/kicadLibrary.tar.xz

    if [ -d ~/.config/kicad/6.0 ];then
        echo "kicad config folder already exists"
    else 
        echo ".config/kicad/6.0 does not exist"
        mkdir -p ~/.config/kicad/6.0
    fi

    # Copy symbol table for eSim custom symbols 
    cp kicadLibrary/template/sym-lib-table ~/.config/kicad/6.0/
    echo "symbol table copied in the directory"

    # Copy KiCad symbols made for eSim
    sudo cp -r kicadLibrary/eSim-symbols/* /usr/share/kicad/symbols/

    set +e      # Temporary disable exit on error
    trap "" ERR # Do not trap on error of any command
    
    # Remove extracted KiCad Library - not needed anymore
    rm -rf kicadLibrary

    set -e      # Re-enable exit on error
    trap error_exit ERR

    # Change ownership from Root to the User
    sudo chown -R $USER:$USER /usr/share/kicad/symbols/
}

function uninstall
{
    echo "Uninstalling eSim.........................."
    sudo rm -rf /usr/share/local/sky130_fd_pr
    sudo rm -rf ~/.config/kicad/6.0/sym-lib-table
    sudo rm -rf /usr/share/kicad/symbols/*
    sudo apt-get remove -y llvm-15 llvm-15-dev xterm python3-psutil python3-pyqt5 python3-matplotlib python3-distutils
    pip3 uninstall -y watchdog pyhdlparser makerchip-app sandpiper-saas
    echo "eSim and its dependencies have been removed."
}

# Check for installation flag and proceed accordingly
if [ "$1" == "--install" ]; then
    echo "Starting eSim installation..."
    createConfigFile
    installDependency
    installKicad
    installNghdl
    installSky130Pdk
    copyKicadLibrary
    echo "eSim installation completed successfully!"
elif [ "$1" == "--uninstall" ]; then
    uninstall
else
    echo "Usage: $0 --install | --uninstall"
    exit 1
fi
