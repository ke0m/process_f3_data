%.o: %.cpp
	g++ -O3 -fPIC -ffast-math -fopenmp -shared -Wall \
		-I. -c -o $@ $<

INSTALL_DIR=..

default: lvconv1d lvconv2d

lvconv1d: lvconv1d.o 
	g++ -O3 -fPIC -ffast-math -fopenmp -std=c++1y -shared -Wall \
		`${CONDA_PREFIX}/bin/python3 -m pybind11 --includes` \
		-g lvconv1d.o lvconv1dpy.cpp -o \
		$(INSTALL_DIR)/lvconv1d`${CONDA_PREFIX}/bin/python3-config --extension-suffix`

lvconv2d: lvconv2d.o
	g++ -O3 -fPIC -ffast-math -fopenmp -std=c++1y -shared \
		-Wall `${CONDA_PREFIX}/bin/python3 -m pybind11 --includes` \
		-g lvconv2d.o lvconv2dpy.cpp -o \
		$(INSTALL_DIR)/lvconv2d`${CONDA_PREFIX}/bin/python3-config --extension-suffix`
