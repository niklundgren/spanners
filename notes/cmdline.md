# COMMANDLINE BASICS

Tab is used as an autocomplete for commands and paths → **this is your best friend**

## Organization, Generally
Everything starts at "/" - this forward-slash with nothing preceding it means your
starting from the VERY top of the folder paths.
The computer keeps a lot of handy things around the /etc directory

## There's No Place Like "/home"
Most things you'll use starts in the /home/<username> directory (where username is 
whatever you selected as your username).

## Special Names

### 1. "./" (Current Directory)
When you open a terminal, it usually defaults to your home directory, but no matter what
it is in SOME directory. The name of the directory you are currently in has a name, but
in bash it also can be referred to as "./"

When writing commands in bash if you see a path that starts with "./" that means the
path starts from whatever directory you're in.

### 2. "../" (Parent Directory)
The directory "above" you (as in the folder containing the folder you're in) is
referred to as "../" (notice the second dot before the slash)

## Let's Go!
We're going to start moving around your computer now. The most important two commands
are going to be: `cd` and `ls`
- `cd` is how you move around the computer, navigating "Directories" (folders)
- `ls` shows you what's in that folder!

## Navigation

### Look Around
ls -a # lists all files (including hidden (files that start with "."))

ls -l # shows files with extra information (e.g. last use, size)

ls -1 # lists ONLY names on separate lines

### Move!
cd <relative path> # move directories

### Special Cases
cd - # return to last directory, in case you moved multiple directories away

mkdir -p ./{monolayer,bilayer}/{300, 500, 800} (makes multiple sets of directories)
less +F (follow and be able to scroll through logs)
ctrl + r - search your command history!!
    then use + to put the command in your cli

pushd <path> / popd # This is one of my favorite ways to move
around. It starts a "stack" (first in; last out) with your current
directory at the bottom and <path> as the second item. To return
to your starting directory enter popd. You can run pushd any number of times
before "popping" back to your initial directory.

ps l # lists the processes owned by your user!

## Running Stuff

### Programs in Bash
You can use any program in your "${PATH}" at any time, in any folder. Generally, the 
computer loads a few basics to start with and you can get fancy by adding things to
your path
A "bin" directory keeps executable binaries (basically, programs) somewhere handy, I
typically keep mine at /home/<username>/bin
Add those directories to your path and suddenly you can call whatever program from
every directory

### Working with Multiple Commands

<c1> | <c2> #pipes the output of one command to the next

<c1> ; <c2> # runs c1 then c2

<c1> & <c2> # runs c1 and c2

<c1> & disown # runs c1, then disowns the task
stdin and stderr are still directed to the terminal so make sure
you direct those somewhere

<c1> > <file> # directs stdout to a file

<c1> 2>&1     # directs stderr to wherever stdout is going

<c1> 2> <file> # directs stderr to a file

### Utilities

tab - autocompletes paths and executables if possible

ctrl-u - cuts before cursor

ctrl-y - pastes

## Bang Commands

Searches your commandline history with regex under the hood.

### Commands
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

### Arguments
<cmd> !:n - executes command with arguments from nth command ago
example: lmp !:1 reruns lammps with the last flags you used

<cmd> !$ - repeats last arguments


---

# SPECIFIC TOOLS

## Contents
1. Text Manipulation
2. System Checks
3. Timing
4. Retrieving Data "en masse"

---

## Text Manipulation
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

# print specific columns from an output stream
<your command outputting text> | awk '{ print $1, $4 }'

## print textfile, but skip lines that include a pattern (xxxx)
awk '(/xxxx/){next}{ print $0 }' txtfile.txt

The expresion you want to match is put inside the /../ within the parenthesis. The
parenthesis are kinda like if statements! and then the two bracketed pieces are the 
condition to perform whether its true or false
awk '(CONDITION){If true: .. }{ Else: .. }' txtfile.txt

You can also string together conditions like
awk '(CONDITION1){If true: .. }{ Else: .. } (CONDITION2){If true: .. } ' txtfile.txt

# replace first instance in each row of a pattern (xxxx) in a text file
sed "s/xxxx/newvalue/" txtfile.txt

# replace all instances in each row of a pattern (xxxx) in a text file
sed "s/xxxx/newvalue/g" txtfile.txt

# Check the tails of n last updated files
# N_files = number of files to check
for file in $(ls -ltr | tail -nN_files | awk '{print $NF}' ); do tail ${file}; done

## System Checks

### Check for Library (Good for Debugging When Compiling)
ldconfig -p | grep <library>
gcc -l<library> # returns "undefined reference to 'main'"

### Count CPUs

Here's a bunch of different ways to do that:
htop - show cores and usage!
lspcu
cat /proc/cpuinfo
top (press 1 to view cores, then 3 after loading to find a node)

### Check GPUs
nvidia-smi
  Use the -i flag to target specific cards (e.g. in our lab, occassionally
one would "fall off the bus" and nvidia-smi would fail unless you used -i to
target the specific GPUs still functioning)

### Check USBs 
lsusb -t
  This let's you know what generation of USB your ports are which can be
helpful when buying hardware, checking compatability, etc.

### Audio
Speakers or audio device not detected after computer wakes from sleep
sudo alsa force-reload
or
systemctl --user restart pulseaudio.service
  Both seem to work when the audio isn't working


## Timing

```bash
timeout <t><s/m/h> <command>  # Run stuff for a certain amount of time
sleep <t><s/m/h>; <command>   # Run stuff after a certain amount of time
```

## Data Retrieval

### Locate Directories with Pattern

Locate directories with pattern using ls piped to grep, save this as a list, then iterate over the directories and execute command.

**Note:** Spacing on export command is important. The `$( <> )` requires space before + after. Also, the semicolons basically separate lines you would use in a bash script but this is executable from CLI.

```bash
export press=$( ls -la | grep -oP "\d\dGPa-1" ); for i in $press; do tail ${i}/thermo.out -n1 | cut -b 64-123; done

# Generic syntax:
export myvariable=$( <command to find dirs> ); for iter in $myvariable; do <command to process data in dirs>; done
```

### Find Files If You've Lost Them

This only works if the system has had a chance to update the database, so files should be older than 1 day. If you want to use this, but the files are kinda new, you can try to ask someone with sudo privileges to run `sudo updatedb` which will allow you to use this.

```bash
locate <filename>
```

### Search Whole File System

This works regardless of when the file was created. I would recommend using your own home directory as the `<dir_to_search>` so you won't run into permission errors.

```bash
find <dir_to_search> --name <filename> | grep "keyword"
```

