import subprocess

run_no = 	'4'
inpt_files = 	'topos/coords.'+run_no+'.pdb trajectory.'+run_no+'.dcd'

# Calculate only for last frame
last =		True

# calculate radial distribution function
gofr =		True
gofr_atom = 	['Si', 'Si']
gofr_cutoff =	'3.4'
gofr_outname=	'gofr_'+run_no
# calculate angular distribution function
angd =	True
angd_atom =	['Si', 'Si']
angd_ind =	['100','300']		# atom indices
angd_cutoff =	'3.4' 		# default is neighbor distance
angd_outname =	'angd_'+run_no

substring = 	'~/development/GPTA3/bin/gpta3.x --i '+inpt_files

if last:
	substring+=' --last'
if gofr:
	substring+= ' --gofr'
	# note i+1 to offset python 0 counting
	for i in range(0,len(gofr_atom)):
		substring+=' +s'+str(i+1)+' '+gofr_atom[i]
	substring+=' +r '+gofr_cutoff+' +o '+gofr_outname

if angd:
	substring+= ' --angdist'
	# note i+1 to offset python 0 counting
	for i in range(0,len(angd_atom)):
		substring+=' +s'+str(i+1)+' '+angd_atom[i]
	for i in range(0,len(angd_ind)):
		substring+=' +i'+str(i+1)+' '+angd_ind[i]
	substring+=' +r '+angd_cutoff+' +o '+angd_outname



print(substring)

subprocess.call(substring,shell=True)


