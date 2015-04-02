
vector.so : sparse_vector.o linkedlist.o
	clang -shared -o vector.so sparse_vector.o linkedlist.o -Wall

linkedlist.o : linkedlist.c linkedlist.h
	clang -fpic -c -I /usr/include/python2.7/ -I /usr/lib/python2.7/config-x86_64-linux-gnu/ linkedlist.c -Wall -O3

sparse_vector.o : sparse_vector.c linkedlist.h
	clang -fpic -c -I /usr/include/python2.7/ -I /usr/lib/python2.7/config-x86_64-linux-gnu/ sparse_vector.c -Wall -O3

clean : 
	rm *.o *.so

