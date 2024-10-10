# gTranscribe is a software focused on easy transcription of spoken words.
# Copyright (C) 2013-2025 Philip Rinn <rinni@inventati.org>
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

"""MPRIS D-Bus interface for media key support."""

import logging
from typing import Any, Dict
import dbus
import dbus.service

logger = logging.getLogger('mpris')


class MPRISInterface(dbus.service.Object):
    """MPRIS D-Bus interface for media key support."""
    
    MPRIS_IFACE = 'org.mpris.MediaPlayer2'
    MPRIS_PLAYER_IFACE = 'org.mpris.MediaPlayer2.Player'
    
    def __init__(self, bus_name: dbus.service.BusName, app: Any) -> None:
        dbus.service.Object.__init__(self, bus_name, '/org/mpris/MediaPlayer2')
        self.app = app
    
    @dbus.service.method(MPRIS_PLAYER_IFACE)
    def Play(self) -> None:
        """Handle Play command from media keys."""
        logger.debug('MPRIS: Play')
        if self.app.slider.is_sensitive():
            self.app.play_action.set_active(True)
    
    @dbus.service.method(MPRIS_PLAYER_IFACE)
    def Pause(self) -> None:
        """Handle Pause command from media keys."""
        logger.debug('MPRIS: Pause')
        self.app.play_action.set_active(False)
    
    @dbus.service.method(MPRIS_PLAYER_IFACE)
    def PlayPause(self) -> None:
        """Handle PlayPause command from media keys."""
        logger.debug('MPRIS: PlayPause')
        if self.app.slider.is_sensitive():
            self.app.play_action.set_active(not self.app.play_action.get_active())
    
    @dbus.service.method(MPRIS_PLAYER_IFACE)
    def Stop(self) -> None:
        """Handle Stop command from media keys."""
        logger.debug('MPRIS: Stop')
        self.app.play_action.set_active(False)
    
    @dbus.service.method(MPRIS_PLAYER_IFACE)
    def Next(self) -> None:
        """Handle Next command from media keys."""
        logger.debug('MPRIS: Next')
        if self.app.forward_button.is_sensitive():
            self.app.forward(None)
    
    @dbus.service.method(MPRIS_PLAYER_IFACE)
    def Previous(self) -> None:
        """Handle Previous command from media keys."""
        logger.debug('MPRIS: Previous')
        if self.app.rewind_button.is_sensitive():
            self.app.rewind(None)
    
    @dbus.service.method(MPRIS_IFACE)
    def Raise(self) -> None:
        """Raise the application window."""
        logger.debug('MPRIS: Raise')
        self.app.window.present()
    
    @dbus.service.method(MPRIS_IFACE)
    def Quit(self) -> None:
        """Quit the application."""
        logger.debug('MPRIS: Quit')
        self.app.quit()
    
    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='ss', out_signature='v')
    def Get(self, interface: str, prop: str) -> Any:
        """Get property."""
        return self.GetAll(interface)[prop]
    
    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface: str) -> Dict[str, Any]:
        """Get all properties."""
        if interface == self.MPRIS_IFACE:
            return {
                'CanQuit': True,
                'CanRaise': True,
                'HasTrackList': False,
                'Identity': 'gTranscribe',
                'DesktopEntry': 'org.innir.gtranscribe',
            }
        elif interface == self.MPRIS_PLAYER_IFACE:
            return {
                'CanControl': True,
                'CanPlay': self.app.slider.is_sensitive(),
                'CanPause': self.app.slider.is_sensitive(),
                'CanSeek': self.app.slider.is_sensitive(),
                'CanGoNext': self.app.forward_button.is_sensitive(),
                'CanGoPrevious': self.app.rewind_button.is_sensitive(),
                'PlaybackStatus': 'Playing' if self.app.play_action.get_active() else 'Paused',
            }
        return {}
    
    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='ssv')
    def Set(self, interface: str, prop: str, value: Any) -> None:
        """Set property (not implemented)."""
        pass
