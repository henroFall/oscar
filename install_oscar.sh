#!/bin/bash

rootCheck() {
    if ! [ $(id -u) = 0 ]; 
    then
        echo -e "\e[41m I am not root! Run with SUDO. \e[0m"
        exit 1
    fi
}

check_exit_status() {
    if [ $? -ne 0 ]
    then
        echo -e "\e[41m ERROR: PROCESS FAILED!"
        echo
        read -p "The last command exited with an error. Exit script? (yes/no)" answer
        if [ "$answer" == "yes" ]
        then
		    echo -e "EXITING. \e[0m"
			echo
            exit 1
        fi
    fi
echo
}

rootCheck

echo "               ____ "
echo "   ___________//__\\\\__________"
echo "  /___________________________\\"
echo "  I___I___I___I___I___I___I___I"
echo "        < ,wWWWWwwWWWWw, >"
echo "       <  WW( 0 )( 0 )WW  >"
echo "      <      \'-\'  \'-\'      >"
echo "     <    ,._.--\"\"--._.,    >"
echo "     <   \' \\   .--.   / \`   >"
echo "      <     \'./__\\_\\.'     >"
echo "    ___<.-.____________.-.>___"
echo "   (___/   \\__________/   \\___)"
echo "    |  \\,_,/          \\,_,/  |"
echo "  .-|/^\\ /^\\ /^\\ /^\\ /^\\ /^\\ |-."
echo " / (|/\\| | | | | | | | | | /\\|) \\"
echo " '.___/| | | | | | | | | | \\___.'"
echo "    || | | | | | | | | | | | |"
echo "    || | | | | | | | | | | | |"
echo "    || | | | | | | | | | | | |"
echo "    || | | | | | | | | | | | |"
echo "    || | | | | | | | | | | | |"
echo "    || | | | | | | | | | | | |"
echo "    || | | | | | | | | | | | |"
echo "    || | | | | | | | | | | | |"
echo "    || | | | | | | | | | | | |"
echo "    |\\_/ \\_/ \\_/ \\_/ \\_/ \\_/ |"
echo "    |                        |"
echo
echo "Hello! Let's set up Oscar!"
echo
echo "This script is tested on Raspbian and Ubuntu 20.04."
echo

######################################## Dependencies
echo
echo "We need to install some dependencies. This can take upwards of an"
echo "hour, since it involves compiling stuff. Ready? Press <enter> when"
echo "you're ready. Press 'Ctrl+C' to cancel."
read 
echo
echo "Stripping nodejs & npm from system and reinstalling with other dependencies..."
apt update
apt remove npm
apt remove nodejs-legacy
apt remove nodejs
rm /usr/bin/node
apt install sed python-setuptools python-pip git supervisor build-essential nodejs npm -y
check_exit_status
ln -s which node /usr/local/bin/node
check_exit_status
pip install PyYAML trello==0.9.1 twilio
check_exit_status
######################################## Oscar itself
cd /var
git clone https://github.com/henroFall/oscar.git
check_exit_status
cd /var/oscar/web

echo
echo "Oscar needs a TCP port for a web server. I can use port 80, but"
echo "that is some pretty prime real estate. You can enter any valid"
echo "TCP port number here, or press <enter> to use 79."
read -p "Port number [79]:" webport
if [ -z "$webport" ]
then webport=79
fi
sed -i "s/80/$webport/g" /var/oscar/web/app.js
check_exit_status

npm install
check_exit_status

python build1.py

echo
echo "We are now going to attept to detect your USB barcode scanner."
echo "Be sure it is UNPLUGED, then press <enter>."
read
echo "Standby..."
sleep 2
ls -1 /dev/input > ~/before.txt
sleep 1
echo
echo "Now, please PLUG IT IN, then press <enter>."
read
echo "Standby..."
sleep 2
ls -1 /dev/input > ~/after.txt
usbPort=$(comm -13  ~/before.txt ~/after.txt)
if [ -z "$usbPort" ]
then
      echo
      echo "I didn't see anything change, so we will assume this is Raspbian or"
          echo "another OS that defaults to event0 for the device input." 
          echo "Using event0..."
          usbPort="event0"
else
      echo "I see a new device attached to $usbPort, so we are going to use that."
fi
echo

place="/dev/input/"
usbPlace="${place}${usbPort}"
echo 
echo "Set device to: $usbPlace"

python build2.py $usbPlace

sed -i "s/79/$webport/g" /etc/oscar.yaml

supervisorctl reload
check_exit_status