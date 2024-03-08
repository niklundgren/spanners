
#################################################
###### Compiling is a bitch.
#################################################

Here's some examples of different compiling errors and the ways I got around them.
You may also find some helpful things in my command line notes like ways to find libraries ("lib<..>.so" or "lib<..>.a" files)

# g++

    If you are missing a library (e.g. fatal error: <lib name>: No such file or directory)
    You probably need to include a path to some specific library.
    Try running locate <lib name> to find it on your machine
    Then add the path to that library into the make file, or configure options as a flag
    to the g++ compilers. It should look something like this:

INITIAL ERROR: (encountered compiling lzlib.h for use with QE)
'''
> g++  -Wall -W -O2 -c -o compress.o compress.cc
compress.cc:34:10: fatal error: lzlib.h: No such file or directory
   34 | #include <lzlib.h>
      |          ^~~~~~~~~
'''

RUN LOCATE (or however you want to find the file)
'''
> locate lzlib.h (or find /home/nlundgre -iname lzlib.h)
/home/nlundgre/develop/lzlib-1.10/lzlib.h
/home/nlundgre/develop/lzlib-1.10/include/lzlib.h
'''

ADD FLAG TO `./configure` FILE
'''
CXXFLAGS='-I/home/nlundgre/develop/lzlib-1.10/ -Wall -W -O2'
'''

    Where in this case I needed to add a header file ("lzlib.h").



