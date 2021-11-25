ODIR=./obj
BDIR=./bin
SRCDIR=./src

CC=gcc
FLAGS=-Wall -o2 -g

all=tree.o main.exe

main.exe: $(SRCDIR)/main.c tree.o
	$(CC) -o $(BDIR)/$@ $(ODIR)/tree.o $<

tree.o: $(SRCDIR)/tree.c $(SRCDIR)/tree.h 
	$(CC) $(FLAGS) -c -o $(ODIR)/$@ $<

