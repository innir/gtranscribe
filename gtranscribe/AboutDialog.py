# gTranscribe is a software focussed on easy transcription of spoken words.
# Copyright (C) 2013-2016 Philip Rinn <rinni@inventati.org>
# Copyright (C) 2010 Frederik Elwert <frederik.elwert@web.de>
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

import gettext
from gettext import gettext as _
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gettext.textdomain('gTranscribe')


class AboutDialog:

    def __init__(self, trans):
        authors = ["Philip Rinn <rinni@inventati.org>"]
        self.about_dialog = Gtk.AboutDialog()
        self.about_dialog.set_transient_for(trans.window)
        self.about_dialog.set_destroy_with_parent(True)
        self.about_dialog.set_name("gTranscribe")
        self.about_dialog.set_version("0.4")
        self.about_dialog.set_copyright("Copyright \xc2\xa9 2013-2016 Philip Rinn\nCopyright \xc2\xa9 2010 Frederik Elwert")
        self.about_dialog.set_comments(_("gTranscribe is a software focussed on easy transcription of spoken words."))
        self.about_dialog.set_website("https://github.com/innir/gtranscribe")
        self.about_dialog.set_authors(authors)
        self.about_dialog.set_license("This program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License version 3 as\npublished by the Free Software Foundation.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see http://www.gnu.org/licenses/.")

        icon_theme = Gtk.IconTheme.get_default()
        if icon_theme.has_icon('gtranscribe'):
            icon = icon_theme.load_icon('gtranscribe', 128, 0)
            self.about_dialog.set_logo(icon)

        self.about_dialog.connect("response", self._close, trans)
        self.about_dialog.connect("delete-event", self._delete_event, trans)

    def show(self):
        return self.about_dialog.show()

    # callbacks for destroying the dialog
    def _close(self, dialog, response, trans):
        trans.about_dialog = None
        dialog.destroy()

    def _delete_event(self, dialog, event, trans):
        trans.about_dialog = None
        return True
