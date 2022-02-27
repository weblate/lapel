# coding: utf-8
"""
Common wrappers.
"""
from gi.repository import Gtk

class DialogWrapper(Gtk.Box):
	"""
	GTK widget that shows options for a Mycroft skill dialog.
	"""
	__gtype_name__ = 'DialogWrapper'

	def __init__(self, *args, **kwargs):
		"""Initializes a SuggestionWrapper."""
		super().__init__(*args, **kwargs)

class SuggestionWrapper(DialogWrapper):
	"""
	DialogWrapper widget that provides suggestion buttons.
	"""
	def __init__(self):
		"""Initializes a SuggestionWrapper."""
		super().__init__()
		self.button_revealer = Gtk.Revealer(reveal_child=True, hexpand=True)

		scroll = Gtk.ScrolledWindow(hexpand=True)
		scroll.set_policy(
			Gtk.PolicyType.AUTOMATIC,
			Gtk.PolicyType.NEVER
		)

		self.buttons = Gtk.Box(spacing=6)
		scroll.set_child(self.buttons)

		self.button_revealer.set_child(scroll)
		self.append(self.button_revealer)

	def add_button(self, answer, label=None):
		"""Adds a button to the SuggestionWrapper."""
		if not label:
			label = answer

		button = Gtk.Button(label=label)
		button.connect('clicked', self.do_suggestion, answer)
		button.add_css_class('pill')
		button.add_css_class('suggestion-button')
		self.buttons.append(button)

	def do_suggestion(self, button, answer):
		"""Sends a message from a suggestion."""
		from ..daemon import get_daemon
		get_daemon().send_message(answer)
		self.button_revealer.set_reveal_child(False)

class ConfirmDialog(SuggestionWrapper):
	"""
	SuggestionWrapper with Confirm and Cancel buttons.
	"""
	def __init__(self):
		super().__init__()
		self.add_button('confirm', 'Confirm')
		self.add_button('cancel', 'Cancel')