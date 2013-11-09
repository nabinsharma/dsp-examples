Nabin Sharma
Nov 08, 2013

Platform:
  OSX Mavericks 10.9

Source:
  pa_stable_v19_20111121.tgz , November 21, 2011
  (http://www.portaudio.com/download.html)

Build:
  1. Replace *-Werror* by *-Wall* in CFLAGS (in Mac OS X section of file
     Configure.in).
  2. The file has support up to OSX 10.7 only. So replace
     10.7 in one of the (last) xcodebuild blocks by 10.9.
     For example,
       if xcodebuild -version -sdk macosx10.7 Path >/dev/null 2>&1 ; then
         mac_version_min="-mmacosx-version-min=10.7"
         mac_sysroot="-isysroot `xcodebuild -version -sdk macosx10.7 Path`"
       fi

     should be
       if xcodebuild -version -sdk macosx10.9 Path >/dev/null 2>&1 ; then
         mac_version_min="-mmacosx-version-min=10.9"
         mac_sysroot="-isysroot `xcodebuild -version -sdk macosx10.9 Path`"
       fi
  3. As the configure settings are modified, do
       $autoreconfig -if
  4. Then the normal process
       ./configure
       make
       make install
  5. Portaudio libraries should be availabe at /usr/local/lib
       libportaudio.2.dylib
       libportaudio.a
       libportaudio.dylib
       libportaudio.la
