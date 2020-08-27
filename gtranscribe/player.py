# gTranscribe is a software focused on easy transcription of spoken words.
# Copyright (C) 2013-2014 Philip Rinn <rinni@inventati.org>
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

#pylint: disable=wrong-import-position
import logging
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject
logger = logging.getLogger('player')
Gst.init(None)


class gTranscribePlayer(Gst.Bin):
    """Class to play audio files with Gstreamer."""

    __gtype_name__ = 'gTranscribePlayer'

    __gsignals__ = {
        'ready': (GObject.SignalFlags.RUN_LAST, None, (GObject.TYPE_STRING,)),
        'ended': (GObject.SignalFlags.RUN_LAST, None, ())
    }

    def __init__(self):
        super(gTranscribePlayer, self).__init__()

        self._rate = 1
        self._duration = None
        self.init_pipeline()

    def init_pipeline(self):
        """Initialize the audio pipeline."""
        self.pipeline = Gst.Pipeline()
        self.audiosrc = Gst.ElementFactory.make('filesrc', None)
        decoder = Gst.ElementFactory.make('decodebin', None)
        convert1 = Gst.ElementFactory.make('audioconvert', None)
        resample1 = Gst.ElementFactory.make('audioresample', None)
        self.volume1 = Gst.ElementFactory.make('volume', None)
        self.volume1.set_property('volume', 1)
        scaletempo = Gst.ElementFactory.make('scaletempo', None)
        convert2 = Gst.ElementFactory.make('audioconvert', None)
        resample2 = Gst.ElementFactory.make('audioresample', None)
        sink = Gst.ElementFactory.make('autoaudiosink', None)

        decoder.connect('pad-added', self.on_new_decoded_pad)

        self.pipeline.add(self.audiosrc)
        self.pipeline.add(decoder)
        self.pipeline.add(convert1)
        self.pipeline.add(self.volume1)
        self.pipeline.add(resample1)
        self.pipeline.add(scaletempo)
        self.pipeline.add(convert2)
        self.pipeline.add(resample2)
        self.pipeline.add(sink)

        self.audiosrc.link(decoder)
        convert1.link(resample1)
        resample1.link(self.volume1)
        self.volume1.link(scaletempo)
        scaletempo.link(convert2)
        convert2.link(resample2)
        resample2.link(sink)

        self.apad = convert1.get_static_pad('sink')

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.on_message)

    @property
    def filename(self):
        """Return the filename of the current stream."""
        return self.audiosrc.get_property('location')

    @property
    def duration(self):
        """Return the duration of the current stream."""
        success = False
        if self._duration is None:
            success, self._duration = self.pipeline.query_duration(Gst.Format.TIME)
            logger.debug('Query was successful: %s, Duration is: "%s"', success, self._duration)
        return self._duration if success else 0

    def _get_position(self):
        """Return the position of the current stream."""
        # Sometimes querying the position does not work on the first try
        pos = [0]
        while pos[0] == 0:
            pos = self.pipeline.query_position(Gst.Format.TIME)
        return pos[1]

    def _set_position(self, position):
        """Set the position of the current stream."""
        self.pipeline.seek(self._rate,
                           Gst.Format.TIME,
                           Gst.SeekFlags.FLUSH | Gst.SeekFlags.ACCURATE,
                           Gst.SeekType.SET, position,
                           Gst.SeekType.NONE, -1)

    position = property(_get_position, _set_position)

    @property
    def playing(self):
        """Return if pipeline is currently playing."""
        return Gst.State.PLAYING == self.state

    def _get_rate(self):
        """Get the playback speed of the current stream."""
        return self._rate

    def _set_rate(self, rate):
        """Set the playback speed of the current stream."""
        self._rate = rate
        seek_type = Gst.SeekType.SET
        pos = self.pipeline.query_position(Gst.Format.TIME)
        # Position query was not successful
        if pos[0] == 0:
            seek_type = Gst.SeekType.NONE
        self.pipeline.seek(rate,
                           Gst.Format.TIME,
                           Gst.SeekFlags.FLUSH | Gst.SeekFlags.ACCURATE,
                           seek_type, pos[1],
                           Gst.SeekType.NONE, -1)

    rate = property(_get_rate, _set_rate)

    def _get_state(self):
        """Get the state of the audio pipeline."""
        return self.pipeline.get_state(0)[1]

    def _set_state(self, state):
        """Set the state of the audio pipeline."""
        if not state == self.state:
            self.pipeline.set_state(state)

    state = property(_get_state, _set_state)

    def _get_volume(self):
        """Get the volume of the current stream."""
        return self.volume1.get_property('volume')

    def _set_volume(self, volume):
        """Set the volume of the current stream."""
        self.volume1.set_property('volume', volume)

    volume = property(_get_volume, _set_volume)

    # pylint: disable=unused-argument
    def on_new_decoded_pad(self, element, pad):
        """
        Handle new decoded pad from decodebin.

        decodebin creates a new pad after decoding the stream, so we
        have to wait with linking until decodebin has the new pad.
        """
        caps = pad.query_caps(None).to_string()
        if caps.startswith('audio/'):
            if not self.apad.is_linked():
                pad.link(self.apad)
            self.emit('ready', self.filename)

    # pylint: disable=unused-argument
    def on_message(self, bus, message):
        """Handle message and react accordingly."""
        if message.type == Gst.MessageType.EOS:
            self.state = Gst.State.NULL
            self.emit('ended')
        elif message.type == Gst.MessageType.ERROR:
            logger.debug("%s", print(message.parse_error()))
            self.state = Gst.State.NULL

    def open(self, filepath, duration=True):
        """Open audio file and optionally query duration."""
        logger.debug('Opening file "%s"', filepath)
        self.state = Gst.State.READY
        self.audiosrc.set_property('location', filepath)
        if duration:
            self._duration = None
        # Force decoding of file so we have a duration
        self.state = Gst.State.PLAYING
        self.state = Gst.State.PAUSED

    def reset(self):
        """Reset the pipeline."""
        logger.debug('Reset the pipeline')
        self.state = Gst.State.NULL
        filename = self.filename
        self.init_pipeline()
        self.open(filename, False)

    def play(self):
        """Start playback from current position."""
        self.state = Gst.State.PLAYING

    def pause(self):
        """Pause playback."""
        self.state = Gst.State.PAUSED

    def move_position(self, amount):
        """Move playback position."""
        new_position = self.position + amount
        # Clamp new_position between 0 and self.duration
        self.position = max(min(new_position, self.duration), 0)
