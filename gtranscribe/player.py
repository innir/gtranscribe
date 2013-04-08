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

import time
import datetime
import logging
logger = logging.getLogger('player')

import pygst
pygst.require('0.10')
import gst
import gobject

QueryError = gst.QueryError # for imports in GUI


class gTranscribePlayer(gobject.GObject):

    __gtype_name__ = 'gTranscribePlayer'

    __gsignals__ = {
        'ready': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, 
                  (gobject.TYPE_STRING,)),
        'ended': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                  ())
    }

    def __init__(self):
        gobject.GObject.__init__(self)
        
        self._rate = 1
        
        self.pipeline = gst.Pipeline('pipeline_main')
        self.audiosrc = gst.element_factory_make('filesrc', 'audio')
        self.decoder = gst.element_factory_make('decodebin', 'decoder')
        self.convert1 = gst.element_factory_make('audioconvert', 'convert1')
        self.resample1 = gst.element_factory_make('audioresample', 'resample1')
        self.volume1 = gst.element_factory_make('volume', 'volume')
        self.volume1.set_property('volume', 1)
        self.scaletempo = gst.element_factory_make('scaletempo',
                                                   'scaletempo')
        self.convert2 = gst.element_factory_make('audioconvert', 'convert2')
        self.resample2 = gst.element_factory_make('audioresample', 'resample2')
        self.sink = gst.element_factory_make('autoaudiosink', 'sink')
        
        self.decoder.connect('new-decoded-pad', self.on_new_decoded_pad)
        
        self.pipeline.add(self.audiosrc, self.decoder, self.convert1,
                self.volume1, self.resample1, self.scaletempo, self.convert2,
                self.resample2, self.sink)
        self.audiosrc.link(self.decoder)
        gst.element_link_many(self.convert1, self.resample1, self.volume1, 
                self.scaletempo, self.convert2, self.resample2, self.sink)
        
        self.apad = self.convert1.get_pad('sink')
        
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.on_message)
        
    @property
    def filename(self):
        return self.audiosrc.get_property('location')
        
    @property
    def duration(self):
        """Return the duration of the current stream."""
        dur = self.pipeline.query_duration(gst.FORMAT_TIME, None)[0]
        return dur
        
    def _get_position(self):
        """Return the position of the current stream."""
        pos = self.pipeline.query_position(gst.FORMAT_TIME, None)[0]
        # TODO: Handle QueryError
        return pos
        
    def _set_position(self, position):
        self.pipeline.seek(self._rate,
                           gst.FORMAT_TIME,
                           gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE,
                           gst.SEEK_TYPE_SET, position,
                           gst.SEEK_TYPE_NONE, -1)
        
    position = property(_get_position, _set_position)
        
    @property
    def playing(self):
        """Return if pipeline is currently playing."""
        return gst.STATE_PLAYING in self.pipeline.get_state()
        
    def _get_rate(self):
        return self._rate
    
    def _set_rate(self, rate):
        self._rate = rate
        seek_type = gst.SEEK_TYPE_SET
        try:
            pos = self.pipeline.query_position(gst.FORMAT_TIME, None)[0]
        except gst.QueryError:
            seek_type = gst.SEEK_TYPE_NONE
            pos = -1
        self.pipeline.seek(rate,
                           gst.FORMAT_TIME,
                           gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE,
                           seek_type, pos,
                           gst.SEEK_TYPE_NONE, -1)
    
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
        if message.type == gst.MESSAGE_EOS:
            self.pipeline.set_state(gst.STATE_NULL)
            self.emit('ended')
                
    def open(self, filepath):
        logger.debug('Opening file "%s"' % filepath)
        self.pipeline.set_state(gst.STATE_NULL)
        self.audiosrc.set_property('location', filepath)
        # Force decoding of file so we have a duration
        self.pipeline.set_state(gst.STATE_PLAYING)
        self.pipeline.set_state(gst.STATE_PAUSED)
                
    def play(self):
        """
        Start playback from current position.
        
        """
        self.pipeline.set_state(gst.STATE_PLAYING)
        
    def pause(self):
        """
        Pause playback.
        
        """
        self.pipeline.set_state(gst.STATE_PAUSED)

