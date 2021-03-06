// Digital Signal Processing (on Coursera)
//   by Paolo Prandoni, Martin Vetterli
//
// Real-Time Audio Processing - a representative example
// demonstrating baisc DSP algorithms in action - in real time!!!
//
// Original source code by: Paolo Prandoni, Martin Vetterli.
//
// Modified by: Nabin Sharma, Nov 08, 2013.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "portaudio.h"

#include "SoundProcessor.h"
#include "PortAudioPipe.h"

#define DITHER_FLAG (0)


int main(void)
{
  // Instantiate a pipe.
  PortAudioPipe m_Pipe;
  m_Pipe.Initial();
  m_Pipe.Start();
  return(0);
}
