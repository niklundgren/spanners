import os
import sys
import numpy as np


if len(sys.argv) < 2:
    print('Please specify available GPU slots')
else:
    cudavisibledevices = sys.argv[2:]
    print('Using GPUs '+' '.join(cudavisibledevices))

prefix = sys.argv[1]
directories = np.array(os.listdir(prefix))
directories = directories[[os.path.isdir(prefix+'/'+d) for d in directories]]
directories = directories[[not os.path.isfile(prefix+'/'+d+'/thermo.out') for d in directories]]
directories.sort()
directories = directories.tolist()

ngpu = len(cudavisibledevices)
njobs = len(directories)
print('directories detected that require gpumd runs are:\n\t'+' '.join(directories))
print('\ttotal jobs: '+str(njobs))
# timeperrun = 500 # in seconds
# estimatedtime = (timeperrun*njobs / ngpu) / 3600
# print('\testimated runtime: {} h'.format(estimatedtime))

n = len(directories)
k = n // ngpu # number of jobs to run per cpu
masterlist = []
for i in range(ngpu):
    masterlist.append([])
for j in range(k):
    for i in range(ngpu):
        masterlist[i].append(directories.pop())
if k*ngpu != n:
    diff = (k*ngpu - n)
    print('Uneven list, appending runs to {} job lists'.format(diff))
    for i in range(len(directories)):
        masterlist[i].append(directories.pop())

print('\n\nFinal job breakdown:\n')
for i in range(ngpu):
    print('\tScript job{}.sh-{} jobs\n\t\t {}'.format(cudavisibledevices[i], len(masterlist[i]), masterlist[i]))

for i in range(ngpu):
    gpu = cudavisibledevices[i]
    with open(prefix+'/job'+str(gpu)+'.sh', 'w') as fout:
        fout.write('export CUDA_VISIBLE_DEVICES="{}"\n'.format(gpu))
        fout.write('for i in '+' '.join(masterlist[i]))
        fout.write('\ndo')
        fout.write('\n\tcd ${i}')
        fout.write('\n\tgpumd > log')
        fout.write('\n\tcd ../')
        fout.write('\ndone')

print('\n\n\tTo run these jobs please enter the following into a command prompt:')
print('\n\t\t bash execute_all.sh')
with open(prefix+'/execute_all.sh', 'w') as fout:
    fout.write('for i in '+' '.join(cudavisibledevices))
    fout.write('\ndo')
    fout.write('\n\tbash job${i}.sh &>> out.job & disown')
    fout.write('\ndone')
