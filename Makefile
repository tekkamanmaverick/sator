
projection.so: projection.o
	gcc -shared -Wl,-soname,projection.so -o projection.so projection.o

projection.o: projection.c
	gcc -c -fPIC projection.c -o projection.o

clean:
	-rm -vf projection.so projection.o projection.pyc
