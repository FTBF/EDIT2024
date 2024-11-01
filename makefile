all: otsEthTest

otsEthTest: EthernetInterface.cpp EthernetInterface.h otsEthTest.cpp 
	g++ -O3 -o $@ $^ -lpthread

clean:
	rm otsEthTest
