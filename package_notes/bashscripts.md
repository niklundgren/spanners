
####################################################

### #!/bin/Bash Scripting ##########################

####################################################

    0. Start
    Conventionally, all bash scripts start with
    the line:
    #!/bin/bash 
    Which tells your computer which interpreter to use. It's not required, but its the standard

    1. Baby's first variable
    Variables are stored like: myvar="somevalue"
    Notice that there aren't any spaces.
    Referencing variables is like ${myvar}


####################################################
# Control flows
####################################################

### for loop
for x in <list of stuff>
do
    <cmds>
done

    Try this with {1...10} to make a list of integers from 1 to 10


### if else
if [ ${1} == 2 ]
then
    echo "yes!"
else

fi

    Notice that the tests need spaces between the brackets and -f or a variable name
    Tests that are handy:
    Test if file: [ -f ${filename} ]
    Test if dir:  [ -d ${dirname} ]
    Test if less than: [ 2 -lt 4 ]
    Test if greater:   [ 5 -gt 3 ]
    Test if a file DOESNT exist: [ ! -f ${filename} ]
    Test with or: [ 1 = 1 -o 5 -gt 10 ]
    Test with and: [ 1 = 1 -a 1 = 1 ]

### case - esac
case ${myvar} in
    p)
        if your variable = p then this executes
    ;;
    \?)
        otherwise ...
    ;;
esac


####################################################
## String Manipulation 
####################################################

${file%%.py} removes ".py" from a filename


####################################################
## Flag retrieval 
####################################################

    Set the str in getopts"<str>" to :<a>: where a is some
    flag you'd like to screen for. This syntax accepts
    arguments into a, e.g. -a 4 sets a=4. 

while getopts":p:" opt;
do
    case $opt in
        p)
            <code to run with option p>
        \?)
            echo "Invalid Option"
        ;;
done
