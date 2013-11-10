Digital Signal Processing (Coursera/EPFL)
by Paolo Prandoni, Martin Vetterli

Real-time audio processing in C++ for Mac OS X Mavericks

Original source code (provided in the course website
https://class.coursera.org/dsp-002/wiki/view?page=RTproc):
https://spark-public.s3.amazonaws.com/dsp/num_examples/rtproc.zip


The original source had conio.h as shell input/output utility.
The related functionalities have been fulfilled by ncurses.h
(it has been assumed that ncurses is part of your system
libraries - check /usr/lib).

From rtproc folder, run makefile to get rtproc binary.

Use (mic/)headphone instead of lounspeaker to avoid feedback
issues.

Nabin Sharma
Nov 12, 2013
