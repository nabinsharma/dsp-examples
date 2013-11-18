// Digital Signal Processing (on Coursera)
//   by Paolo Prandoni, Martin Vetterli
//
// Real-Time Audio Processing - a representative example
// demonstrating baisc DSP algorithms in action - in real time!!!
//
// Original source code by: Paolo Prandoni, Martin Vetterli.
//
// Modified by: Nabin Sharma, Nov 08, 2013.

#include "PortAudioPipe.h"

#include <sstream>
#include <string>

namespace {
// Printing accessories.
const int kOptionStartLine = 3;
WINDOW *wnd;
int num_rows, num_cols;
int current_row;

void InitNcurses() {
  wnd = initscr();
  getmaxyx(wnd, num_rows, num_cols);
  current_row = 0;
  noecho();
  nodelay(wnd, TRUE);
  clear();
  refresh();
}

bool ClearScreen() {
  if (current_row > num_rows - 14) {
    current_row = 0;
    return true;
  }
  return false;
}

void PrintSingleLineMsg(std::string msg) {
  mvprintw(current_row, 0, msg.c_str());
  current_row += 1;
  refresh();
}

void HighlightOption(int option, int prev_option) {
  wmove(wnd, prev_option + kOptionStartLine, 0);
  attroff(A_STANDOUT);
  std::stringstream ss;
  ss << prev_option << ": " << kCoreProcesses[prev_option];
  addstr(ss.str().c_str());
  refresh();
  wmove(wnd, option + kOptionStartLine, 0);
  attron(A_STANDOUT);
  ss.str(std::string());
  ss.clear();
  ss << option << ": " << kCoreProcesses[option];
  addstr(ss.str().c_str());
  refresh();
}
}


PortAudioPipe::PortAudioPipe() {
}


PortAudioPipe::~PortAudioPipe() {
}


// Intialize all the components.
void PortAudioPipe:: Initial() {
  // Create the Buffer.
  int numBytes;
  numBytes = FRAMES_PER_BUFFER * NUM_CHANNELS * SAMPLE_SIZE;
  sampleBlock = (char *) malloc(numBytes);
  if (sampleBlock == NULL) {
    printf("Could not allocate record array.\n");
    exit(1);
  }
  CLEAR(sampleBlock);

  // Initialize the PortAudio library.
  err = Pa_Initialize();
  if (err != paNoError)
    error();

  // Initialize the input device.
  inputParameters.device = Pa_GetDefaultInputDevice();
  inputParameters.channelCount = NUM_CHANNELS;
  inputParameters.sampleFormat = PA_SAMPLE_TYPE;
  inputParameters.suggestedLatency = Pa_GetDeviceInfo(
      inputParameters.device)->defaultHighInputLatency;
  inputParameters.hostApiSpecificStreamInfo = NULL;

  // Initialize the output device.
  outputParameters.device = Pa_GetDefaultOutputDevice();
  outputParameters.channelCount = NUM_CHANNELS;
  outputParameters.sampleFormat = PA_SAMPLE_TYPE;
  outputParameters.suggestedLatency = Pa_GetDeviceInfo(
      outputParameters.device)->defaultHighOutputLatency;
  outputParameters.hostApiSpecificStreamInfo = NULL;

  // Intialize SoundProcessor with sample rate.
  m_soundProcessor.Init(SAMPLE_RATE);

  // Initialize printing.
  InitNcurses();
}

void PortAudioPipe::Start() {
  int r;
  // Display all possible sound effect and get the first sound effect.
  PrintOptions();
  int option = 0;
  m_soundProcessor.SetFunction(option);

  // Start the stream.
  err = Pa_OpenStream(
      &stream,
      &inputParameters,
      &outputParameters,
      SAMPLE_RATE,
      FRAMES_PER_BUFFER,
      paClipOff,  // We won't output out of range samples so don't bother
                  // clipping them.
      NULL,       // No callback, use blocking API.
      NULL);     // No callback, so no callback userData.
  if (err != paNoError) {
    endwin();
    error();
  }

  err = Pa_StartStream(stream);
  if (err != paNoError) {
    endwin();
    error();
  }

  // Infinite loop for all the operations.
  while (1) {
    r = getch();
    if (r == ERR) {
      // No key is pressed on the keyboard.
      err = Pa_ReadStream(stream, sampleBlock, FRAMES_PER_BUFFER);
      if (err && CHECK_OVERFLOW) {
        endwin();
        xrun();
      }
      currentBlock = sampleBlock;
      // Read samples from the buffer and put them back after operations.
      for (int j = 0; j < FRAMES_PER_BUFFER; j++) {
        int tmp = *((__int16_t*)(currentBlock));
        *((__int16_t*)(currentBlock)) = (__int16_t)m_soundProcessor.Process(
            (float)tmp);
        currentBlock += 2;  // Size of the data is 2 bytes.
      }
      err = Pa_WriteStream(stream, sampleBlock, FRAMES_PER_BUFFER);
      if (err && CHECK_UNDERFLOW) {
        endwin();
        xrun();
      }
    } else {
      // A key is pressed. (ASCII('0', 'Q', 'q') = (48, 81, 113).
      option = r - 48;
      HighlightOption(option, m_soundProcessor.Option());
      if (option == 33 || option == 65) {
        Stop();
        endwin();
        return;
      }
      m_soundProcessor.SetFunction(option);
      if (ClearScreen()) {
        clear();
        refresh();
        PrintOptions();
      }
    }
  }
}


void PortAudioPipe::Stop() {
  if (stream) {
    Pa_AbortStream(stream);
    Pa_CloseStream(stream);
  }
  free(sampleBlock);
  Pa_Terminate();
  return;
}


void PortAudioPipe::error() {
  if (stream) {
    Pa_AbortStream(stream);
    Pa_CloseStream(stream);
  }
  free(sampleBlock);
  Pa_Terminate();
  fprintf(stderr, "An error occured while using the portaudio stream\n");
  fprintf(stderr, "Error number: %d\n", err);
  fprintf(stderr, "Error message: %s\n", Pa_GetErrorText(err));
  return;
}


void PortAudioPipe::xrun() {
  if (stream) {
    Pa_AbortStream(stream);
    Pa_CloseStream(stream);
  }
  free(sampleBlock);
  Pa_Terminate();
  if (err & paInputOverflow)
    fprintf(stderr, "Input Overflow.\n");
  if (err & paOutputUnderflow)
    fprintf(stderr, "Output Underflow.\n");
  return;
}


void PortAudioPipe::PrintOptions() {
  PrintSingleLineMsg("-----------------------------");
  PrintSingleLineMsg("Please choose a sound effect:");
  PrintSingleLineMsg("-----------------------------");
  for (int i = 0; i < sizeof(kCoreProcesses) / sizeof(kCoreProcesses[0]); ++i) {
    std::stringstream option_msg;
    option_msg << i << ": " << kCoreProcesses[i];
    PrintSingleLineMsg(option_msg.str());
  }
  PrintSingleLineMsg("\nQ: Quit");
}
