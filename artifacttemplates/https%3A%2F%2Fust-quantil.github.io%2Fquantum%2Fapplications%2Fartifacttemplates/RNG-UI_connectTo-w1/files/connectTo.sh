#!/bin/bash
# Parameters:
# $Port
# $VMIP
# $SOURCE_AppName

sed -i "s/VMIP/$VMIP/g" /var/www/html/$SOURCE_AppName/index.html
sed -i "s/PORT/$Port/g" /var/www/html/$SOURCE_AppName/index.html

echo "Replaced VMIP with $VMIP and Port $Port"
