
CC = gcc

all: binning.so projection.so

%.so: %.o
	$(CC) -shared -Wl,-soname,$@ -o $@ $<

%.o: %.c
	$(CC) -c -fPIC $< -o $@

clean:
	rm -f *.o
	rm -f *.so
