from flask import Flask, render_template, redirect, url_for
from datetime import datetime
import random
import time
import os
import glob
import pandas as pd

import backend

#import measure_now

app = Flask(__name__)

@app.route('/')
def index(timeframe=12):
	
	# now = datetime.now()

	# curr_time = now.strftime("%d %B %Y | %H:%M %p")

	gpu_temp = os.popen("vcgencmd measure_temp").readline()
	gpu_temp = gpu_temp.replace("temp=","").replace("'C", "")

	cpu_temp = os.popen("cat /sys/class/thermal/thermal_zone0/temp").readline()
	cpu_temp = round(int(cpu_temp)/1000, 1)

	df = pd.read_csv('data/BME_sensor_data.csv')

	last_meas = int(round((time.time() - datetime.timestamp(datetime.strptime(df.iloc[-1]['Timestamp'], '%Y-%m-%d %H:%M:%S')))/60))
	curr_temp = df.iloc[-1]['Temperature']
	r_h = df.iloc[-1]['Humidity']
	iaq = int(round(df.iloc[-1]['IAQ']))
	eco2 = int(round(df.iloc[-1]['eCO2']))
	bvoc = round(df.iloc[-1]['bVOC'],2)
	press = int(round(df.iloc[-1]['Pressure']))
	gas = int(round(df.iloc[-1]['Gas']))

	plots_path = 'static/images/plots_' + str(timeframe) + 'h'

	humidity_path = os.path.join(plots_path, [element for element in os.listdir(plots_path) if "humidity" in element][0])
	temperature_path = os.path.join(plots_path, [element for element in os.listdir(plots_path) if "temperature" in element][0])
	IAQ_path = os.path.join(plots_path, [element for element in os.listdir(plots_path) if "iaq" in element][0])
	eCO2_path = os.path.join(plots_path, [element for element in os.listdir(plots_path) if "eco2" in element][0])
	bVOC_path = os.path.join(plots_path, [element for element in os.listdir(plots_path) if "bvoc" in element][0])
	pressure_path = os.path.join(plots_path, [element for element in os.listdir(plots_path) if "pressure" in element][0])
	gas_path = os.path.join(plots_path, [element for element in os.listdir(plots_path) if "gas" in element][0])

	return render_template('index.html', last_meas = last_meas, curr_temp = curr_temp, r_h = r_h, iaq = iaq, eco2 = eco2, 
										bvoc = bvoc, press = press, gas = gas, gpu_temp = gpu_temp, cpu_temp = cpu_temp,
										humidity_path = humidity_path, temperature_path = temperature_path, IAQ_path = IAQ_path,
										eCO2_path = eCO2_path, bVOC_path = bVOC_path, pressure_path = pressure_path, gas_path = gas_path)
	
@app.route('/measure_now')
def measure_now():
	print("Measure request received")
	backend.generate_figures_BME()
	return index()

@app.route('/<hours>')
def change_timeframe(hours):
	print("Timeframe change request received")

	gpu_temp = os.popen("vcgencmd measure_temp").readline()
	gpu_temp = gpu_temp.replace("temp=","").replace("'C", "")

	cpu_temp = os.popen("cat /sys/class/thermal/thermal_zone0/temp").readline()
	cpu_temp = round(int(cpu_temp)/1000, 1)

	df = pd.read_csv('data/BME_sensor_data.csv')

	last_meas = int(round((time.time() - datetime.timestamp(datetime.strptime(df.iloc[-1]['Timestamp'], '%Y-%m-%d %H:%M:%S')))/60))
	curr_temp = df.iloc[-1]['Temperature']
	r_h = df.iloc[-1]['Humidity']
	iaq = int(round(df.iloc[-1]['IAQ']))
	eco2 = int(round(df.iloc[-1]['eCO2']))
	bvoc = round(df.iloc[-1]['bVOC'],2)
	press = int(round(df.iloc[-1]['Pressure']))
	gas = int(round(df.iloc[-1]['Gas']))

	plots_path = 'static/images/plots_' + str(hours) + 'h'

	humidity_path = os.path.join(plots_path, [element for element in os.listdir(plots_path) if "humidity" in element][0])
	temperature_path = os.path.join(plots_path, [element for element in os.listdir(plots_path) if "temperature" in element][0])
	IAQ_path = os.path.join(plots_path, [element for element in os.listdir(plots_path) if "iaq" in element][0])
	eCO2_path = os.path.join(plots_path, [element for element in os.listdir(plots_path) if "eco2" in element][0])
	bVOC_path = os.path.join(plots_path, [element for element in os.listdir(plots_path) if "bvoc" in element][0])
	pressure_path = os.path.join(plots_path, [element for element in os.listdir(plots_path) if "pressure" in element][0])
	gas_path = os.path.join(plots_path, [element for element in os.listdir(plots_path) if "gas" in element][0])

	return render_template('index.html', last_meas = last_meas, curr_temp = curr_temp, r_h = r_h, iaq = iaq, eco2 = eco2, 
										bvoc = bvoc, press = press, gas = gas, gpu_temp = gpu_temp, cpu_temp = cpu_temp,
										humidity_path = humidity_path, temperature_path = temperature_path, IAQ_path = IAQ_path,
										eCO2_path = eCO2_path, bVOC_path = bVOC_path, pressure_path = pressure_path, gas_path = gas_path)



if __name__ == '__main__':
	app.run(debug=True, port=59424, host='0.0.0.0')

