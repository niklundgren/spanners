import shutil
import os
import sys

# Select GPUs
if len(sys.argv) < 2:
    print('Please specify available GPU slots')
else:
    cudavisibledevices = sys.argv[1:]
    print('Using GPUs '+' '.join(cudavisibledevices))


# Select directories
with open('resources/J2R', 'r') as fin:
    jobs = fin.readlines()
jobs = [j.strip() for j in jobs]
njobs = len(jobs)
ngpu = len(cudavisibledevices)
k = njobs // ngpu # number of jobs to run per cpu
masterlist = []
for i in range(ngpu):
    masterlist.append([])
for j in range(k):
    for i in range(ngpu):
        masterlist[i].append('../'+jobs.pop())
if k*ngpu != njobs:
    diff = (k*ngpu - njobs)
    print('Uneven list, appending runs to {} job lists'.format(diff))
    for i in range(jobs):
        masterlist[i].append(jobs.pop())

print('\n\nFinal job breakdown:\n')
for i in range(ngpu):
    print('\tScript job{}.sh-{} jobs\n\t\t {}'.format(cudavisibledevices[i], len(masterlist[i]), masterlist[i]))

for i in range(ngpu):
    gpu = cudavisibledevices[i]
    with open('resources/job'+str(gpu)+'.sh', 'w') as fout:
        fout.write('#!/bin/bash\n')
        fout.write('export CUDA_VISIBLE_DEVICES="{}"\n'.format(gpu))
        fout.write('cd ../\n')
        fout.write('for i in '+' '.join(masterlist[i]))
        fout.write('\ndo')
        fout.write('\n\tcd ${i}')
        fout.write('\n\tgpumd > log')
        fout.write('\n\tcd ../')
        fout.write('\ndone')

with open('execute_jobs.sh', 'w') as fout:
    fout.write('#!/bin/bash\n')
    fout.write('rm resources/J2R\n')
    fout.write('cd resources\n')
    fout.write('for i in '+' '.join(cudavisibledevices))
    fout.write('\ndo')
    fout.write('\n\tbash job${i}.sh &>> jobs.out & disown')
    fout.write('\ndone')

