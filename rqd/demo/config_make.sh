
#!/bin/sh -xe

./configure --prefix=/usr --libdir=/usr/lib64 "$@"
make -j`nproc`
make install
