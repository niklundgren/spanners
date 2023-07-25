./configure --enable-openmp --enable-mpi --enable-threads --prefix=/home/nwlundgren/develop/fftw-3.3.9/build --enable-static --enable-shared --enable-sse2 --enable-avx
make -j50 all
make install
