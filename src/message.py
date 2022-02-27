# coding: utf-8
"""
Code for storing information about messages.
"""
from gi.repository import Gtk, GObject

class LapelMessage(GObject.Object):
	"""
	GObject wrapper for Mycroft messages.
	"""
	__gtype_name__ = 'LapelMessage'

	def __init__(self, message):
		"""Initializes a LapelMessage object."""
		super().__init__()
		self.message = message

	def to_mycroft_message(self):
		"""Returns the Mycroft message stored by the LapelMessage object."""
		return self.message

	@GObject.Property(type=str, flags=GObject.ParamFlags.READABLE)
	def type(self):
		"""Type of message."""
		return self.message.msg_type

	@GObject.Property(flags=GObject.ParamFlags.READABLE)
	def data(self):
		"""Message data."""
		return self.message.data

@Gtk.Template(resource_path='/org/dithernet/lapel/ui/messageview.ui')
class MessageView(Gtk.ListBoxRow):
	"""
	GTK widget for displaying the data of a message contained in a
	LapelMessage object.
	"""
	__gtype_name__ = 'MessageView'

	utterance_label = Gtk.Template.Child()

	def __init__(self, message=None):
		"""
		Creates an empty MessageView. You can bind it to a LapelMessage
		with the MessageView.bind_to_message function.
		"""
		super().__init__()
		if message:
			self.bind_to_message(message)

	def bind_to_message(self, message):
		"""Binds the MessageView to a message."""
		self.message = message
		if message.type == 'recognizer_loop:utterance':
			self.is_sent()
			self.utterance_label.set_label(' '.join(message.data['utterances']))
		else:
			self.add_css_class('recieved')
			self.utterance_label.set_label(message.data['utterance'])

	def is_sent(self):
		"""
		Actions to perform when the message recieved contains information
		about a sent message.
		"""
		self.add_css_class('sent')
		self.set_halign(Gtk.Align.END)
		self.utterance_label.set_halign(Gtk.Align.END)
