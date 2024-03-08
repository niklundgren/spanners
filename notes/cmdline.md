########## COMMANDLINE BASICS #####################################
Tab is used as an autocomplete for commands and paths
 --> this is your best friend <--

# Look around and move
ls -a # lists all files (including hidden)

ls -l # shows files with extra information (e.g. last use, size)

ls -1 # lists ONLY file names

cd <relative path> # move directories

pushd <path> / popd # This is one of my favorite ways to move
around. It starts a "stack" (first in; last out) with your current
directory at the bottom and <path> as the second item. To return
to your starting directory enter popd. You can run pushd any number of times
before "popping" back to your initial directory.

ps l # lists the processes owned by your user!

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

tab - autocompletes paths and executables if possible

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


############## SPECIFIC TOOLS #############################
# Contents:
# 1. Text Manipulation
# 2. System Checks
# 3. Timing
# 4. Retrieving data "en masse"
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

# print specific columns
awk '{ print $1, $2 }' txtfile.txt

# replace first instance in each row of a pattern (xxxx) in a text file
sed "s/xxxx/newvalue/" txtfile.txt

# replace all instances in each row of a pattern (xxxx) in a text file
sed "s/xxxx/newvalue/g" txtfile.txt


############### SYSTEM CHECKS #######################
## Check for library (good for debugging when compiling)
ldconfig -p | grep <library>
gcc -l<library> # returns "undefined reference to 'main'"

## Count CPUS
# Here's a bunch of different ways to do that
htop - show cores and usage!
lspcu
cat /proc/cpuinfo
top (press 1 to view cores, then 3 after loading to find a node)

## Check GPUs
nvidia-smi

######### TIMING ###########################################
# Run stuff for a certain amount of time
timeout <t><s/m/h> <command>
# Run stuff after a certain amount of time
sleep <t><s/m/h>; <command>

######### DATA RETRIEVAL  ###########################################
# 0. locate directories with pattern using ls piped to grep, save this as a list, then iterate over the directories and execute command
# Spacing on export command is important. the $( <> ) requires space before + after. Also, the semicolons basically separate
# lines you would use in a bash script but this is executable from CLI
export press=$( ls -la | grep -oP "\d\dGPa-1" ); for i in $press; do tail ${i}/thermo.out -n1 | cut -b 64-123; done
# to help with syntax this is the command without my specific processing commmands
export myvariable=$( <command to find dirs> ); for iter in $myvariable; do <command to process data in dirs>; done

# 1. Find files if you've lost them.
# This only works if the system has had a chance to update the database, so files should be older than 1 day.
# if you want to use this, but the files are kinda new, you can try to ask someone with sudo priviledges to run
# "sudo updatedb" which will allow you to use this.
locate <filename>

# 2. searches whole file system, pipe to grep
# This works regardless of when the file was created. I would reccommend using your own home directory
# as the <dir_to_search> so you won't run into permission errors.
find <dir_to_search> --name <filename> | grep "keyword"

