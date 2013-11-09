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

class SoundProcessor {
 public:
	SoundProcessor(void);
	~SoundProcessor(void);
	void SetFunction(int ix);
	void Init(int SamplingRate) {m_SR = SamplingRate;};
	float Process(float Sample);

 protected:	
	// Core processing algorithms.
	float Delta();
	float Echo();
	float IIREcho();
	float NaturalEcho();
	float Reverb();
	float BiQuad();
	float Tremolo();
	float Fuzz();
	float Flanger();
	float Wah();

	// Sampling rate.
	int m_SR;
  
	// 10 sec @ 24KHz.
	enum {BUF_LEN = 60000};
	enum{BUF_MASK=BUF_LEN};
	float m_pY[BUF_LEN];
	float m_pX[BUF_LEN];
	int m_Ix;
	int m_Iy;
	int m_If;

	enum {MAX_ENTRIES = 20};	

	float CoreProcess() {
		float y;
		switch(m_If) {
      case 0:
      default:
        y = Delta();
        break;
      case 1:
        y = Echo();
        break;
      case 2:
        y = IIREcho();
        break;
      case 3:
        y = NaturalEcho();
        break;
      case 4:
        y = Reverb();
        break;
      case 5:
        y = BiQuad();
        break;
      case 6:
        y = Fuzz();
        break;
      case 7:
        y = Flanger();
        break;
      case 8:
        y = Wah();
        break;
      case 9:
        y = Tremolo();
        break;
		}
		return y;
	}
};
