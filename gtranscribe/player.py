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
logger = logging.getLogger('player')
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject
Gst.init(None)

QueryError = Gst.QueryError # for imports in GUI


class gTranscribePlayer(GObject.GObject):

    __gtype_name__ = 'gTranscribePlayer'

    __gsignals__ = {
        'ready': (GObject.SignalFlags.RUN_LAST, None,
                  (GObject.TYPE_STRING,)),
        'ended': (GObject.SignalFlags.RUN_LAST, None,
                  ())
    }

    def __init__(self):
        GObject.GObject.__init__(self)

        self._rate = 1
        self._duration = None

        self.pipeline = Gst.Pipeline()
        self.audiosrc = Gst.ElementFactory.make('filesrc', 'audio')
        self.decoder = Gst.ElementFactory.make('decodebin', 'decoder')
        self.convert1 = Gst.ElementFactory.make('audioconvert', 'convert1')
        self.resample1 = Gst.ElementFactory.make('audioresample', 'resample1')
        self.volume1 = Gst.ElementFactory.make('volume', 'volume')
        self.volume1.set_property('volume', 1)
        self.scaletempo = Gst.ElementFactory.make('scaletempo', 'scaletempo')
        self.convert2 = Gst.ElementFactory.make('audioconvert', 'convert2')
        self.resample2 = Gst.ElementFactory.make('audioresample', 'resample2')
        self.sink = Gst.ElementFactory.make('autoaudiosink', 'sink')

        self.decoder.connect('new-decoded-pad', self.on_new_decoded_pad)

        self.pipeline.add(self.audiosrc)
        self.pipeline.add(self.decoder)
        self.pipeline.add(self.convert1)
        self.pipeline.add(self.volume1)
        self.pipeline.add(self.resample1)
        self.pipeline.add(self.scaletempo)
        self.pipeline.add(self.convert2)
        self.pipeline.add(self.resample2)
        self.pipeline.add(self.sink)
        self.audiosrc.link(self.decoder)
        
        self.convert1.link(self.resample1)
        self.resample1.link(self.volume1)
        self.volume1.link1(self.scaletempo)
        self.scaletempo.link(self.convert2)
        self.convert2.link(self.resample2)
        self.resample2.link(self.sink)

        self.apad = self.convert1.get_static_pad('sink')

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.on_message)

    @property
    def filename(self):
        return self.audiosrc.get_property('location')

    @property
    def duration(self):
        """Return the duration of the current stream."""
        if self._duration == None:
            self._duration = self.pipeline.query_duration(Gst.Format.TIME, None)[0]
        return self._duration

    def _get_position(self):
        """Return the position of the current stream."""
        pos = self.pipeline.query_position(Gst.Format.TIME, None)[0]
        return pos

    def _set_position(self, position):
        self.pipeline.seek(self._rate,
                           Gst.Format.TIME,
                           Gst.SeekFlags.FLUSH | Gst.SeekFlags.ACCURATE,
                           Gst.SeekType.SET, position,
                           Gst.SeekType.NONE, -1)

    position = property(_get_position, _set_position)

    @property
    def playing(self):
        """Return if pipeline is currently playing."""
        return Gst.State.PLAYING in self.pipeline.get_state()

    def _get_rate(self):
        return self._rate

    def _set_rate(self, rate):
        self._rate = rate
        seek_type = Gst.SeekType.SET
        try:
            pos = self.pipeline.query_position(Gst.Format.TIME, None)[0]
        except:
            seek_type = Gst.SeekType.NONE
            pos = -1
        self.pipeline.seek(rate,
                           Gst.Format.TIME,
                           Gst.SeekFlags.FLUSH | Gst.SeekFlags.ACCURATE,
                           seek_type, pos,
                           Gst.SeekType.NONE, -1)

    rate = property(_get_rate, _set_rate)

    def _get_state(self):
        return self.pipeline.get_state()[1]

    def _set_state(self, state):
        if not state == self.state:
            self.pipeline.set_state(state)

    state = property(_get_state, _set_state)

    def _get_volume(self):
        return self.volume1.get_property('volume')

    def _set_volume(self, volume):
        self.volume1.set_property('volume', volume)

    volume = property(_get_volume, _set_volume)

    def on_new_decoded_pad(self, element, pad, last):
        """
        Handle new decoded pad from decodebin.
        
        decodebin creates a new pad after decoding the stream, so we
        have to wait with linking until decodebin has the new pad.
        
        """
        caps = pad.get_caps()
        name = caps[0].get_name()
        if name in ('audio/x-raw-float', 'audio/x-raw-int'):
            if not self.apad.is_linked():
                pad.link(self.apad)
            self.emit('ready', self.audiosrc.get_property('location'))

    def on_message(self, bus, message):
        if message.type == Gst.MessageType.EOS:
            self.pipeline.set_state(Gst.State.NULL)
            self.emit('ended')

    def open(self, filepath):
        logger.debug('Opening file "%s"' % filepath)
        self.pipeline.set_state(Gst.State.NULL)
        self.audiosrc.set_property('location', filepath)
        # Force decoding of file so we have a duration
        self.pipeline.set_state(Gst.State.PLAYING)
        self.pipeline.set_state(Gst.State.PAUSED)
        self._duration = None

    def play(self):
        """Start playback from current position."""
        self.pipeline.set_state(Gst.State.PLAYING)
        
    def pause(self):
        """Pause playback."""
        self.pipeline.set_state(Gst.State.PAUSED)

