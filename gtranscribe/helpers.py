# gTranscribe is a software focussed on easy transcription of spoken words.
# Copyright (C) 2010 Frederik Elwert <frederik.elwert@web.de>
# Copyright (C) 2013-2014 Philip Rinn <rinni@inventati.org>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as 
# published by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import datetime
from gi.repository import Gtk, Gio
import hashlib
import gettext
from gettext import gettext as _
gettext.textdomain('gTranscribe')

# Where your project will look for your data (for instance, images and ui
# files). By default, this is ../data, relative your trunk layout
__gtranscribe_data_directory__ = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/'))
# if this path does not exist fall back to system wide directory
if not os.path.exists(__gtranscribe_data_directory__):
    __gtranscribe_data_directory__ = sys.exec_prefix + '/share/gTranscribe/'

def get_data_file(*path_segments):
    return os.path.join(__gtranscribe_data_directory__, *path_segments)


def trim(timestring, digits=1):
    """
    Trim a time string to contain only a given number of digits
    
    """
    pos = timestring.find('.')
    if pos > -1:
        return timestring[:pos+1+digits]
    else:
        return timestring

def ns_to_time(ns):
    """
    Converts nanoseconds to a datetime.time object.
    
    :Parameters:
        - `ns`: Nanoseconds as int.
    
    :Return:
        - A datetime.time object.
        
    """
    h = ns / (60 * 60 * 1000000000)
    mod = ns % (60 * 60 * 1000000000)
    m = mod / (60 * 1000000000)
    mod = mod % (60 * 1000000000)
    s = mod / 1000000000
    mod = mod % 1000000000
    ms = mod / 1000
    return datetime.time(h, m, s, ms)
    
def time_to_ns(time):
    """
    Converts a datetime.time object to nanoseconds.
    
    :Parameters:
        - `time`: A datetime.time object.
    
    :Return:
        - Nanoseconds as int.
        
    """
    values = []
    values.append(time.hour * 60 * 60 * 1000000000)
    values.append(time.minute * 60 * 1000000000)
    values.append(time.second * 1000000000)
    values.append(time.microsecond * 1000)
    return sum(values)
    
def filepath_to_uri(path):
    file = Gio.File.new_for_path(path)
    return file.get_uri()

def uri_to_filepath(uri):
    file = Gio.File.new_for_uri(uri)
    return file.get_path()

def get_open_filename(self):
    filename = None
    chooser = Gtk.FileChooserDialog(_("Open File..."), self.window,
                                    Gtk.FileChooserAction.OPEN,
                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                     Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    filter = Gtk.FileFilter()
    filter.set_name(_('Plain Text Files'))
    filter.add_mime_type('text/plain')
    chooser.add_filter(filter)
    chooser.set_filter(filter)

    response = chooser.run()
    if response == Gtk.ResponseType.OK: filename = chooser.get_filename()
    chooser.destroy()
    return filename

def get_save_filename(self):
    filename = None
    chooser = Gtk.FileChooserDialog(_("Save File..."), self.window,
                                    Gtk.FileChooserAction.SAVE,
                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                     Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
    response = chooser.run()
    if response == Gtk.ResponseType.OK: filename = chooser.get_filename()
    chooser.destroy()
    return filename

def error_message(self, message):
    dialog = Gtk.MessageDialog(None,
                               Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                               Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, message)
    dialog.run()
    dialog.destroy()

def md5_of_file(fname):
    md5 = hashlib.md5()
    f = open(fname, 'r')
    while True:
        data = f.read(81920)
        if not data:
            break
        md5.update(data)
    f.close()
    return md5.hexdigest()

