INCLUDES = -I/usr/include
# CCFLAGS = -g -O2 -fpic
CCFLAGS = -fPIC -shared
CCC = gcc
LIB = -L/usr/lib/ -l:libprovenance.so -lprovenance -lpthread -lz

disclose:
	$(CCC) $(INCLUDES) $(CCFLAGS) $(LIB) -o disclose2cam.so disclose_prov.c

clean:
	rm -f *.so
