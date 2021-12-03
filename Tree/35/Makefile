ODIR=obj
BDIR=bin
SRCDIR=src

CC=gcc
FLAGS=-Wall -o2 -g

all: tree.o tree_task35.exe

tree_task35.exe: $(SRCDIR)/main.c $(ODIR)/tree.o
	mkdir -p $(BDIR)
	$(CC) -o $(BDIR)/$@ $^

tree.o: $(SRCDIR)/tree.c $(SRCDIR)/tree.h 
	mkdir -p $(ODIR)
	$(CC) $(FLAGS) -o $(ODIR)/$@  -c $<
