# Subliminal-Minimal-Gui

#A simple Graphical User Interface for Subliminal.
##Made for downloading subtitles quickly from different providers in different languages.
Depends on python 2, subliminal, and PyGObject.
It's built in one script so you can easily add/remove languages/providers
####Comes with the following languages:
English, Esperanto, Arabic, Hebrew, Russian, and Spanish.
**You can easily add your own languages by changing the script.**
You can download multiple subtitles by simply clicking on the download button as many times as you wish. Each download will be in its own thread. When it does, the progress bar should indicate that by going faster.

##Requirements,
- depends on subliminal, pip install subliminal.
- depends on gtk3+
- depends on Pygobject

Tested on many old machines and limited virtual machines and it's very fast.
Runs on windows and linux.



##ToDo,

download subtitles for a list of movies
choose from different subtitle options in addition to downloading a the best fit
tab views for the different modes while still keeping the interface as simple as possible.

*Do not! use the debian package system for subliminal. It seems the debian package currently is too old a version for this app. this application only works with subliminal from pypi ; pip install subliminal*
