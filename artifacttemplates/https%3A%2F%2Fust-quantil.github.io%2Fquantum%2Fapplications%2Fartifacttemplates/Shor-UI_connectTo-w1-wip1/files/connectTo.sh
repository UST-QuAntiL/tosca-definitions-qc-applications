#!/bin/bash
# Parameters:
# $Port
# $VMIP
# $ContainerIP
# $SOURCE_AppName

if [[ ! -z $VMIP ]]; then
    sed -i "s/VMIP/$VMIP/g" /var/www/html/$SOURCE_AppName/index.html
elif [[ ! -z ContainerIP ]]; then
    sed -i "s/VMIP/$ContainerIP/g" /var/www/html/$SOURCE_AppName/index.html
else
    echo "ERROR: Neither VMIP nor ContainerIP is given!"
fi

sed -i "s/PORT/$Port/g" /var/www/html/$SOURCE_AppName/index.html