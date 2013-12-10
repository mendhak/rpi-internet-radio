pushd pi32-driver

STATE=${1:-"0"} #Default to 1

if [ $STATE == "0" ]; then
    sudo rmmod ssd1289
    sudo insmod ssd1289.ko.nobl
else
    sudo rmmod ssd1289
    sudo insmod ssd1289.ko.orig
fi

popd
