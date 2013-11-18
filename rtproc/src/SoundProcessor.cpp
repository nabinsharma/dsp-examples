// Digital Signal Processing (on Coursera)
//   by Paolo Prandoni, Martin Vetterli
//
// Real-Time Audio Processing - a representative example
// demonstrating baisc DSP algorithms in action - in real time!!!
//
// Original source code by: Paolo Prandoni, Martin Vetterli.
//
// Modified by: Nabin Sharma, Nov 08, 2013.

#include "SoundProcessor.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define PI 3.1415926535897932384626433832795


SoundProcessor::SoundProcessor()
    : m_SR(44100),
      m_Ix(0),
      m_Iy(0),
      m_If(0) {
  memset(m_pX, 0, sizeof(float) * BUF_LEN);
  memset(m_pY, 0, sizeof(float) * BUF_LEN);
}


SoundProcessor::~SoundProcessor() {
}


void SoundProcessor::SetFunction(int ix) {
  m_If = ix;
  m_Ix = 0;
  m_Iy = 0;
  memset(m_pX, 0, sizeof(float) * BUF_LEN);
  memset(m_pY, 0, sizeof(float) * BUF_LEN);
}


float SoundProcessor::Process(float Sample) {
  // Push input sample up input buffer.
  m_pX[m_Ix] = Sample;

  float y = CoreProcess();

  // Push output sample up output buffer.
  m_pY[m_Iy] = y;

  // Increment pointers.
  m_Ix = (m_Ix + 1) % BUF_MASK;
  m_Iy = (m_Iy + 1) % BUF_MASK;

  return y;
}


float SoundProcessor::Delta() {
  return m_pX[m_Ix];
}


float SoundProcessor::Echo() {
  // y[n] = (ax[n] + bx[n-N] + cx[n-2N])/(a+b+c)
  static float a = 1;
  static float b = 0.7f;
  static float c = 0.5f;
  static float norm = 1.0f / (a+b+c);
  static int N = (int)(0.3 * m_SR);

  return norm * (
      a * m_pX[m_Ix]
    + b * m_pX[(m_Ix + BUF_LEN - N) %  BUF_MASK]
    + c * m_pX[(m_Ix + BUF_LEN - 2*N) % BUF_MASK]);
}


float SoundProcessor::IIREcho() {
  // y[n] = x[n] + ay[n-N]
  static float a = 0.7f;
  static float norm = (1 - a * a);
  static int N = (int)(0.3 * m_SR);

  return norm * (
            m_pX[m_Ix]
      + a * m_pY[(m_Iy + BUF_LEN - N) % BUF_MASK]);
}


float SoundProcessor::NaturalEcho() {
  // y[n] = x[n] + y[n-N] * h[n], h[n] is leaky integrator.
  static float a = 0.7f;
  static float norm = 1.0f / (1+a);
  static int N = (int)(0.3 * m_SR);

  return norm * (
                m_pX[m_Ix]
      -     a * m_pX[(m_Ix + BUF_LEN - 1) % BUF_MASK]
      +     a * m_pY[(m_Iy + BUF_LEN - 1) % BUF_MASK]
      + (1-a) * m_pY[(m_Iy + BUF_LEN - N) % BUF_MASK]);
}


float SoundProcessor::Reverb() {
  // y[n] = -ax[n] + x[n-N] + ay[n-N]
  static float a = 0.8f;
  static float norm = 1.0f;
  static int N = (int)(0.02 * m_SR);

  return norm * (
      - a * m_pX[m_Ix]
      +     m_pX[(m_Ix + BUF_LEN - N) % BUF_MASK]
      + a * m_pY[(m_Iy + BUF_LEN - N) % BUF_MASK]);
}


float SoundProcessor::BiQuad() {
  // y[n] = x[n] + b_1x[n-1] + b_2x[n-2] - a_1y[n-1] - a_2y[n-2]
  // Pole (magnitude and phase).
  static float pm = 0.98f;
  static float pp = (float)(0.1 * PI);
  // Zero (magnitude and phase).
  static float zm = 0.9f;
  static float zp = (float)(0.06 * PI);
  static float norm = 0.5f;

  float b1 = -2*zm*cos(zp);
  float b2 = zm*zm;
  float a1 = -2*pm*cos(pp);
  float a2 = pm*pm;

  return norm * (
               m_pX[m_Ix]
        + b1 * m_pX[(m_Ix + BUF_LEN - 1) % BUF_MASK]
        + b2 * m_pX[(m_Ix + BUF_LEN - 2) % BUF_MASK]
        - a1 * m_pY[(m_Iy + BUF_LEN - 1) % BUF_MASK]
        - a2 * m_pY[(m_Iy + BUF_LEN - 2) % BUF_MASK]);
}


float SoundProcessor::Fuzz() {
  // y[n] = a trunc(x[n]/a)
  static float T = 0.005f;
  static float G = 5;

  static float limit = 32767 * T;

  float y = m_pX[m_Ix];
  if (y > limit)
    y = limit;
  if (y < -limit)
    y = -limit;
  return G*y;
}


float SoundProcessor::Tremolo() {
  // y[n] = (1+cos(wn))x[n]

  static double phi = 5 * 2*PI / m_SR;  // 1Hz LFO
  static double omega = 0;

  omega = omega + phi;
  return (float)(((1 + cos(omega))/2) * m_pX[m_Ix]);
}


float SoundProcessor::Flanger() {
  // y[n] = x[n] + x[n - d(1+cos(wn))]

  static int N = (int)(0.002 * m_SR);   // min delay
  static int FD = 2;                    // max delay factor
  static double phi = 1 * 2*PI / m_SR;  // 1Hz LFO
  static double omega = 0;

  int d = (int)(N * FD * (1 + cos(omega))/2);
  omega = omega + phi;
  return 0.5f + (m_pX[m_Ix] + m_pX[(m_Ix + BUF_LEN - d) % BUF_MASK]);
}


float SoundProcessor::Wah() {
  // Max pole deviation.
  static float delta =  (float)(0.3 * PI);
  // LFO frequency.
  static double phi =  (float)(3 * 2*PI / m_SR);
  static double omega = 0;

  // Pole (magnitude and phase).
  static float pm = 0.99f;
  static float pp = (float)(0.04 * PI);
  // Zero (magnitude and phase).
  static float zm = 0.9f;
  static float zp = (float)(0.06 * PI);

  // Pole deviation.
  float d = (float)(delta * (1+cos(omega))/2);
  omega = omega + phi;

  float b1 = -2*zm*cos(zp+d);
  float b2 = zm*zm;
  float a1 = -2*pm*cos(pp+d);
  float a2 = pm*pm;

  float norm = 0.8f;

  return norm * (
             m_pX[m_Ix]
      + b1 * m_pX[(m_Ix + BUF_LEN - 1) % BUF_MASK]
      + b2 * m_pX[(m_Ix + BUF_LEN - 2) % BUF_MASK]
      - a1 * m_pY[(m_Iy + BUF_LEN - 1) % BUF_MASK]
      - a2 * m_pY[(m_Iy + BUF_LEN - 2) % BUF_MASK]);
}
