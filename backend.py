import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


import numpy as np
import pandas as pd

import os

from datetime import datetime
import time

import warnings
warnings.filterwarnings("ignore")

def generate_figures_BME():

	sensor_data_path_txt = 'data/BME_sensor_data.txt'

	curr_time = str(round(time.time()))

	print("Reading sensor data saved...")
	bsec_log = open(sensor_data_path_txt, "r")
	log = bsec_log.readlines()

	time_array = []
	IAQ_array = []
	T_array = []
	H_array = []
	P_array = []
	G_array = []
	eCO2_array = []
	bVOC_array = []

	for sample in range(len(log)):
		time_array.append(log[sample].split(',')[0])
		IAQ_array.append(float(log[sample].split(',')[1].split(':')[-1]))
		T_array.append(float(log[sample].split(',')[2].split(':')[-1]))
		H_array.append(float(log[sample].split(',')[3].split(':')[-1]))
		P_array.append(float(log[sample].split(',')[4].split(':')[-1]))
		G_array.append(float(log[sample].split(',')[5].split(':')[-1]))
		eCO2_array.append(round(float(log[sample].split(',')[7].split(':')[-1]), 3))
		bVOC_array.append(round(float(log[sample].split(',')[8].split(':')[-1][:-1]), 5))


	df_log = pd.DataFrame({'Timestamp':time_array, 'IAQ':IAQ_array, 'Temperature':T_array, 'Humidity':H_array, 'Pressure':P_array, 'Gas':G_array, 'eCO2':eCO2_array, 'bVOC':bVOC_array})
		
	df_log.to_csv('data/BME_sensor_data.csv')

	for timeframe in [2, 4, 8, 12, 24]:

		print("Plotting for timeframe " + str(timeframe) + "h")

		humidity_path = '/home/pi/air_monitoring/static/images/plots_' + str(timeframe) + 'h/humidity_' + curr_time +'.png'
		temperature_path = '/home/pi/air_monitoring/static/images/plots_' + str(timeframe) + 'h/temperature_' + curr_time +'.png'
		IAQ_path = '/home/pi/air_monitoring/static/images/plots_' + str(timeframe) + 'h/iaq_' + curr_time +'.png'
		eCO2_path = '/home/pi/air_monitoring/static/images/plots_' + str(timeframe) + 'h/eco2_' + curr_time +'.png'
		bVOC_path = '/home/pi/air_monitoring/static/images/plots_' + str(timeframe) + 'h/bvoc_' + curr_time +'.png'
		pressure_path = '/home/pi/air_monitoring/static/images/plots_' + str(timeframe) + 'h/pressure_' + curr_time +'.png'
		gas_path = '/home/pi/air_monitoring/static/images/plots_' + str(timeframe) + 'h/gas_' + curr_time +'.png'

		print("Clearing previous plots ... ")

		plots_path = 'static/images/plots_' + str(timeframe) + 'h'
		for plot in os.listdir(plots_path):
			os.remove(os.path.join(plots_path,plot))


		df_timeframe = df_log.tail(int(int(timeframe)*60/5))

		time_str_array = [datetime.strptime(stamp, '%Y-%m-%d %H:%M:%S').strftime("%H:%M") for stamp in df_timeframe['Timestamp'].tolist()]
		print("Converting to CSV and plotting...")
		# ***** Humidity *****
		plt.figure(figsize=[20,10])

		plt.xlabel('Time', fontsize=18)
		plt.ylabel('Rel. Humidity (%)', fontsize=18)

		# plt.plot(time_str_array, H_array, "-o", linewidth=4, markersize=15, c="#fb7d07")
		plt.plot(time_str_array, df_timeframe['Humidity'].values, linewidth=4, c="#fb7d07")
		plt.fill_between(time_str_array, df_timeframe['Humidity'].values-3, df_timeframe['Humidity'].values+3, color="#fb7d07", alpha=0.5)
		plt.grid()

		plt.xticks(fontsize=18)
		plt.yticks(fontsize=18)

		axes = plt.axes()
		x_values = axes.get_xticks()
		x_len = len(x_values)
		new_x = [x_values[i] for i in [0, x_len // 6, 2 * x_len // 6, 3 * x_len // 6, 4 * x_len // 6, 5 * x_len // 6, -1]]
		axes.set_xticks(new_x)

		plt.gca().spines['bottom'].set_color('white')
		plt.gca().spines['left'].set_color('white')
		plt.gca().xaxis.label.set_color('white')
		plt.gca().yaxis.label.set_color('white')
		plt.gca().tick_params(axis='x', colors='white')
		plt.gca().tick_params(axis='y', colors='white')

		plt.savefig(humidity_path, dpi=200, bbox_inches='tight', transparent="True", pad_inches=0)

		plt.close()

		# ***** Temperature *****
		plt.figure(figsize=[20,10])

		plt.xlabel('Time', fontsize=18)
		plt.ylabel('Temperature (deg C)', fontsize=18)

		plt.plot(time_str_array, df_timeframe['Temperature'].values, linewidth=4, color="#0e87cc")
		plt.fill_between(time_str_array, df_timeframe['Temperature'].values-1, df_timeframe['Temperature'].values+1, color="#0e87cc", alpha=0.5)
		plt.grid()

		plt.xticks(fontsize=18)
		plt.yticks(fontsize=18)

		axes = plt.axes()
		x_values = axes.get_xticks()
		x_len = len(x_values)
		new_x = [x_values[i] for i in [0, x_len // 6, 2 * x_len // 6, 3 * x_len // 6, 4 * x_len // 6, 5 * x_len // 6, -1]]
		axes.set_xticks(new_x)

		plt.gca().spines['bottom'].set_color('white')
		plt.gca().spines['left'].set_color('white')
		plt.gca().xaxis.label.set_color('white')
		plt.gca().yaxis.label.set_color('white')
		plt.gca().tick_params(axis='x', colors='white')
		plt.gca().tick_params(axis='y', colors='white')

		plt.savefig(temperature_path, dpi=200, bbox_inches='tight', transparent="True", pad_inches=0)

		plt.close()

		# ***** IAQ *****
		plt.figure(figsize=[20,10])

		plt.xlabel('Time', fontsize=18)
		plt.ylabel('IAQ Score', fontsize=18)

		plt.plot(time_str_array, df_timeframe['IAQ'].values, linewidth=4, color="#8c0034")
		plt.fill_between(time_str_array, df_timeframe['IAQ'].values*0.85, df_timeframe['IAQ'].values*1.15, color="#8c0034", alpha=0.5)
		plt.grid()

		plt.xticks(fontsize=18)
		plt.yticks(fontsize=18)

		axes = plt.axes()
		x_values = axes.get_xticks()
		x_len = len(x_values)
		new_x = [x_values[i] for i in [0, x_len // 6, 2 * x_len // 6, 3 * x_len // 6, 4 * x_len // 6, 5 * x_len // 6, -1]]
		axes.set_xticks(new_x)

		plt.gca().spines['bottom'].set_color('white')
		plt.gca().spines['left'].set_color('white')
		plt.gca().xaxis.label.set_color('white')
		plt.gca().yaxis.label.set_color('white')
		plt.gca().tick_params(axis='x', colors='white')
		plt.gca().tick_params(axis='y', colors='white')

		plt.savefig(IAQ_path, dpi=200, bbox_inches='tight', transparent="True", pad_inches=0)

		plt.close()

		# ***** eCO2 *****
		plt.figure(figsize=[20,10])

		plt.xlabel('Time', fontsize=18)
		plt.ylabel('eCO2 (ppm)', fontsize=18)

		plt.plot(time_str_array, df_timeframe['eCO2'].values, linewidth=4, color="#3a2efe")
		plt.fill_between(time_str_array, df_timeframe['eCO2'].values*0.85, df_timeframe['eCO2'].values*1.15, color="#3a2efe", alpha=0.5)
		plt.grid()

		plt.xticks(fontsize=18)
		plt.yticks(fontsize=18)

		axes = plt.axes()
		x_values = axes.get_xticks()
		x_len = len(x_values)
		new_x = [x_values[i] for i in [0, x_len // 6, 2 * x_len // 6, 3 * x_len // 6, 4 * x_len // 6, 5 * x_len // 6, -1]]
		axes.set_xticks(new_x)

		plt.gca().spines['bottom'].set_color('white')
		plt.gca().spines['left'].set_color('white')
		plt.gca().xaxis.label.set_color('white')
		plt.gca().yaxis.label.set_color('white')
		plt.gca().tick_params(axis='x', colors='white')
		plt.gca().tick_params(axis='y', colors='white')

		plt.savefig(eCO2_path, dpi=200, bbox_inches='tight', transparent="True", pad_inches=0)

		plt.close()

		# ***** bVOC *****
		plt.figure(figsize=[20,10])

		plt.xlabel('Time', fontsize=18)
		plt.ylabel('bVOC (ppm)', fontsize=18)

		plt.plot(time_str_array, df_timeframe['bVOC'].values, linewidth=4, color="#6ecb3c")
		plt.fill_between(time_str_array, df_timeframe['bVOC'].values*0.85, df_timeframe['bVOC'].values*1.15, color="#6ecb3c", alpha=0.5)
		plt.grid()

		plt.xticks(fontsize=18)
		plt.yticks(fontsize=18)

		axes = plt.axes()
		x_values = axes.get_xticks()
		x_len = len(x_values)
		new_x = [x_values[i] for i in [0, x_len // 6, 2 * x_len // 6, 3 * x_len // 6, 4 * x_len // 6, 5 * x_len // 6, -1]]
		axes.set_xticks(new_x)

		plt.gca().spines['bottom'].set_color('white')
		plt.gca().spines['left'].set_color('white')
		plt.gca().xaxis.label.set_color('white')
		plt.gca().yaxis.label.set_color('white')
		plt.gca().tick_params(axis='x', colors='white')
		plt.gca().tick_params(axis='y', colors='white')

		plt.savefig(bVOC_path, dpi=200, bbox_inches='tight', transparent="True", pad_inches=0)

		plt.close()

		# ***** Pressure *****
		plt.figure(figsize=[20,10])

		plt.xlabel('Time', fontsize=18)
		plt.ylabel('Pressure (hPa)', fontsize=18)
		
		plt.plot(time_str_array, df_timeframe['Pressure'].values, linewidth=4, color="#019529")
		plt.fill_between(time_str_array, df_timeframe['Pressure'].values-1, df_timeframe['Pressure'].values+1, color="#019529", alpha=0.5)
		plt.grid()

		plt.xticks(fontsize=18)
		plt.yticks(fontsize=18)

		axes = plt.axes()
		x_values = axes.get_xticks()
		x_len = len(x_values)
		new_x = [x_values[i] for i in [0, x_len // 6, 2 * x_len // 6, 3 * x_len // 6, 4 * x_len // 6, 5 * x_len // 6, -1]]
		axes.set_xticks(new_x)

		plt.gca().spines['bottom'].set_color('white')
		plt.gca().spines['left'].set_color('white')
		plt.gca().xaxis.label.set_color('white')
		plt.gca().yaxis.label.set_color('white')
		plt.gca().tick_params(axis='x', colors='white')
		plt.gca().tick_params(axis='y', colors='white')

		plt.savefig(pressure_path, dpi=200, bbox_inches='tight', transparent="True", pad_inches=0)

		plt.close()

		# ***** Gas *****
		plt.figure(figsize=[20,10])

		plt.xlabel('Time', fontsize=18)
		plt.ylabel('Gas (Ohms)', fontsize=18)

		plt.plot(time_str_array, df_timeframe['Gas'].values, linewidth=4, c="#8d5eb7")

		plt.grid()

		plt.xticks(fontsize=18)
		plt.yticks(fontsize=18)

		axes = plt.axes()
		x_values = axes.get_xticks()
		x_len = len(x_values)
		new_x = [x_values[i] for i in [0, x_len // 6, 2 * x_len // 6, 3 * x_len // 6, 4 * x_len // 6, 5 * x_len // 6, -1]]
		axes.set_xticks(new_x)

		plt.gca().spines['bottom'].set_color('white')
		plt.gca().spines['left'].set_color('white')
		plt.gca().xaxis.label.set_color('white')
		plt.gca().yaxis.label.set_color('white')
		plt.gca().tick_params(axis='x', colors='white')
		plt.gca().tick_params(axis='y', colors='white')

		plt.savefig(gas_path, dpi=200, bbox_inches='tight', transparent="True", pad_inches=0)

		plt.close()

	print("Plots completed and saved...")

if __name__ == '__main__':

	while True:
		print("Plotting figure...")
		generate_figures_BME()
		print("Sleeping now, next figure in 10 minutes\n")
		time.sleep(600)