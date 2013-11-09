#include "portAudioPipe.h"

portAudioPipe::portAudioPipe()
{		
}

portAudioPipe::~portAudioPipe()
{
}

//Intialize all the component
void portAudioPipe:: Initial()
{
	//create the Buffer
	int numBytes;   
	numBytes = FRAMES_PER_BUFFER * NUM_CHANNELS * SAMPLE_SIZE ;
  
	sampleBlock = (char *) malloc( numBytes );
	if( sampleBlock == NULL )
  {
		printf("Could not allocate record array.\n");
    exit(1);
  }
  CLEAR( sampleBlock );	
  
	//Initialize the PortAudio library 
	err = Pa_Initialize();
  if( err != paNoError ) 
		error();
	
	//Initialize the input device
  inputParameters.device = Pa_GetDefaultInputDevice(); /* default input device */
  inputParameters.channelCount = NUM_CHANNELS;
  inputParameters.sampleFormat = PA_SAMPLE_TYPE;
  inputParameters.suggestedLatency = Pa_GetDeviceInfo( inputParameters.device )->defaultHighInputLatency ;
  inputParameters.hostApiSpecificStreamInfo = NULL;

	//Initialize the output device
  outputParameters.device = Pa_GetDefaultOutputDevice(); /* default output device */
  outputParameters.channelCount = NUM_CHANNELS;
  outputParameters.sampleFormat = PA_SAMPLE_TYPE;
  outputParameters.suggestedLatency = Pa_GetDeviceInfo( outputParameters.device )->defaultHighOutputLatency;
  outputParameters.hostApiSpecificStreamInfo = NULL;

	//Intialize soundProcessor with Sample rate
	m_soundProcessor.Init(SAMPLE_RATE);
}

void portAudioPipe::Start()
{
	int r;
	char c;	

	//Display all possible sound effect and get the first sound effect
	printOptions();
	option = getchar()- '0';
	m_soundProcessor.SetFunction(option);

	//start the stream
	err = Pa_OpenStream(&stream,
											&inputParameters,
											&outputParameters,
											SAMPLE_RATE,
											FRAMES_PER_BUFFER,
											paClipOff,          /* we won't output out of range samples so don't bother clipping them */
											NULL,               /* no callback, use blocking API */
											NULL );             /* no callback, so no callback userData */
  if( err != paNoError ) 
		error();

  err = Pa_StartStream( stream );
  if( err != paNoError ) 
		error();


	//Infinite loop for all the operations
	while(1)
  {
		r = _kbhit();
		if(r == 0)    // no key is pressed on the keyboard
		{
			err = Pa_ReadStream( stream, sampleBlock, FRAMES_PER_BUFFER );
			if( err && CHECK_OVERFLOW )
				xrun();       
	   
			currentBlock = sampleBlock;
			//read samples from the buffer and put them back after operations
			for(int j=0;j<FRAMES_PER_BUFFER;j++)
			{
				int tmp = *((__int16*)(currentBlock));
				*((__int16*)(currentBlock)) = (__int16)m_soundProcessor.Process((float)tmp);
				currentBlock+=2;		//+2 because the size of the data is two byte
			}
	   
			err = Pa_WriteStream( stream, sampleBlock, FRAMES_PER_BUFFER );
			if( err && CHECK_UNDERFLOW ) 
				xrun();       
		}
		else if (r != 0)	// If user press the keyboard    
		{
			int option = _getch();
			if (option == 'q' || option == 'Q')
			{
				Stop();
				return;
			}
			option -= '0';
			printf("\nYour option is %c\n",option+'0');
			m_soundProcessor.SetFunction(option);
			printOptions();
		}	  
  }
}

void portAudioPipe::Stop()
{
	if( stream ) 
	{
		Pa_AbortStream( stream );
		Pa_CloseStream( stream );
  }
  free( sampleBlock );
  Pa_Terminate();
	return;
}


void portAudioPipe::printOptions()
{
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

void portAudioPipe::error()
{
	if( stream ) 
	{
		Pa_AbortStream( stream );
    Pa_CloseStream( stream );
  }

	free( sampleBlock );
  Pa_Terminate();
  fprintf( stderr, "An error occured while using the portaudio stream\n" );
  fprintf( stderr, "Error number: %d\n", err );
  fprintf( stderr, "Error message: %s\n", Pa_GetErrorText( err ) );
	return;
}


void portAudioPipe::xrun()
{
	if( stream ) 
	{
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