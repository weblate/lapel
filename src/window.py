# coding: utf-8
"""
Main window creation code.
"""
import sys
import gi

gi.require_version('Adw', '1')
gi.require_version('Gtk', '4.0')

from gi.repository import Adw, Gtk, Gio

from .assistant import AssistantContent
from .skills_page import SkillsContent
from .daemon import start_daemon, get_daemon

@Gtk.Template(resource_path='/org/dithernet/lapel/ui/window.ui')
class LapelWindow(Adw.ApplicationWindow):
	"""Main window for the program."""
	__gtype_name__ = 'LapelWindow'

	content_stack = Gtk.Template.Child()
	assistant_page = Gtk.Template.Child()

	no_connection = Gtk.Template.Child()
	no_connection_status = Gtk.Template.Child()

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.daemon = get_daemon()

		self.daemon.client.on('error', self.handle_error)
		self.daemon.client.on('mycroft.ready', self.ready)
		self.no_connection.hide()

		self.daemon.refresh_skills()

	def handle_error(self, error):
		"""Handles errors."""
		print(error)
		self.no_connection.show()
		self.no_connection.set_reveal_child(True)
		self.assistant_page.get_child().content_flap.set_reveal_flap(False)

	def ready(self, *args):
		"""Recovers after an error."""
		self.no_connection.set_receives_default(False)
		self.no_connection.set_reveal_child(False)
		self.no_connection.hide()
		self.daemon.refresh_skills()

@Gtk.Template(resource_path='/org/dithernet/lapel/ui/about.ui')
class AboutDialog(Gtk.AboutDialog):
	"""Main about dialog for Assistant."""
	__gtype_name__ = 'AboutDialog'

	def __init__(self, parent):
		Gtk.AboutDialog.__init__(self)
		self.props.version = "0.1.0"
		self.set_transient_for(parent)

class Application(Adw.Application):
	def __init__(self):
		super().__init__(
			application_id='org.dithernet.lapel',
			flags=Gio.ApplicationFlags.FLAGS_NONE,
			resource_base_path='/org/dithernet/lapel/'
		)
		start_daemon()

	def do_activate(self):
		win = self.props.active_window
		if not win:
			win = LapelWindow(application=self)
		self.create_action('about', self.on_about_action)
		win.present()

	def on_about_action(self, widget, _):
		about = AboutDialog(self.props.active_window)
		about.present()

	def on_preferences_action(self, widget, _):
		print('app.preferences action activated')

	def create_action(self, name, callback):
		"""Add an action and connect it to a callback."""
		action = Gio.SimpleAction.new(name, None)
		action.connect("activate", callback)
		self.add_action(action)

def main(version):
	app = Application()
	return app.run(sys.argv)
