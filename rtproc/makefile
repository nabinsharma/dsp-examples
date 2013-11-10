SYS_LDIR = /usr/lib
PA_IDIR = portaudio/include
PA_LDIR = portaudio/lib
SRC_DIR = src

OBJS = $(PA_LDIR)/libportaudio.dylib $(SRC_DIR)/main.o \
	$(SRC_DIR)/SoundProcessor.o $(SRC_DIR)/PortAudioPipe.o

CC = g++
CFLAGS = -Wall -g -c
LFLAGS = -Wall -g

rtproc: $(OBJS)
	$(CC) $(LFLAGS) $(OBJS) \
	$(SYS_LDIR)/libstdc++.dylib $(SYS_LDIR)/libncurses.dylib \
	-o rtproc

main.o: $(SRC_DIR)/main.cpp
	$(CC) $(CFLAGS) $(SRC_DIR)/main.cpp

pipe.o: $(PA_IDIR)/portaudio.h
	$(CC) $(CFLAGS) $(SRC_DIR)/PortAudioPipe.cpp

processor.o: $(SRC_DIR)/SoundProcessor.h
	$CC) $(CFLAGS) $(SRC_DIR)/SoundProcessor.cpp

clean:
	rm *.o $(SRC_DIR)/*.o rtproc
