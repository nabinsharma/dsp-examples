PA_IDIR = portaudio/include
PA_LDIR = portaudio/lib
SRC_DIR = src

OBJS = $(PA_LDIR)/libportaudio.a $(SRC_DIR)/SoundProcessor.o \
	$(SRC_DIR)/PortAudioPipe.o

CC = g++
CFLAGS = -Wall -c

rtproc: $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o rtproc

main.o: $(SRC_DIR)/main.cpp
	$(CC) $(CFLAGS) $(SRC_DIR)/main.cpp
 
pipe.o: $(PA_IDIR)/portaudio.h
	$(CC) $(CFLAGS) $(SRC_DIR)/PortAudioPipe.cpp

processor.o: $(SRC_DIR)/SoundProcessor.h
	$CC) $(CFLAGS) $(SRC_DIR)/SoundProcessor.cpp

clean:
	\rm $(SRC_DIR)/*.o rtproc
