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


PortAudioPipe::PortAudioPipe() {		
}


PortAudioPipe::~PortAudioPipe() {
}


// Intialize all the components.
void PortAudioPipe:: Initial() {
	// Create the Buffer.
	int numBytes;
	numBytes = FRAMES_PER_BUFFER * NUM_CHANNELS * SAMPLE_SIZE ;
  
	sampleBlock = (char *) malloc( numBytes );
	if( sampleBlock == NULL ) {
		printf("Could not allocate record array.\n");
    exit(1);
  }
  CLEAR( sampleBlock );	
  
	// Initialize the PortAudio library .
	err = Pa_Initialize();
  if( err != paNoError ) 
		error();
	
	// Initialize the input device.
  inputParameters.device = Pa_GetDefaultInputDevice();
  inputParameters.channelCount = NUM_CHANNELS;
  inputParameters.sampleFormat = PA_SAMPLE_TYPE;
  inputParameters.suggestedLatency = Pa_GetDeviceInfo(
      inputParameters.device )->defaultHighInputLatency ;
  inputParameters.hostApiSpecificStreamInfo = NULL;

	// Initialize the output device.
  outputParameters.device = Pa_GetDefaultOutputDevice();
  outputParameters.channelCount = NUM_CHANNELS;
  outputParameters.sampleFormat = PA_SAMPLE_TYPE;
  outputParameters.suggestedLatency = Pa_GetDeviceInfo(
      outputParameters.device )->defaultHighOutputLatency;
  outputParameters.hostApiSpecificStreamInfo = NULL;

	// Intialize SoundProcessor with sample rate.
	m_soundProcessor.Init(SAMPLE_RATE);
}

void PortAudioPipe::Start() {
	int r;
	char c;	

	// Display all possible sound effect and get the first sound effect.
	PrintOptions();
	option = getchar()- '0';
	m_soundProcessor.SetFunction(option);

	// Start the stream.
	err = Pa_OpenStream(
      &stream,
      &inputParameters,
      &outputParameters,
      SAMPLE_RATE,
      FRAMES_PER_BUFFER,
      paClipOff,  // We won't output out of range samples so don't bother clipping them.
      NULL,       // No callback, use blocking API.
      NULL );     // No callback, so no callback userData.
  if( err != paNoError ) 
		error();

  err = Pa_StartStream( stream );
  if( err != paNoError ) 
		error();

	// Infinite loop for all the operations.
  nodelay(stdscr, TRUE);
	while(1) {
		r = getch();
		if(r == ERR) {
      // No key is pressed on the keyboard.
			err = Pa_ReadStream( stream, sampleBlock, FRAMES_PER_BUFFER );
			if( err && CHECK_OVERFLOW )
				xrun();

			currentBlock = sampleBlock;
			// Read samples from the buffer and put them back after operations.
			for(int j=0;j<FRAMES_PER_BUFFER;j++) {
				int tmp = *((__int16*)(currentBlock));
				*((__int16*)(currentBlock)) = (__int16)m_soundProcessor.Process((float)tmp);
				currentBlock+=2;		// Size of the data is 2 bytes.
			}

			err = Pa_WriteStream( stream, sampleBlock, FRAMES_PER_BUFFER );
			if( err && CHECK_UNDERFLOW ) 
				xrun();       
		} else {
      // A key is pressed.
			int option = getch();
			if (option == 'q' || option == 'Q') {
				Stop();
				return;
			}
			option -= '0';
			printf("\nYour option is %c\n",option+'0');
			m_soundProcessor.SetFunction(option);
			PrintOptions();
		}
  }
}


void PortAudioPipe::Stop() {
	if( stream ) {
		Pa_AbortStream( stream );
		Pa_CloseStream( stream );
  }
  free( sampleBlock );
  Pa_Terminate();
	return;
}


void PortAudioPipe::PrintOptions() {
	printf("#####################################\n");
	printf("Please choose a sound effect:\n");
	printf("0: delta\n");
	printf("1: echo\n");
	printf("2: IIR echo\n");
	printf("3: natural echo\n");
	printf("4: reverb\n");
	printf("5: biquad\n");
	printf("6: fuzz\n");
	printf("7: flanger\n");
	printf("8: wah\n");
	printf("9: tremolo\n");
	printf("\n");
	printf("Q: quit\n");
}


void PortAudioPipe::error() {
	if( stream ) {
		Pa_AbortStream( stream );
    Pa_CloseStream( stream );
  }
  free(sampleBlock);
  Pa_Terminate();
  fprintf(stderr, "An error occured while using the portaudio stream\n");
  fprintf(stderr, "Error number: %d\n", err);
  fprintf(stderr, "Error message: %s\n", Pa_GetErrorText(err));
	return;
}


void PortAudioPipe::xrun() {
	if( stream ) {
		Pa_AbortStream( stream );
		Pa_CloseStream( stream );
  }
  free( sampleBlock );
  Pa_Terminate();
  if( err & paInputOverflow )
    fprintf( stderr, "Input Overflow.\n" );
  if( err & paOutputUnderflow )
    fprintf( stderr, "Output Underflow.\n" );
	return;
}
