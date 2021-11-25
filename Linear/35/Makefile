CC=gcc

all: queue.o main.bin

queue.o: src/queue.c src/queue.h
	$(CC) -c -g -Isrc/ $< -o obj/$@ 

main.bin: obj/queue.o
	$(CC) src/main.c -g -o bin/$@ $^

clean:
	rm -f *.o 