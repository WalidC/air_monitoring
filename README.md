# Air Monitoring
Air monitoring of environment (Temperature, humidity, eCO2, bVOC, etc.) using the [BOSCH BME680 sensor](https://www.sparkfun.com/products/16466) powered by a Raspberry Pi backend using Python and Flask.

# Prerequisites
- Flask (Web server) (https://pypi.org/project/Flask/)
- PM2 for processes in background (continously running server and backend scripts) (https://pm2.keymetrics.io/)
- Matplotlib for plots (https://matplotlib.org/)
- BOSCH BSEC software that gives an approximation for CO2 concentration and Indoor Air Quality (https://www.bosch-sensortec.com/software-tools/software/bsec/)

# How to run

First, we need to compile the BSEC binary and place it in the same folder. Refer to https://github.com/alexh-name/bsec_bme680_linux for instructions on compiling BSEC binary. For best results, use the `make.config` and `bsec_bme680.c` files from this repo for binary compiling (removal of temperature offset and correct CPU architecture for RPi 4B. 

Once all libraries are installed and sensor is connected via I2C to the RPi, we will load up the scripts in the background starting with the data capture shell script `binary_bsec.sh` which appends the stdout in the `data/BME_sensor_data.txt` file. This script will query the BME680 sensor every 5 minutes (sampling rate is specified in the `make.config` file earlier) for sampling then runs the sensor output through the BSEC BOSH software that outputs IAQ, eCO2 and bVOC (which are approximations for the Indoor Air Quality indice, approximated CO2 concentration and approximate breath VOC gases concentration).

```
sudo pm2 start binary_bsec.sh
```

Then, we need to run the backend script that handles the data conversion into plots while adding the accuracy (+- a range for every measurement) for the past 2, 4, 8, 12 and 24 hours.

```
sudo pm2 start backend_shell.sh
```

Finally, we are now ready to start the web server that will handles the HTTP requests and provide the plots for the timeframe requested.

```
sudo pm2 start website_shell.sh
```

The web server should now be up and running, data is being sampled every 5 minutes and plots generated every 10 minutes (delays are arbitrary and can be changed within the `time.sleep()` functions). The RPi should be serving the website on `localhost:80` on itself and locally on its local ip (e.g: `192.168.0.150:80`)

# Troubleshooting

If you are unable to run `pm2` in sudo, simply get the exact location of pm2 and run it as sudo by using
```
type pm2
```
this will output the location of pm2 as shown here `pm2 is /home/pi/.config/nvm/versions/node/v17.2.0/bin/pm2`, then the new command shall be
```
sudo /home/pi/.config/nvm/versions/node/v17.2.0/bin/pm2 start xxxx.sh
```
