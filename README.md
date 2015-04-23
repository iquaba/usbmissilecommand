# usbmissilecommand
USB Missile Command Launcher Python script

Mashed up by Chris Evans (aka cbevans)

Mashed up from USB Missile Launcher Python Interface written by Pedram Amini <pamini@tippingpoint.com>
          and  Armageddon USB Missile Launcher by Piotr Maliński (aka riklaunim), http://www.rk.edu.pl

Takes the best of riklaunim's armageddon class and merges it with the USB missile laucnher
interface by Pedram Amini.  I wanted to use the web server, command line interface and 
socket features from Pedram's code, remove the dependency on the Windows usbhid.dll, and 
replace it with the functionality in riklaunim's Armageddon python class.

The result is a web interface, command line, and socket interface to control the Dream Cheeky
908 Thunder missile launcher from Ubuntu.  Requires pythin (uh - yeah...) and pyusb 1.0.

