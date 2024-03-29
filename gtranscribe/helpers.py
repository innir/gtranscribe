# gTranscribe is a software focused on easy transcription of spoken words.
# Copyright (C) 2013-2021 Philip Rinn <rinni@inventati.org>
# Copyright (C) 2010 Frederik Elwert <frederik.elwert@web.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# pylint: disable=wrong-import-position
import os.path
from hashlib import md5
import re
import gettext
from gettext import gettext as _
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gettext.textdomain('gTranscribe')

# pylint: disable=invalid-name
class duration:
    """
    Stores a time duration in hours, minutes, seconds and microseconds.

    Implements only a fraction of datetime.time but allows hour >= 24.
    """

    __slots__ = '_hour', '_minute', '_second', '_microsecond'

    def __new__(cls, hour=0, minute=0, second=0, microsecond=0):
        """Constructor.
        Arguments:
        hour, minute, second, microsecond (default to zero)
        """
        self = object.__new__(cls)
        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        return self

    @property
    def hour(self):
        """hour"""
        return self._hour

    @property
    def minute(self):
        """minute (0-59)"""
        return self._minute

    @property
    def second(self):
        """second (0-59)"""
        return self._second

    @property
    def microsecond(self):
        """microsecond (0-999999)"""
        return self._microsecond

    def strftime(self, fmt_string):
        """
        Probably not what you think it is :-(.
        It just implements what's needed for gTranscribe.
        """
        txt = fmt_string.replace("%H", str(self._hour))
        txt = txt.replace("%M", str(self._minute))
        txt = txt.replace("%S", str(self._second))
        txt = txt.replace("%f", str(self._microsecond))
        return txt


def trim(timestring, digits=1):
    """Trim a time string to contain only a given number of digits."""
    pos = re.search("[.-]", timestring).start()
    if pos > -1:
        return timestring[:pos + 1 + digits]
    return timestring

def ns_to_time(ns):
    """
    Convert nanoseconds to a duration object.

    :Parameters:
        - 'ns': Nanoseconds as int.

    :Return:
        - A datetime.time object.
    """
    h = ns // (60 * 60 * 1000000000)
    mod = ns % (60 * 60 * 1000000000)
    m = mod // (60 * 1000000000)
    mod = mod % (60 * 1000000000)
    s = mod // 1000000000
    mod = mod % 1000000000
    ms = mod // 1000
    return duration(h, m, s, ms)


def time_to_ns(time):
    """
    Convert a datetime.time or duration object to nanoseconds.

    :Parameters:
        - 'time': A datetime.time or duration object.

    :Return:
        - Nanoseconds as int.
    """
    values = []
    values.append(time.hour * 60 * 60 * 1000000000)
    values.append(time.minute * 60 * 1000000000)
    values.append(time.second * 1000000000)
    values.append(time.microsecond * 1000)
    return sum(values)


def get_open_filename(self, title, filter_name, filter_mime):
    """Display a file open dialog and returns the filename."""
    filename = None
    chooser = Gtk.FileChooserDialog(title, self.window,
                                    Gtk.FileChooserAction.OPEN,
                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                     Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    file_filter = Gtk.FileFilter()
    file_filter.set_name(filter_name)
    file_filter.add_mime_type(filter_mime)
    chooser.add_filter(file_filter)
    chooser.set_filter(file_filter)

    response = chooser.run()
    if response == Gtk.ResponseType.OK:
        filename = chooser.get_filename()
    chooser.destroy()
    return filename


def get_save_filename(self):
    """Display a file save dialog and returns the filename."""
    filename = None
    chooser = Gtk.FileChooserDialog(_("Save Text File"), self.window,
                                    Gtk.FileChooserAction.SAVE,
                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                     Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
    chooser.set_do_overwrite_confirmation(True)
    response = chooser.run()
    if response == Gtk.ResponseType.OK:
        filename = chooser.get_filename()
    chooser.destroy()
    return filename


def error_message(self, message):
    """Display the string 'message' in an error dialog."""
    dialog = Gtk.MessageDialog(self.window,
                               Gtk.DialogFlags.MODAL |
                               Gtk.DialogFlags.DESTROY_WITH_PARENT,
                               Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,
                               message)
    dialog.run()
    dialog.destroy()


def md5_of_file(fname):
    """
    Calculate the md5 hash of the given file.

    :Parameters:
        - 'fname': filename.

    :Return:
        - A string of length 32, containing the md5 hash as hexadecimal digits.
    """
    md5_hash = md5()
    with open(fname, "rb") as data:
        for chunk in iter(lambda: data.read(81920), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def get_data_file(root_dir, *path_segments):
    """Return the absolute path of the given data file."""
    # Where to look for data (ui and image files). By default,
    # this is ../data, relative your trunk layout
    data_directory = os.path.join(root_dir, 'data/')

    # If this path does not exist fall back to system wide directory
    if not os.path.exists(data_directory):
        data_directory = os.path.join(root_dir, 'share/gTranscribe/')

    return os.path.join(data_directory, *path_segments)
