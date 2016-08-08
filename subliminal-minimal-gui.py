from __future__ import unicode_literals
from threading import Thread
from babelfish import Language
from subliminal import region, scan_video, download_best_subtitles, save_subtitles

from gi.repository import Gtk, GObject

class SubtitleWindow(Gtk.Window):
	def __init__(self):
		GObject.threads_init()
		Gtk.Window.__init__(self)
		# Initial configuration
		self.set_resizable(False)
		self.set_title("Subliminal Minimal GUI")
		self.region = region.configure('dogpile.cache.memory')
		
		# Widget creation and initial config
		notebook = Gtk.Notebook()
		grid = Gtk.Grid()
		frame = Gtk.Frame( label="Download a Single Subtitle" )
		grid.set_column_spacing(10)
		grid.set_row_spacing(10)
		self.add( notebook )
		frame.add( grid )
		notebook.append_page( frame, Gtk.Label("Single Sub") )
		self.movie_entry = Gtk.Entry()
		open_movie = Gtk.Button( label = "Open Video" )
		best_match = Gtk.Button ( label = "Download Best Match")
		language_label = Gtk.Label("Language")
		video_label = Gtk.Label("Video File")
		provider_label = Gtk.Label("Provider")
		self.language_combo = Gtk.ComboBoxText.new_with_entry()
		self.progress_bar = Gtk.ProgressBar()

		# Append languages to a combo box
		self.language_combo.append_text("eso")
		self.language_combo.append_text("eng")
		self.language_combo.append_text("heb")
		self.language_combo.append_text("rus")
		self.language_combo.append_text("ara")
		self.language_combo.append_text("spa")
		self.language_combo.set_active(0)
		
		# Append providers to a combo box
		self.provider_combo = Gtk.ComboBoxText.new()
		self.provider_combo.append_text("addic7ed")
		self.provider_combo.append_text("legendastv")
		self.provider_combo.append_text("opensubtitles")
		self.provider_combo.append_text("podnapisi")
		self.provider_combo.append_text("shooter")
		self.provider_combo.append_text("subscenter")
		self.provider_combo.append_text("thesubdb")
		self.provider_combo.append_text("tvsubtitles")
		self.provider_combo.set_active(0)
		
		# Grid placement
		grid.attach(video_label, 0, 0, 5, 1)
		grid.attach(self.movie_entry, 0, 1, 2, 1)
		grid.attach(open_movie, 2, 1, 2, 1)
		grid.attach(language_label, 0, 2, 1, 1)
		grid.attach(self.language_combo, 0, 3, 2, 1)
		grid.attach(provider_label, 2, 2, 2, 1)
		grid.attach(self.provider_combo, 3, 3, 1, 1)
		grid.attach(best_match, 0, 6, 5, 1)
		grid.attach(self.progress_bar, 0, 5, 5, 1)
		
		# Margin config
		frame.set_margin_left(10)
		frame.set_margin_right(10)
		frame.set_margin_top(10)
		frame.set_margin_bottom(10)
		self.language_combo.set_margin_left(10)
		best_match.set_margin_bottom(10)
		best_match.set_margin_left(10)
		best_match.set_margin_right(10)
		self.movie_entry.set_margin_left(10)
		video_label.set_margin_top(10)
		
		# Connect events
		open_movie.connect( "clicked", self.open_file )
		best_match.connect( "clicked", self.get_best_match )
		self.connect("delete-event", Gtk.main_quit)
		
	def open_file(self, widget):
		# Open a file dialog and movie the chosen movie location to the movie entry
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
			self.movie_entry.set_text(fileLocation)
			dialog.destroy()
		elif response == Gtk.ResponseType.CANCEL:
			dialog.destroy()
	
	def dialog_filters(self, dialog):
		# Filters for dialog box
		filter_movie = Gtk.FileFilter()
		filter_movie.set_name("Movie Files")
		filter_movie.add_pattern("*.mkv")
		filter_movie.add_pattern("*.avi")
		filter_movie.add_pattern("*.wmv")
		filter_movie.add_pattern("*.mp4")

		dialog.add_filter(filter_movie)
		
		filter_all = Gtk.FileFilter()
		filter_all.set_name("Other")
		filter_all.add_pattern("*")
		dialog.add_filter(filter_all)
			
	def get_best_match(self, widget):
		# Open a thread to find a subtitle through get_best_subtitle
		self.video = scan_video( self.movie_entry.get_text() )
		x = Thread(target=self.get_best_subtitle)
		x.start()

	def get_best_subtitle(self):
		# Get a subtitle for a given video file 
		print "getting subtitles"
		self.timeout = GObject.timeout_add( 100, self.progress_pulse )
		self.subtitle = download_best_subtitles(
		[self.video],
		{ Language( self.language_combo.get_active_text() ) },
		providers=[self.provider_combo.get_active_text()] )
		
		try:
			self.subtitle = self.subtitle[self.video][0]
		
		except IndexError:
			print "no subtitle found"
			GObject.source_remove(self.timeout)
			self.progress_bar.set_fraction(0)
			return False
			
		save_subtitles(self.video, [self.subtitle])
		print "done"
		GObject.source_remove(self.timeout)
		self.progress_bar.set_fraction(1)
		
	def progress_pulse(self):
		self.progress_bar.pulse()
		return True
		

if __name__ == "__main__":
	
	window = SubtitleWindow()
	window.show_all()
	Gtk.main()
