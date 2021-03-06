# Garage-Door-Opener
## Raspberry Pi with a relay HAT to activate a garage door opener (used an existing 'switch' connection on an existing electric garage door opener)

Features:
  - Raspberry Pi web page to control the door - only accessible on home network
  - Web page shows temperature in garage - now, max & min from midnight
  - Enable / Disable to prevent accidental door activation
  - External switch provides local control inside the garage
  - Only IPs on an approved list can activate the garage door

![Screenshot_20210802-141056_Chrome](https://user-images.githubusercontent.com/30411837/128991054-8d093c03-5bdf-41e5-a993-6b47c27b34a4.jpg)

![20210425_141103](https://user-images.githubusercontent.com/30411837/128991141-6e284f93-cb96-489d-8816-3d32057109bf.jpg)

![20210425_141209](https://user-images.githubusercontent.com/30411837/128991502-967a53f4-af42-40d6-b2a7-9b0f530aefb2.jpg)

### Components:
  - Raspberry Pi Zero
  - sb components Zero Relay 2 Channel 5V Relay Shield for Raspberry Pi
  - Adafruit MCP9808 High Accuracy I2C Temperature Sensor Breakout Board

### Notes:
  - Install Adafruit library on the Raspberry Pi
  - Install Apache web server & PHP on the Raspberry Pi
  - Copy garagedoor.php file as index.php into /var/www/html
  - Edit req_ip_log.txt to contain valid IP addresses of devices to control the door (make device IPs fixed at router) - copy file to /var/www/html 
