# gTranscribe

Audio player designed to make the transcription of interviews and other sources as easy as possible.

**Author:** Philip Rinn <rinni@inventati.org>
**Homepage:** https://github.com/innir/gtranscribe

## Dependencies

### Runtime Dependencies
- Python >= 3.10 (`python3`)
- PyGObject (`python3-gi`)
- python3-dbus (`python3-dbus`)
- GTK 4 (`gir1.2-gtk-4.0`)
- GtkSourceView 5 (`gir1.2-gtksource-5`)
- libadwaita (`gir1.2-adw-1`)
- libspelling (`gir1.2-spelling-1`)
- GLib 2.0 (`gir1.2-glib-2.0`)
- GStreamer 1.0 (`gir1.2-gstreamer-1.0`)
- GStreamer plugins base (`gir1.2-gst-plugins-base-1.0`)

### Build Dependencies

For building from source with Meson:
- Meson >= 0.59.0 (`meson`)
- Ninja build system (`ninja-build`)
- Python 3 (`python3`)
- Gettext tools for translations (`gettext`)
- Desktop file utilities (`desktop-file-utils`)
- GLib compile schemas (`libglib2.0-dev-bin`)
- AppStream CLI for appdata validation (`appstream`)
- GTK icon cache tool (`gtk-update-icon-cache`)

Additionally for building from source with pip:
- meson-python (`python3-mesonpy` or Python package)
- build (`python3-build` or Python package, recommended)

### Recommended
- GStreamer bad plugins (`gstreamer1.0-plugins-bad`)

## Building and Installing

### Using Meson (recommended for distributions)

```bash
meson setup builddir
meson compile -C builddir
meson install -C builddir
```

### Using pip (for Python users)

Install build dependencies first:
```bash
pip install meson-python build
```

Then install gTranscribe:
```bash
pip install .
```

Or build a wheel:
```bash
python3 -m build
pip install dist/*.whl
```

### Development/Running from source

Without installing:
```bash
./bin/gtranscribe [audiofile]
```

## License

gTranscribe is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License version 3 as published by the Free Software Foundation.

The icon of gTranscribe (gtranscribe.svg) is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License version 2.1 as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU (Lesser) General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
