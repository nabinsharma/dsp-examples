// Digital Signal Processing (on Coursera)
//   by Paolo Prandoni, Martin Vetterli
//
// Real-Time Audio Processing - a representative example
// demonstrating baisc DSP algorithms in action - in real time!!!
//
// Original source code by: Paolo Prandoni, Martin Vetterli.
//
// Modified by: Nabin Sharma, Nov 08, 2013.

#pragma once

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <ncurses.h>

#include "PortAudio.h"

#include "SoundProcessor.h"

#define SAMPLE_RATE  (44100)
#define FRAMES_PER_BUFFER (4)
#define NUM_CHANNELS    (1)
#define NUM_SECONDS     (15)
/*
  @todo Underflow and overflow is disabled until we fix priming of
  blocking write.
*/
#define CHECK_OVERFLOW  false
#define CHECK_UNDERFLOW  false

/* Select sample format. */
#if 0
#define PA_SAMPLE_TYPE  paFloat32
#define SAMPLE_SIZE (4)
#define SAMPLE_SILENCE  (0.0f)
#define CLEAR(a) memset((a), 0, FRAMES_PER_BUFFER * NUM_CHANNELS * \
                         SAMPLE_SIZE)
#define PRINTF_S_FORMAT "%.8f"
#elif 1
#define PA_SAMPLE_TYPE  paInt16
#define SAMPLE_SIZE (2)
#define SAMPLE_SILENCE  (0)
#define CLEAR(a) memset((a), 0,  FRAMES_PER_BUFFER * NUM_CHANNELS * \
                         SAMPLE_SIZE)
#define PRINTF_S_FORMAT "%d"
#elif 0
#define PA_SAMPLE_TYPE  paInt24
#define SAMPLE_SIZE (3)
#define SAMPLE_SILENCE  (0)
#define CLEAR(a) memset((a), 0,  FRAMES_PER_BUFFER * NUM_CHANNELS * \
                         SAMPLE_SIZE)
#define PRINTF_S_FORMAT "%d"
#elif 0
#define PA_SAMPLE_TYPE  paInt8
#define SAMPLE_SIZE (1)
#define SAMPLE_SILENCE  (0)
#define CLEAR(a) memset((a), 0,  FRAMES_PER_BUFFER * NUM_CHANNELS *  \
                         SAMPLE_SIZE)
#define PRINTF_S_FORMAT "%d"
#else
#define PA_SAMPLE_TYPE  paUInt8
#define SAMPLE_SIZE (1)
#define SAMPLE_SILENCE  (128)
#define CLEAR(a) { \
    int i; \
    for (i = 0; i < FRAMES_PER_BUFFER*NUM_CHANNELS; i++) \
        ((unsigned char *)a)[i] = (SAMPLE_SILENCE); \
}
#define PRINTF_S_FORMAT "%d"
#endif

class PortAudioPipe {
 public:
  PortAudioPipe();
  virtual ~PortAudioPipe();
  void Initial();
  void Start();
  void Stop();
  void PrintOptions();
  void error();
  void xrun();

  SoundProcessor m_soundProcessor;

 private:
  PaStreamParameters inputParameters, outputParameters;
  PaStream *stream;
  PaError err;
  char *sampleBlock, *samplePointer;
  char *currentBlock;
  int option;
};
