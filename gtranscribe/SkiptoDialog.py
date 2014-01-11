# gTranscribe is a software focussed on easy transcription of spoken words.
# Copyright (C) 2010 Frederik Elwert <frederik.elwert@web.de>
# Copyright (C) 2013 Philip Rinn <rinni@gmx.net>
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

import ctypes
import datetime
from gi.repository import Gtk
import gettext
from gettext import gettext as _
gettext.textdomain('gTranscribe')

from gtranscribe.helpers import ns_to_time, time_to_ns, trim

class SkiptoDialog:

    def __init__(self):
        self.time_format = '%M:%S.%f'
        label = Gtk.Label(label=_("Skip to:"))
        box = Gtk.HBox()
        self.skipDialog = Gtk.Dialog(_("Skip to ..."),
                           None,
                           Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                           (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                            Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.skipDialog.vbox.pack_start(box, True, True, 0)
        box.pack_start(label, True, True, 0)
        self.spinbutton = Gtk.SpinButton()
        self.spinbutton.connect("input",self.on_spinbutton_time_input)
        self.spinbutton.connect("output",self.on_spinbutton_time_output)
        box.pack_end(self.spinbutton, True, True, 0)
        self.spinbutton.show()
        label.show()
        box.show()
        
    def on_spinbutton_time_input(self, spinbutton, value_ptr):
        text = spinbutton.get_text()
        try:
            time = datetime.datetime.strptime(text, self.time_format).time()
        except ValueError:
            return -1
        double = ctypes.c_double.from_address(hash(value_ptr))
        double.value = float(time_to_ns(time))
        return True
        
    def on_spinbutton_time_output(self, spinbutton):
        time = ns_to_time(int(spinbutton.get_value()))
        text = trim(time.strftime(self.time_format))
        spinbutton.set_text(text)
        return True

    def run(self):
        return self.skipDialog.run()

    def destroy(self):
        self.skipDialog.destroy()

