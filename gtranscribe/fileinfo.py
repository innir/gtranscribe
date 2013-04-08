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

import logging
logger = logging.getLogger('fileinfo')
import gio

POSITION_ATTRIBUTE = "metadata::totem::position"
SPEED_ATTRIBUTE = "metadata::gtranscribe::speed"
MSECOND = 1000000


class FileInfo (object):
    """
    Query and store information about a given file.
    
    This class abstracts several metadata storage systems in favor of a simple
    interface.
    
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self._cache = {}
        
    def _get_gio_attribute(self, attribute):
        """
        A generic method to hide the verbose process of getting GIO attributes.
        
        """
        # Use cached values if available to limit requests
        if attribute in self._cache:
            return self._cache[attribute]
        file = gio.File(path=self.filepath)
        info = file.query_info(attribute)
        value = info.get_attribute_as_string(attribute)
        self._cache[attribute] = value
        logger.debug('Get attribute "%s": %s' % (attribute, value))
        return value
        
    def _set_gio_attribute(self, attribute, value):
        """
        A generic method to hide the verbose process of setting GIO attributes.
        
        """
        logger.debug('Set attribute "%s": %s' % (attribute, value))
        file = gio.File(path=self.filepath)
        info = file.query_info(attribute)
        info.set_attribute_string(attribute, str(value))
        file.set_attributes_from_info(info)
        self._cache[attribute] = value
        
    def _get_position(self):
        position = self._get_gio_attribute(POSITION_ATTRIBUTE)
        if position:
            position = int(position) * MSECOND
        return position
    
    def _set_position(self, position):
        self._set_gio_attribute(POSITION_ATTRIBUTE, str(position / MSECOND))
        
    position = property(_get_position, _set_position)
    
    def _get_speed(self):
        speed = self._get_gio_attribute(SPEED_ATTRIBUTE)
        if speed:
            speed = float(speed)
        return speed
        
    def _set_speed(self, speed):
        self._set_gio_attribute(SPEED_ATTRIBUTE, str(speed))
        
    speed = property(_get_speed, _set_speed)

