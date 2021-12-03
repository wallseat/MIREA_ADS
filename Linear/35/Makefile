ODIR=obj
BDIR=bin
SRCDIR=src

CC=gcc
FLAGS=-Wall -o2 -g

all: queue.o linear_task35.exe

linear_task35.exe: $(SRCDIR)/main.c $(ODIR)/queue.o
	mkdir -p $(BDIR)
	$(CC) -o $(BDIR)/$@ $^

queue.o: $(SRCDIR)/queue.c $(SRCDIR)/queue.h
	mkdir -p $(ODIR)
	$(CC) $(FLAGS) -o $(ODIR)/$@ -c $<