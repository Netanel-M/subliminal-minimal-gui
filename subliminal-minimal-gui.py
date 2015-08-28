from __future__ import unicode_literals
import os
from threading import Thread
from babelfish import Language
from subliminal import region, scan_video, download_best_subtitles, save_subtitles

from gi.repository import Gtk, GObject

class SubtitleWindow(Gtk.Window):
	def __init__(self):
		GObject.threads_init()
		Gtk.Window.__init__(self)
		self.connect("delete-event", Gtk.main_quit)
		
		self.region = region.configure('dogpile.cache.memory')
		
		grid = Gtk.Grid()
		self.add( grid )
		
		self.movieEntry = Gtk.Entry()
		openMovie = Gtk.Button( label = "Open Video" )
		bestMatch = Gtk.Button ( label = "Download Best Match")
		openMovie.connect("clicked", self.open_file)
		bestMatch.connect("clicked", self.get_best_match)
		
		self.languageCombo = Gtk.ComboBoxText.new_with_entry()
		self.languageCombo.append_text("eng")
		self.languageCombo.append_text("heb")
		self.languageCombo.append_text("rus")
		self.languageCombo.append_text("ara")
		self.languageCombo.set_active(0)
		
		self.providerCombo = Gtk.ComboBoxText.new()
		self.providerCombo.append_text("opensubtitles")
		self.providerCombo.append_text("podnapisi")
		self.providerCombo.append_text("thesubdb")
		self.providerCombo.append_text("tvsubtitles")
		self.providerCombo.append_text("addic7ed")
		self.providerCombo.set_active(0)
		
		childEntry = self.languageCombo.get_child()
		childEntry.set_width_chars(3)
		
		self.progressBar = Gtk.ProgressBar()
		
		grid.attach(self.movieEntry, 0, 0, 1, 1)
		grid.attach(openMovie, 1, 0, 1, 1)
		grid.attach(self.languageCombo, 2, 0, 1, 1)
		grid.attach(self.providerCombo, 3, 0, 1, 1)
		grid.attach(bestMatch, 4, 0, 1, 1)
		grid.attach(self.progressBar, 0, 1, 5, 1)
		
	def open_file(self, widget):
		dialog = Gtk.FileChooserDialog (
		"Please choose a movie or tv episode", 
		self,
		Gtk.FileChooserAction.OPEN,
		(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
		Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
		)
		
		self.dialog_filters(dialog)
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			fileLocation = dialog.get_filename()
			self.movieEntry.set_text(fileLocation)
			dialog.destroy()
		elif response == Gtk.ResponseType.CANCEL:
			dialog.destroy()
	
	def dialog_filters(self, dialog):
		filter_movie = Gtk.FileFilter()
		filter_movie.set_name("Movie Files")
		filter_movie.add_mime_type("video/mp4")
		filter_movie.add_mime_type("video/x-msvideo")
		filter_movie.add_mime_type("video/x-matroska")
		filter_movie.add_mime_type("video/x-ms-wmv")
		dialog.add_filter(filter_movie)
		
		filter_all = Gtk.FileFilter()
		filter_all.set_name("Other")
		filter_all.add_pattern("*")
		dialog.add_filter(filter_all)
			
	def get_best_match(self, widget):
		self.video = scan_video( self.movieEntry.get_text() )
		x = Thread(target=self.get_best_subtitle)
		x.start()

	def get_best_subtitle(self):
		print "getting subtitles"
		self.timeout = GObject.timeout_add( 100, self.progress_pulse )
		self.subtitle = download_best_subtitles(
		[self.video],
		{ Language( self.languageCombo.get_active_text() ) },
		providers=[self.providerCombo.get_active_text()] )
		
		try:
			self.subtitle = self.subtitle[self.video][0]
		
		except IndexError:
			print "no subtitle found"
			GObject.source_remove(self.timeout)
			self.progressBar.set_fraction(0)
			return False
			
		save_subtitles(self.video, [self.subtitle])
		print "done"
		GObject.source_remove(self.timeout)
		self.progressBar.set_fraction(1)
		
	def progress_pulse(self):
		self.progressBar.pulse()
		return True
		
if __name__ == "__main__":
	
	window = SubtitleWindow()
	window.show_all()
	Gtk.main()
