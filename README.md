# Subliminal-Minimal-Gui

## A simple Graphical User Interface for Subliminal.
Made for downloading subtitles quickly from different providers in different languages.
Depends on python 3, subliminal, and PyGObject.
It's built in one script and one configuration file so you can easily add/remove languages/providers
#### Comes with the following languages:
English, Esperanto, Arabic, Hebrew, Russian, and Spanish.
**You can easily change your languages/providers by changing the config.ini file.**
You can download multiple subtitles by simply clicking on the download button as many times as you wish. Each download will be in its own thread. When it does, the progress bar should indicate that by going faster.

## Requirements,
- depends on subliminal, pip install subliminal.
- depends on gtk3+
- depends on Pygobject

Tested on many old machines and limited virtual machines and it's very fast.
Tested on linux and windows.

##ToDo,
- ~~use ConfigParser to set and read settings from a configuration file~~
- download subtitles for a list of movies
- add a tab for searching and downloading subtitles for multiple movies in a folder (add recursive feature too)
- add a tab for choosing a subtitle from a list of availiable subtitles
- add settings tab to choose default settings & which languages/providers to use (edit config file from within app)
- css theme support
