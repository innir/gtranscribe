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

import sqlite3
import gi
from gi.repository import GLib
import os.path
import logging
logger = logging.getLogger('fileinfo')

database = os.path.join(GLib.get_user_cache_dir(), "gTranscribe",
                        "metadata.db")


class FileInfo (object):
    """
    Query and store information about a given file.

    This class abstracts several metadata storage systems in favor of a simple
    interface.
    """

    def __init__(self, filepath, md5):
        self.filepath = filepath
        self.md5 = md5
        self._cache = {}

    def _get_data(self, attribute):
        """
        A generic method to hide the verbose process of getting attributes.
        """
        # Use cached values if available to limit requests
        if attribute in self._cache:
            return self._cache[attribute]
        con = sqlite3.connect(database)
        cur = con.cursor()
        query = 'SELECT ' + attribute + ' FROM metadata WHERE md5=?'
        cur.execute(query, (self.md5,))
        value = cur.fetchone()[0]
        cur.close()
        con.close()
        self._cache[attribute] = value
        logger.debug('Get attribute "%s": %s' % (attribute, value))
        return value

    def _set_data(self, attribute, value):
        """
        A generic method to hide the verbose process of setting attributes.
        """
        logger.debug('Set attribute "%s": %s' % (attribute, value))
        query = 'UPDATE metadata SET ' + attribute + '=? WHERE md5=?'
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute(query, (value, self.md5))
        con.commit()
        cur.close()
        con.close()
        self._cache[attribute] = value

    def _get_position(self):
        position = self._get_data("position")
        if not isinstance(position, int):
            position = 0
        return position

    def _set_position(self, position):
        self._set_data("position", position)
        return True

    def _get_speed(self):
        speed = self._get_data("speed")
        if not isinstance(speed, float):
            speed = 1.0
        return speed

    def _set_speed(self, speed):
        self._set_data("speed", speed)
        return True

    position = property(_get_position, _set_position)
    speed = property(_get_speed, _set_speed)
