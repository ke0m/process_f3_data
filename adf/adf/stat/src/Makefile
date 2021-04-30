.o: %.cpp
	g++ -O3 -fPIC -ffast-math -fopenmp -shared -Wall \
		-I. -I../../../../external_cpp/ -c -o $@ $<

INSTALL_DIR=..

default: conv1d

conv1d: conv1d.o 
	g++ -O3 -fPIC -ffast-math -fopenmp -std=c++1y -shared -Wall \
		`${CONDA_PREFIX}/bin/python3 -m pybind11 --includes` \
		-g conv1d.o conv1dpy.cpp -o \
		$(INSTALL_DIR)/conv1d`${CONDA_PREFIX}/bin/python3-config --extension-suffix`
