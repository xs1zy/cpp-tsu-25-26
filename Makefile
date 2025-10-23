CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra

analyze.exe: main.cpp libminimum.so libaverage-read_data.so libconvert_product-selection_sort.a
	$(CXX) $(CXXFLAGS) main.cpp \
	-L. -lminimum -laverage-read_data \
	libconvert_product-selection_sort.a \
	-Wl,-rpath,. \
	-o analyze.exe

libminimum.so: minimum.cpp
	$(CXX) $(CXXFLAGS) -shared -fPIC minimum.cpp -o libminimum.so

libaverage-read_data.so: average.cpp read_data.cpp
	$(CXX) $(CXXFLAGS) -shared -fPIC average.cpp read_data.cpp -o libaverage-read_data.so

libconvert_product-selection_sort.a: convert_product.cpp selection_sort.cpp
	$(CXX) $(CXXFLAGS) -c convert_product.cpp selection_sort.cpp
	ar rcs libconvert_product-selection_sort.a convert_product.o selection_sort.o

clean:
	rm -f *.o *.a *.so analyze.exe
