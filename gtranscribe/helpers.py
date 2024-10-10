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
import datetime
import gettext
from gettext import gettext as _
from typing import Any
from collections.abc import Callable
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio
gettext.textdomain('gTranscribe')

# pylint: disable=invalid-name
class duration:
    """
    Stores a time duration in hours, minutes, seconds and microseconds.

    Implements only a fraction of datetime.time but allows hour >= 24.
    """

    __slots__ = '_hour', '_minute', '_second', '_microsecond'

    def __new__(cls, hour: int = 0, minute: int = 0, second: int = 0, microsecond: int = 0) -> 'duration':
        """Constructor.
        Arguments:
        hour, minute, second, microsecond (default to zero)
        """
        self = object.__new__(cls)
        self._hour = hour  # type: ignore[attr-defined]
        self._minute = minute  # type: ignore[attr-defined]
        self._second = second  # type: ignore[attr-defined]
        self._microsecond = microsecond  # type: ignore[attr-defined]
        return self

    @property
    def hour(self) -> int:
        """hour"""
        return self._hour  # type: ignore[attr-defined,no-any-return]

    @property
    def minute(self) -> int:
        """minute (0-59)"""
        return self._minute  # type: ignore[attr-defined,no-any-return]

    @property
    def second(self) -> int:
        """second (0-59)"""
        return self._second  # type: ignore[attr-defined,no-any-return]

    @property
    def microsecond(self) -> int:
        """microsecond (0-999999)"""
        return self._microsecond  # type: ignore[attr-defined,no-any-return]

    def strftime(self, fmt_string: str) -> str:
        """
        Probably not what you think it is :-(.
        It just implements what's needed for gTranscribe.
        """
        txt = fmt_string.replace("%H", str(self._hour))  # type: ignore[attr-defined]
        txt = txt.replace("%M", str(self._minute))  # type: ignore[attr-defined]
        txt = txt.replace("%S", str(self._second))  # type: ignore[attr-defined]
        txt = txt.replace("%f", str(self._microsecond))  # type: ignore[attr-defined]
        return txt


def trim(timestring: str, digits: int = 1) -> str:
    """Trim a time string to contain only a given number of digits."""
    match = re.search("[.-]", timestring)
    if match:
        pos = match.start()
        if pos > -1:
            return timestring[:pos + 1 + digits]
    return timestring

def ns_to_time(ns: int) -> duration:
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


def time_to_ns(time: duration | datetime.time) -> int:
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


def get_open_filename(self: Any, title: str, filter_name: str, filter_mime: str, callback: Callable[[Gtk.FileDialog, Gio.AsyncResult], None]) -> None:
    """Display a file open dialog."""
    chooser = Gtk.FileDialog.new()
    chooser.set_title(title)

    file_filter = Gtk.FileFilter()
    file_filter.set_name(filter_name)
    file_filter.add_mime_type(filter_mime)
    filters = Gio.ListStore.new(Gtk.FileFilter)
    filters.append(file_filter)
    chooser.set_filters(filters)
    chooser.open(self.window, None, callback)


def get_save_filename(self: Any) -> None:
    """Display a file save dialog."""
    chooser = Gtk.FileDialog.new()
    chooser.set_title(_("Save Text File"))
    chooser.save(self.window, None, self.save_dialog_callback)


def error_message(self: Any, message: str) -> None:
    """Display the string 'message' in an error dialog."""
    dialog = Gtk.AlertDialog.new(message)
    dialog.show(self.window)


def md5_of_file(fname: str) -> str:
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


def get_data_file(root_dir: str, *path_segments: str) -> str:
    """Return the absolute path of the given data file."""
    # Where to look for data (ui and image files). By default,
    # this is ../data, relative your trunk layout
    data_directory = os.path.join(root_dir, 'data/')

    # If this path does not exist fall back to system wide directory
    if not os.path.exists(data_directory):
        data_directory = os.path.join(root_dir, 'share/gTranscribe/')

    return os.path.join(data_directory, *path_segments)
