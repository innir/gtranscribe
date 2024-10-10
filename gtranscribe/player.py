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

# pylint: disable=wrong-import-position
import logging
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject
logger = logging.getLogger('player')
Gst.init(None)

# pylint: disable=invalid-name
class gTranscribePlayer(Gst.Bin):
    """Class to play audio files with Gstreamer."""

    __gtype_name__ = 'gTranscribePlayer'

    __gsignals__ = {
        'ready': (GObject.SignalFlags.RUN_LAST, None, (GObject.TYPE_STRING,)),
        'ended': (GObject.SignalFlags.RUN_LAST, None, ()),
        'duration_changed': (GObject.SignalFlags.RUN_LAST, None, ())
    }

    def __init__(self) -> None:
        super().__init__()

        self._rate: float = 1
        self._duration: int | None = None
        self._message_type: Gst.MessageType = Gst.MessageType.UNKNOWN
        self.init_pipeline()

    def init_pipeline(self) -> None:
        """Initialize the audio pipeline."""
        self.pipeline = Gst.Pipeline()
        self.audiosrc = Gst.ElementFactory.make('filesrc', None)
        decoder = Gst.ElementFactory.make('decodebin', None)
        convert = Gst.ElementFactory.make('audioconvert', None)
        resample = Gst.ElementFactory.make('audioresample', None)
        self.volume_element = Gst.ElementFactory.make('volume', None)
        self.volume_element.set_property('volume', 1)
        scaletempo = Gst.ElementFactory.make('scaletempo', None)
        sink = Gst.ElementFactory.make('autoaudiosink', None)

        decoder.connect('pad-added', self.on_new_decoded_pad)

        self.pipeline.add(self.audiosrc)
        self.pipeline.add(decoder)
        self.pipeline.add(convert)
        self.pipeline.add(resample)
        self.pipeline.add(self.volume_element)
        self.pipeline.add(scaletempo)
        self.pipeline.add(sink)

        self.audiosrc.link(decoder)
        convert.link(resample)
        resample.link(self.volume_element)
        self.volume_element.link(scaletempo)
        scaletempo.link(sink)

        self.apad = convert.get_static_pad('sink')

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.on_message)

    @property
    def filename(self) -> str:
        """Return the filename of the current stream."""
        return str(self.audiosrc.get_property('location'))

    @property
    def duration(self) -> int:
        """Return the duration of the current stream."""
        success = False
        if self._duration is None or self._message_type == Gst.MessageType.DURATION_CHANGED:
            success, self._duration = self.pipeline.query_duration(Gst.Format.TIME)
            if not success:
                self._duration = 0
            logger.debug('Query was successful: %s, Duration is: "%s"',
                         success, self._duration)
        return self._duration

    def _get_position(self) -> int:
        """Return the position of the current stream."""
        # Sometimes querying the position does not work on the first try
        pos = [0]
        while pos[0] == 0:
            pos = self.pipeline.query_position(Gst.Format.TIME)
        return pos[1]

    def _set_position(self, position: int) -> None:
        """Set the position of the current stream."""
        seek_event = Gst.Event.new_seek(
            self._rate,
            Gst.Format.TIME,
            Gst.SeekFlags.FLUSH,
            Gst.SeekType.SET, position,
            Gst.SeekType.NONE, -1
        )
        self.pipeline.send_event(seek_event)

    position = property(_get_position, _set_position)

    @property
    def playing(self) -> bool:
        """Return if pipeline is currently playing."""
        return bool(Gst.State.PLAYING == self.state)

    def _get_rate(self) -> float:
        """Get the playback speed of the current stream."""
        return self._rate

    def _set_rate(self, rate: float) -> None:
        """Set the playback speed of the current stream."""
        self._rate = rate
        pos = self.pipeline.query_position(Gst.Format.TIME)
        # Position query was not successful, use current position or 0
        position = pos[1] if pos[0] else 0
        seek_event = Gst.Event.new_seek(
            rate,
            Gst.Format.TIME,
            Gst.SeekFlags.FLUSH,
            Gst.SeekType.SET, position,
            Gst.SeekType.NONE, -1
        )
        self.pipeline.send_event(seek_event)

    rate = property(_get_rate, _set_rate)

    def _get_state(self) -> Gst.State:
        """Get the state of the audio pipeline."""
        return self.pipeline.get_state(0)[1]

    def _set_state(self, state: Gst.State) -> None:
        """Set the state of the audio pipeline."""
        if not state == self.state:
            self.pipeline.set_state(state)

    state = property(_get_state, _set_state)

    def _get_volume(self) -> float:
        """Get the volume of the current stream."""
        return float(self.volume_element.get_property('volume'))

    def _set_volume(self, volume: float) -> None:
        """Set the volume of the current stream."""
        self.volume_element.set_property('volume', volume)

    volume = property(_get_volume, _set_volume)

    # pylint: disable=unused-argument
    def on_new_decoded_pad(self, element: Gst.Element, pad: Gst.Pad) -> None:
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
    def on_message(self, bus: Gst.Bus, message: Gst.Message) -> None:
        """Handle message and react accordingly."""
        self._message_type = message.type
        if message.type == Gst.MessageType.EOS:
            self.state = Gst.State.NULL
            self.emit('ended')
        elif message.type == Gst.MessageType.ERROR:
            logger.debug("%s", print(message.parse_error()))
            self.state = Gst.State.NULL
        elif message.type == Gst.MessageType.DURATION_CHANGED:
            self.emit('duration_changed')

    def open(self, filepath: str, duration: bool = True) -> None:
        """Open audio file and optionally query duration."""
        logger.debug('Opening file "%s"', filepath)
        self.state = Gst.State.READY
        self.audiosrc.set_property('location', filepath)
        if duration:
            self._duration = None
        # Force decoding of file so we have a duration
        self.state = Gst.State.PLAYING
        self.pipeline.get_state(Gst.CLOCK_TIME_NONE)  # Wait for state change
        self.state = Gst.State.PAUSED
        self.pipeline.get_state(Gst.CLOCK_TIME_NONE)  # Wait for state change

    def reset(self) -> None:
        """Reset the pipeline."""
        logger.debug('Reset the pipeline')
        self.state = Gst.State.NULL
        filename = self.filename
        self.init_pipeline()
        self.open(filename, False)

    def play(self) -> None:
        """Start playback from current position."""
        self.state = Gst.State.PLAYING

    def pause(self) -> None:
        """Pause playback."""
        self.state = Gst.State.PAUSED

    def move_position(self, amount: int) -> None:
        """Move playback position."""
        new_position = self.position + amount
        # Clamp new_position between 0 and self.duration
        self.position = max(min(new_position, self.duration), 0)
