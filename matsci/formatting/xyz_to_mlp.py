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
		nlat = '\t'+lat[0]+'\t'+lat[1]+'\t'+lat[2]+'\n'
		nlat += '\t'+lat[3]+'\t'+lat[4]+'\t'+lat[5]+'\n'
		nlat += '\t'+lat[6]+'\t'+lat[7]+'\t'+lat[8]+'\n'
		observables['Lattice'] = nlat


		# Parse atomic info
		# gap xyz format = Species X Y Z AtomicNum Fx Fy Fz
		n_descriptors = len(cfg[2].split())
		atoms = np.empty((n_atoms, n_descriptors+1), dtype='<U10')
		atoms[:, 0] = range(1, n_atoms+1)
		for i in range(n_atoms):
			atom = cfg[i+2].split()
			atoms[i, 2:] = atom[1:]
		atoms = np.delete(atoms, 5, 1)
		atoms[:, 1] = '0'


		# Format atomic info
		tabs = np.repeat(['\t'], atoms.shape[0])[:,None]
		nlines = np.repeat(['\n'], atoms.shape[0])[:,None]
		atom_strings = [('\t').join(line) for line in np.concatenate((tabs, atoms, nlines), axis=1)]
		system_string = ''
		for i in atom_strings:
			system_string += i


		# Format write string
		write = 'BEGIN_CFG\n'
		write += ' Size\n'
		write += '\t'+str(n_atoms)+'\n'
		write += ' Supercell\n'
		write += nlat.strip("\"")+'\n'
		write += ' AtomData:\tid\ttype\tcartes_x\tcartes_y\tcartes_z\tfx\tfy\tfz\n'
		write += system_string
		write += ' Energy\n\t'+observables['energy']+'\n'
		for i in ['config_type']:
			write += ' Feature\t'+i+'\t'+observables[i]+'\n'
		write += 'END_CFG\n'


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
	to_write = configs[frames]
	writes = to_write['config']
	for config in writes:
		print(config, file=file)
	print('Finished!')


def print_out_types(configs, types, file):
	for t in types:
		single_type_confs = configs[configs['config_type'] == t]
		writes = single_type_confs['config']
		for conf in writes:
			print(conf, file=file)
	print('Finished!')


def print_out_energy(configs, type, num, file, num2=None):
	if type == 'percentile': # reported in percent (e.g. 50% = 50)
		n_configs = len(configs)
		take = int(n_configs * num / 100)
		sorted = np.sort(configs['energy'])
		writes = configs[take:]
		for conf in writes:
			print(conf, file=file)




### Debugging
debug_conf = False

# Get user input + collect data
print('Input\n--------------')
if not debug_conf:
	in_name = input('XYZ file without extension: ')
else:
	in_name = 'gap_carbon'
try:
	dat = np.load(in_name+'.npy', allow_pickle=True)
	n_configs = len(dat)
	print(str(n_configs)+' numpy frames detected')
except FileNotFoundError:
	f = open(in_name+'.xyz', 'r')
	dat = f.readlines()
	n_configs = count_configs(dat)
	print(str(n_configs)+' frames detected')


print('Output\n--------------')
if not debug_conf:
	out_name = input('Insert new name, if desired (default <xyz_name>.cfg): ')
	if out_name == "":
		out_name = in_name
	if os.path.exists(out_name+'.cfg'):
		check = input('This file exists, overwrite? (y)')
		if check != 'y':
			print('exiting!')
			exit()
		else:
			print('Overwriting '+out_name+'.cfg')
	out_file = open(out_name+'.cfg', 'w+')
else:
	out_file = open('cfg.cfg', 'w+')



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
		print('Counts start at 1\nEnter lists exactly like-\nstart1:stop1, start2:stop2, ...')
		frames = input('Range of frames:\n')
		ranges = frames.split(',')
		if frames != '':
			print('Detected ' + str(len(ranges)) + ' ranges of frames')
			for r in ranges:
				frames_list.append(list(range(r[0], r[1]+1)))
			print('Total num frames: '+str(len(frames_list)))
		try:
			configs = np.load(in_name+'_mlp.npy', allow_pickle=True)
		except FileNotFoundError:
			configs = read_configs(dat)
			np.save(in_name+'_mlp', configs)
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
		print('Begin adding types.')
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
			configs = np.load(in_name+'_mlp.npy', allow_pickle=True)
		except FileNotFoundError:
			configs = read_configs(dat)
			np.save(in_name+'_mlp', configs)
		print_out_types(configs, type_list, out_file)

	elif choice == 'e':
		print_out_energy()

	else:
		print('No selection! Bye!')








