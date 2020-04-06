import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from streamlit import caching
import time

# This is the main script for running the ICS shipbuilding prototype simulator. Threshold parameters are taken from 
# the CDD. Deviations from the threshold parameters are determined by the configuration selected by the user.
# Each selectable configuration item determines the shape of the normal distribution from which the parameter is
# drawn.

# The file will run a web application hosted on Heroku.
# Author: Matt Williams, matthew.j.williams@protonmail.com, 518-221-3267
def main():
	# Asks for password, and calls get_selections() is the password is valid
	passwords = ['administrat0r', 'riverrun', 'jupiter', 'andromeda', 'tesla', 'fermi']
	st.title('Ship Prototype Testing Simulator')
	st.header('Configuration options will appear once your password has been entered')
	text_input = st.text_input('Password: ', value='')
	password = text_input.lower()  # convert user input to lowercase
	if password in passwords:
		st.write('You entered ', password)
		get_selections(password)
	elif password == '':
		st.write('')
	else:
		st.write('Password is not recognized. Please reenter.')

def get_selections(password):
	selections_complete = False
	engine = ' '
	hullform = ' '
	fuel_storage = ' '
	er_design = ' '
	engine = st.selectbox(
		'Select a propulsion engine size',
		(' ', 'Small', 'Medium', 'Large'))
	st.write('You selected ', engine.lower())
	if engine != ' ':
		hullform = st.selectbox(
			'Select a hullform block coefficient',
			(' ', 'Fine', 'Moderate', 'Full'))
		st.write('You selected ', hullform.lower())
	if hullform != ' ':
		fuel_storage = st.selectbox(
			'Select a fuel storage capacity',
			(' ', 'Minimum', 'Moderate', 'Maximum'))
		st.write('You selected ', fuel_storage.lower())
	if fuel_storage != ' ':
		er_design = st.selectbox(
			'Select a component replacement design for the engine room',
			(' ', 'RIP', 'Semi-mod', 'Modular'))
		st.write('You selected ', er_design.lower())
	if engine != ' ' and hullform != ' ' and fuel_storage != ' ' and er_design != ' ':
		selections_complete = True
		engine = engine.lower()
		hullform = hullform.lower()
		fuel_storage = fuel_storage.lower()
		er_design = er_design.lower()

	if selections_complete:
		start = st.button('Begin Testing')

		if start:
			perform_calcs(password, engine, hullform, fuel_storage, er_design)

def perform_calcs(password, engine, hullform, fuel_storage, er_design):
	# Threshold parameters
	speed = 22       # knots
	mtbf = 300       # hours
	cargo = 28000    # cuft
	vehicle = 20800  # sqft
	fuel = 310000    # gallons
	range_ = 10000   # nautical miles
	fuel_burn = 75   # gal/nm
	Ao = 0.8
	test_dict = dict([('riverrun', 1), ('jupiter', 5), ('andromeda', 10), ('tesla', 15)])
	if password == 'administrat0r':
		n_tests = 5
	else:
		n_tests = test_dict[password]

	speeds = []
	mtbfs = []
	cargoes = []
	vehicles = []
	fuels = []
	ranges = []
	Aos = []
	test_nums = np.arange(1, n_tests+1)

	engine_options = ['small', 'medium', 'large']
	hull_options = ['fine', 'moderate', 'full']
	fuel_options = ['minimum', 'moderate', 'maximum']
	er_options = ['rip', 'semi-mod', 'modular']
	form_factor = [1.05, 1.0, .95]

	for i in range(n_tests):
	  categories = ['speed', 'mtbf', 'cargo', 'vehicle', 'fuel', 'burn', 'ao']
	  param_dict = {}
	  for cat in categories:
	  	p1_mean = 0.95
	  	p2_mean = 1.
	  	p3_mean = 1.05
	  	p1_std = np.random.uniform(.05, .1)
	  	p2_std = np.random.uniform(.075, .15)
	  	p3_std = np.random.uniform(.1, .2)
	  	p1_std *= p1_mean
	  	p2_std *= p2_mean
	  	p3_std *= p3_mean
	  	p1 = np.random.normal(.95, p1_std)
	  	p2 = np.random.normal(1.0, p2_std)
	  	p3 = np.random.normal(1.05, p3_std)
	  	param_dict[f'{cat}_param_multipliers'] = [p1, p2, p3]
		  # print(f'Param mults: {param_multipliers}')

	  speed_mult = param_dict['speed_param_multipliers'][engine_options.index(engine)]
	  mtbf_mult = param_dict['mtbf_param_multipliers'][er_options.index(er_design)]
	  cargo_mult = param_dict['cargo_param_multipliers'][hull_options.index(hullform)]
	  vehicle_mult = param_dict['vehicle_param_multipliers'][hull_options.index(hullform)]
	  fuel_mult = param_dict['fuel_param_multipliers'][fuel_options.index(fuel_storage)]
	  burn_mult = param_dict['burn_param_multipliers'][::-1][engine_options.index(engine)]
	  ao_mult = param_dict['ao_param_multipliers'][er_options.index(er_design)]
	  form_mult = form_factor[hull_options.index(hullform)]
	  all_mults = [speed_mult, mtbf_mult, cargo_mult, vehicle_mult, fuel_mult, burn_mult, ao_mult]
	  cost_mult = np.mean(all_mults)

	  speed_final = speed * speed_mult * form_mult
	  mtbf_final = mtbf * mtbf_mult
	  cargo_final = cargo * cargo_mult
	  vehicle_final = vehicle * vehicle_mult
	  fuel_final = fuel * fuel_mult
	  burn_final = fuel_burn * burn_mult
	  range_final = fuel_final / burn_final
	  ao_final = Ao * ao_mult  

	  speeds.append(speed_final)
	  mtbfs.append(mtbf_final)
	  cargoes.append(cargo_final)
	  vehicles.append(vehicle_final)
	  fuels.append(fuel_final)
	  ranges.append(range_final)
	  Aos.append(ao_final)

	for i, ao in enumerate(Aos):
	  if ao > 1.0:
	    Aos[i] = 1.0

	prog = progress_bar(password, n_tests)
	if prog == 'complete':
		show_results(n_tests, speeds, mtbfs, cargoes, vehicles, fuels, ranges, Aos, cost_mult)

def show_results(n_tests, speeds, mtbfs, cargoes, vehicles, fuels, ranges, Aos, cost_mult):
	if n_tests == 1:
		st.markdown('Testing Results: ')
		st.markdown(f'Speed: {speed_final:.2f} kts  \nMTBF: {mtbf_final:.1f} hours  \nCargo space: {cargo_final:.2f} sqft  \n\
		Vehicle storage: {vehicle_final:.2f} cuft  \nFuel capacity: {fuel_final:.2f} gallons  \nRange: {range_final:.2f}  \nAo: {ao_final:0.1f} \n\
		Cost factor: {cost_mult:.2f}')
	else:
		st.markdown('Testing Results: ')
		st.markdown(f'Speed: {np.mean(speeds):.2f} kts  \nMTBF: {np.mean(mtbfs):.1f} hours  \nCargo space: {np.mean(cargoes):.2f} sqft  \n\
		Vehicle storage: {np.mean(vehicles):.2f} cuft  \nFuel capacity: {np.mean(fuels):.2f} gallons  \nRange: {np.mean(ranges):.2f}  \n\
		Ao: {np.mean(Aos):0.1f}  \nCost factor: {cost_mult:.2f}')
		#fig, ax = plt.subplots(3, 2)
		plt.plot(range(1, n_tests+1), speeds, 'g-.', marker='*', markersize=14, label='Test speed')
		plt.hlines(np.mean(speeds), 1, n_tests, colors='red', linestyle='dashed', label='Average')
		plt.xlabel('Test number')
		plt.ylabel('Full-scale speed (knots)')
		plt.xticks(range(1, n_tests+1))
		plt.legend()
		st.pyplot()

		plt.plot(range(1, n_tests+1), mtbfs, 'g-.', marker='*', markersize=14, label='MTBF')
		plt.hlines(np.mean(mtbfs), 1, n_tests, colors='red', linestyle='dashed', label='Average')
		plt.xlabel('Test number')
		plt.ylabel('Mean time betweet failures (hours)')
		plt.xticks(range(1, n_tests+1))
		plt.legend()
		st.pyplot()

		plt.plot(range(1, n_tests+1), cargoes, 'g-.', marker='*', markersize=14, label='Prototype cargo space')
		plt.hlines(np.mean(cargoes), 1, n_tests, colors='red', linestyle='dashed', label='Average')
		plt.xlabel('Prototype number')
		plt.ylabel('Full-scale cargo storage space (cuft)')
		plt.xticks(range(1, n_tests+1))
		plt.legend()
		st.pyplot()

		plt.plot(range(1, n_tests+1), vehicles, 'g-.', marker='*', markersize=14, label='Prototype vehicle storage space')
		plt.hlines(np.mean(vehicles), 1, n_tests, colors='red', linestyle='dashed', label='Average')
		plt.xlabel('Prototype number')
		plt.ylabel('Full-scale vehicle storage space (sqft)')
		plt.xticks(range(1, n_tests+1))
		plt.legend()
		st.pyplot()

		plt.plot(range(1, n_tests+1), fuels, 'g-.', marker='*', markersize=14, label='Fuel storage')
		plt.hlines(np.mean(fuels), 1, n_tests, colors='red', linestyle='dashed', label='Average')
		plt.xlabel('Prototype number')
		plt.ylabel('Full-scale fuel storage capacity (gallons)')
		plt.xticks(range(1, n_tests+1))
		plt.legend()
		st.pyplot()

		plt.plot(range(1, n_tests+1), ranges, 'g-.', marker='*', markersize=14, label='Test range')
		plt.hlines(np.mean(ranges), 1, n_tests, colors='red', linestyle='dashed', label='Average')
		plt.xlabel('Test number')
		plt.ylabel('Full-scale range (nm)')
		plt.xticks(range(1, n_tests+1))
		plt.legend()
		st.pyplot()

		plt.plot(range(1, n_tests+1), Aos, 'g-.', marker='*', markersize=14, label='$A_o$')
		plt.hlines(np.mean(Aos), 1, n_tests, colors='red', linestyle='dashed', label='Average')
		plt.xlabel('Test number')
		plt.ylabel('$A_o$')
		plt.xticks(range(1, n_tests+1))
		plt.legend()
		st.pyplot()

def progress_bar(password, n_tests):
	if password == 'administrat0r':
		test_len = 1
	else:
		test_len = 120
	latest_iteration = st.empty()
	my_bar = st.progress(0)
	test_time = n_tests * test_len - (n_tests // 5) * test_len
	for i in range(int(test_time) + 1):
		percent_cpl = int(i / test_time * 100)
		latest_iteration.text(f'Test {int(i//test_len)+1}/{n_tests}')
		my_bar.progress(percent_cpl)
		time.sleep(1)
	return 'complete'


if __name__ == '__main__':
	main()