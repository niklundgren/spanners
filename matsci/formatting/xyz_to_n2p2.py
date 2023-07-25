import os
import time
import numpy as np
import subprocess as sp

def read_configs(dat):
	n_configs = count_configs(dat)
	# Custom dtype to capture desirable traits,
	# here we capture config_type, energy
	# and num_atoms (as well as the output string "config")
	columns = ['config_type',
				'energy',
			   	'num_atoms',
				'config']
	fields = [('config_type', 'U15'),
			  ('energy', 'f8'),
			  ('num_atoms', 'u2'),
			  ('config', 'O')]
	frames = np.empty((n_configs), dtype=fields)

	# Observables in xyz file (need them all, in order, to parse)
	observables = {'energy': None,
				   'config_type': None,
				   'kpoints': None,
				   'Lattice': None,
					'Properties': None}
					# 'kpoints': None,
				    # 'kpoints_density': None,
				    # 'virial': None,
				    # 'cutoff': None,
				    # 'nneightol': None,
				    # 'pbc': None,}
	keys = [x for x in observables.keys()] # get list of keys

	line_count = 0 # Begin Parse Configs
	frame_count = 0
	start = time.time()
	while frame_count < n_configs:
		# Arrange data
		numlines = int(dat[0].strip()) + 2 # n_atoms + 2 lines for info
		cfg = dat[:numlines]
		n_atoms = int(cfg[0].strip())
		obs = cfg[1].strip('energy=')
		atoms = cfg[2:]




		# Parse observables
		for i in range(len(keys)-1):
			key = keys[i]
			next_key = keys[i+1]
			try:
				obs = obs.split(next_key+'=')
				val = obs[0].strip().strip('\"').strip()
				observables[key] = val
				obs = obs[1]
			except:
				print('Error frame ', frame_count)
				print(observables)
				print(key, next_key)
				print(obs)
				obs = obs[0]
				continue
		observables[keys[-1]] = obs.strip()


		# Format Lattice
		lat = observables['Lattice'].split()
		nlat =  'lattice \t'+lat[0]+'\t'+lat[1]+'\t'+lat[2]+'\n'
		nlat += 'lattice \t'+lat[3]+'\t'+lat[4]+'\t'+lat[5]+'\n'
		nlat += 'lattice \t'+lat[6]+'\t'+lat[7]+'\t'+lat[8]+'\n'
		observables['Lattice'] = nlat


		# Parse atomic info
		# gap xyz format = Species X Y Z AtomicNum Fx Fy Fz
		# n2p2 format = X Y Z Symbol 0 0 Fx Fy Fz (the two zeros are mandatory)
		n_descriptors = len(cfg[2].split())
		atoms = np.empty((n_atoms, n_descriptors+1), dtype='<U10')
		for i in range(n_atoms):
			atom = cfg[i+2].split()
			atoms[i, :-1] = atom[:]
		# Current format = Species X Y Z AtomicNum Fx Fy Fz Blank
		# 				  =  0      1 2 3 4         5  6  7  8
		# Swap to correct order
		atoms = atoms[:, [1, 2, 3, 0, 4, 8, 5, 6, 7]]
		atoms[:, 4] = 0; atoms[:, 5] = 0 # Blank out for n2p2 format


		# Format atomic info
		start_str = np.repeat(['atom '], atoms.shape[0])[:,None]
		nlines = np.repeat(['\n'], atoms.shape[0])[:,None]
		atom_strings = [('\t').join(line) for line in np.concatenate((start_str, atoms, nlines), axis=1)]
		system_string = ''
		for i in atom_strings:
			system_string += i


		# Format write string
		write = 'begin\n'
		write += 'comment config_type '+observables['config_type']+'\n'
		write += system_string
		write += 'energy\t'+observables['energy']+'\n'
		write += 'charge\t0.0\n'
		write += 'end'


		# write to array
		frames[frame_count] = observables['config_type'], observables['energy'], n_atoms, write

		# Iterate
		line_count += numlines
		frame_count += 1
		dat = dat[numlines:]
		if frame_count % 1000 == 0:
			stop = time.time()
			rate = frame_count/(stop-start)
			estimation = (n_configs-frame_count)/ rate / 60
			print('Current Rate: %.2f frames/sec' % rate)
			print('Estimated Time %i min' % estimation)
			prog = frame_count*100/n_configs
			print('Reading: %.1f %%' % prog)
		elif frame_count % 500 == 0:
			prog = frame_count*100/n_configs
			print('Reading: %.1f %%' % prog)
		elif frame_count == 100:
			stop = time.time()
			prog = frame_count*100 / n_configs
			print('Reading: %.1f %%' % prog)
			rate = frame_count/(stop-start)
			estimation = n_configs / rate / 60
			print('Current Rate: %.2f frames/sec' % rate)
			print('Estimated Time %i min' % estimation)
	return frames


def count_configs(dat):
	count = 0
	for line in dat:
		if line.startswith('energy'):
			count += 1
	return count


def print_out_indices(configs, frames, file):
	writers = configs['string']
	for i in frames:
		print(writers[i], file=file)
	print('Finished!')


def print_out_types(configs, types, file):
	for t in types:
		single_type_confs = configs[configs['config_type'] == t]
		writes = single_type_confs['config']
		for conf in writes:
			print(conf, file=file)
	print('Finished!')


def print_out_energy():
	# TODO: make new panda column which has an energy/atom column
	print('In Progress')


### Debugging
debug_conf = False

# Get user input + collect data
print('Input\n--------------')
if not debug_conf:
	in_name = input('XYZ file without extension: ')
else:
	in_name = 'gap_carbon'
f = open(in_name+'.xyz', 'r')
dat = f.readlines()
n_configs = count_configs(dat)
print(str(n_configs)+' frames detected')

print('Output\n--------------')
if not debug_conf:
	out_name = input('Insert new name, if desired (default <xyz_name>.n2p2): ')
	if out_name == "":
		out_name = in_name
	if os.path.exists(out_name+'.n2p2'):
		check = input('This file exists, overwrite? (y)')
		if check != 'y':
			print('exiting!')
			exit()
		else:
			print('Overwriting '+out_name+'.data')
	out_file = open(out_name+'.data', 'w+')
else:
	out_file = open('n2p2.data', 'w+')



if debug_conf:
	types = ['Amorphous_Bulk']
	print('\nTypes Selected: ', types)
	configs = read_configs(dat)
	print_out_types(configs, types, out_file)
else:
	print('Frame Selection\n--------------')
	print('Which frames would you liked converted?')
	print('Note: choose "l" and leave list blank to convert all frames')
	print('Options:\n"l" for list of ranges\n"t" for config_type\n"e" for energy')
	choice = input('Enter "l" for list of frames or "t" for type of config\n')
	if choice == 'l':
		frames_list = []
		print('Enter lists exactly\nstart1:stop1, start2:stop2, ...')
		frames = input('Range of frames:\n')
		ranges = frames.split(',')
		if frames != '':
			print('Detected ' + str(len(ranges)) + ' ranges of frames')
			for r in ranges:
				frames_list.append(list(range(r[0], r[1]+1)))
			print('Total num frames: '+str(len(frames_list)))
		try:
			configs = np.load(in_name + '_n2p2.npy', allow_pickle=True)
		except FileNotFoundError:
			configs = read_configs(dat)
			np.save(in_name + '_n2p2', configs)
		print_out_types(configs, type_list, out_file)
		print_out_indices(configs, frames_list, out_file)
	elif choice == 't':
		available = sp.check_output("grep -oP 'config_type=\K\w+' "+in_name
									+".xyz | sort --unique", shell=True)\
									.decode('UTF-8')\
									.strip()\
									.split('\n')

		count_list = []
		for type in available:
			count = sp.check_output('grep '+type+' '+in_name+'.xyz -c', shell=True).decode('UTF-8')
			count_list.append(count)
			print('%s : %i' % (type, int(count)))
		print('Select type or list of types of config')

		type_dict = {}
		for i in range(len(available)):
			type = available[i]
			count = count_list[i]
			type_dict[type] = count.strip('\n')

		type_list = []
		type = None
		num_types = 0
		num_frames = 0
		print('Begin adding types')
		while type != '':
			type = input('')
			if type != '':
				try:
					num_frames += int(type_dict[type])
					num_types += 1
					type_list.append(type)
					print('Added %s, Total Frames %i' % (type, num_frames))
				except:
					print('Not valid input')

		print('\nTypes Selected: ', type_list)
		try:
			configs = np.load(in_name + '_n2p2.npy', allow_pickle=True)
		except FileNotFoundError:
			configs = read_configs(dat)
			np.save(in_name + '_n2p2', configs)
		print_out_types(configs, type_list, out_file)

	elif choice == 'e':
		print_out_energy()

	else:
		print('No selection! Bye!')








