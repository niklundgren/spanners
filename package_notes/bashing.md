########## BASH BASICS #####################################
Tab is used as an autocomplete for commands and paths
 --> this is your best friend <--

# Look around and move
ls -a # lists all files (including hidden)

ls -l # shows files with extra information (e.g. last use, size)

cd <relative path> # move directories

pushd <absolute path> / popd # This is one of my favorite ways to move
around. It starts a "stack" (first in; last out) with your current
directory at the bottom and <absolute path> as the second item. To return
to your starting directory enter popd. You can run pushd any number of times
before "popping" back to your initial directory.

# Running stuff
<c1> | <c2> #pipes the output of one command to the next

<c1> ; <c2> # runs c1 then c2

<c1> & <c2> # runs c1 and c2

<c1> & disown # runs c1, then disowns the task
stdin and stderr are still directed to the terminal so make sure
you direct those somewhere

<c1> > <file> # directs stdout to a file

<c1> 2>&1     # directs stderr to wherever stdout is going

<c1> 2> <file> # firects stderr to a file

# Utilities
ctrl-u - cuts before cursor

crtl-y - pastes

# Bang Commands ##################################
# searches your commandline history 
# with regex under the hood
# commands:
!! - reruns last command
	protip - sudo !!
	after failed command that needs sudo

!<exp> - executes the last command that startswith the exp
example: !mpirun - reruns your last mpirun command

!?<exp> - executes the last command that matches the exp
example: !?xyz - reruns your last command that used an xyz file
		(e.g. python converter.py <f>.xyz)

!-<n> - executes the n-th last command you used
example: !-3 runs the command you gave three commands ago

!!:s/<old>/<new> - executes the last command with substituded regex
example !!:s^file1^file2 reruns the last command with file2

!:p - prints your last command

# arguments:
<cmd> !:n - executes command with arguments from nth command ago
example: lmp !:1 reruns lammps with the last flags you used

<cmd> !$ - repeats last arguments

### Scripting
## (for use in a <file>.sh script. run with bash <file>.sh)
# for loop
for x in <list of stuff>
do
	<cmds>
done

# if else
if [${1} == 2]; then

else

fi


# command line flag retrieval
- set the str in getopts"<str>" to :<a>: where a is some
flag you'd like to screen for. This syntax accepts
arguments into a, e.g. -a 4 sets a=4. 

while getopts":p:" opt; 
do
        case $opt in
                p)
			<code to run with option p>
                        ;;
                \?)
                        echo "Invalid Option"
                        ;;
done


############## SPECIFIC TOOLS #############################
# Contents:
# 1. Text Manipulation
# 2. System Checks
# 3. Timing
###########################################################
########## TEXT MANIPULATION ##############################
# returns unique results from a regex expression
grep -oP 'config_type=\K\w+' gap_carbon.xyz | sort --unique

# returns counts of unique results from a regex expression
grep -oP "config_type\s\K\w*" test.cfg | sort | uniq -c

## Find text in files
grep <exp> file
	# -c = counts
	# -n = line number
	# -r = all files in dir
	# -v <pattern> = excludes pattern
	# -oP "<pattern>"= use regex


############### SYSTEM CHECKS #######################
## Check for library
ldconfig -p | grep <library>
gcc -l<library> # returns "undefined reference to 'main'"

## Count CPUS
htop - show cores and usage!
lspcu
cat /proc/cpuinfo
top (press 1 to view cores, then 3 after loading to find a node)

## Check GPUs
nvidia-smi

## Find files
locate <filename>
# searches whole file system, pipe to grep
find <dir_to_search> --name <filename>

######### TIMING ###########################################
# Run stuff for a certain amount of time
timeout <t><s/m/h> <command>
# Run stuff after a certain amount of time
sleep <t><s/m/h>; <command>

