gTranscribe 0.21 Release Notes
=============================

Bug fixes
---------

  * Get rid of bare 'except's.
    [[3700b4d](https://github.com/innir/gtranscribe/commit/3700b4d)]

  * Add missing import (needed for type annotation).
    [[60f1a27](https://github.com/innir/gtranscribe/commit/60f1a27)]


Maintenance
-----------

  * Move keyboard shortcuts F4/F9 out of on_text_insert().
    [[2c964ec](https://github.com/innir/gtranscribe/commit/2c964ec)]

  * Remove mesonpy build option and fix project name.
    [[6c6ccb9](https://github.com/innir/gtranscribe/commit/6c6ccb9)]

  * Update appdata.xml.
    [[dcf395f](https://github.com/innir/gtranscribe/commit/dcf395f)]



gTranscribe 0.20 Release Notes
=============================

Major changes
-------------

  * Migrate to GTK4.
    [[7629692](https://github.com/innir/gtranscribe/commit/7629692)]


Bug fixes
---------

  * Document available shortcuts.
    [[a7504e2](https://github.com/innir/gtranscribe/commit/a7504e2)]

  * Add zero-padding for H/M/S in duration.strftime.
    [[5ba6afd](https://github.com/innir/gtranscribe/commit/5ba6afd)]

  * Update regex to support resuming from both timestamp formats.
    [[b76b819](https://github.com/innir/gtranscribe/commit/b76b819)]


Maintenance
-----------

  * Migrate to meson build system.
    [[13c43cc](https://github.com/innir/gtranscribe/commit/13c43cc)]

  * Use ruff for linting.
    [[f763f9f](https://github.com/innir/gtranscribe/commit/f763f9f)]

  * Update German translation.
    [[b3cf8df](https://github.com/innir/gtranscribe/commit/b3cf8df)]



gTranscribe 0.11 Release Notes
=============================

New features
------------

  * Add undo/redo functionality.
    [[d4ba34b](https://github.com/innir/gtranscribe/commit/d4ba34b3bd3a21812bcb4e0f0697c70fc424680a)]



gTranscribe 0.10.1 Release Notes
=============================

Bug fixes
---------

  * Make it possible to open file that are longer than 24h.
    [[2e0a4d0](https://github.com/innir/gtranscribe/commit/2e0a4d073ce3721b25badc5199a347091ea45669)]



gTranscribe 0.10 Release Notes
=============================

Dependency changes
---------

  * Remove fallback to GtkSpell - Gspell is available everywhere now.
    [[8d068a5](https://github.com/innir/gtranscribe/commit/8d068a5a7973e7f74afb9af010c750e37f1391b0)]


Bug fixes
---------

  * Correctly toggle play button when used via keyboard shortcuts.
    [[57b02fc](https://github.com/innir/gtranscribe/commit/57b02fc788961ecc7a21f460c71d351b51217abe)]

  * Better cope with GStreamer not able to get the duration of a file.
    [[14f64d1](https://github.com/innir/gtranscribe/commit/14f64d1b5fe1ea69cf6c472040ca6828a770ad84)]
    [[d8be2b6](https://github.com/innir/gtranscribe/commit/d8be2b68f8f04c93e9b847081afe98935a79ec35)]

  * Fix traceback on slower/faster before file is opened.
    [[1fe77d0](https://github.com/innir/gtranscribe/commit/1fe77d0290441c55af79236a83b1e8e2dca6f0ef)]



gTranscribe 0.9 Release Notes
=============================

Bug fixes
---------

  * Fix media keys.
    [[99b1958](https://github.com/innir/gtranscribe/commit/99b19580471619709081e318882fdc030e60b5fa)]

  * Fixes for deprecation warnings & refactoring.
    [[0e26be2](https://github.com/innir/gtranscribe/commit/0e26be2dc9053a9cbdea7c97e60b32de1ceca454)]
    [[7a9c06d](https://github.com/innir/gtranscribe/commit/7a9c06d05dae2765fe42a548fda4d48733b97328)]

  * Make close button work in about dialog.
    [[c29dd68](https://github.com/innir/gtranscribe/commit/c29dd68ed5fbecdeab2bb32bf29bad6fdf0521cf)]

  * Activate speed scale only after a file was loaded.
    [[447e447](https://github.com/innir/gtranscribe/commit/447e44710a7bb5654d9b4186e93ac6a2bce2f1d5)]



gTranscribe 0.8 Release Notes
=============================

Changed behavior
------------

  * Remap key bindings for search:
    Change key bindings for forward/rewind from <CTRL>Left/Right to
    <CRTL><SHIFT>Left/Right so the standard key bindings for moving one
    word backwards/forwards are still usable.
    [[d8c7ef2](https://github.com/innir/gtranscribe/commit/d8c7ef29f6cd200202f34df6597e2bcce3ec80d4)]


New features
------------

  * Add timestamp when pressing F8.
    [[7ed0575](https://github.com/innir/gtranscribe/commit/7ed05758c550c3f8c0d0fb6d73d26ce705c0f771)]

  * Use the de facto standard as timestamp format to make it easier to use the
    output with popular text analysis software. Don't worry, the old format is
    still recognized.
    [[68169a8](https://github.com/innir/gtranscribe/commit/68169a8d968f98f587a137c4c039ca89b09cf369)]


Bug fixes
---------

  * Fix loading of audio files.
    [[8c1da0f](https://github.com/innir/gtranscribe/commit/8c1da0f705edd1915aced4fa2359b76ca662a3ae)]

  * Enable override warning in save dialog.
    [[f037de6](https://github.com/innir/gtranscribe/commit/f037de662a4204f19e35744c0d1d62b4da7211a2)]

  * Only insert timestamp if not at start of file.
    [[b99a96b](https://github.com/innir/gtranscribe/commit/b99a96b3952ec99e284a1a285d0d99a96ced22b0)]



gTranscribe 0.7.1 Release Notes
=============================

Bug fixes
---------

  * Use correct root directory when searching for data files.
    [[0d11280](https://github.com/innir/gtranscribe/commit/0d1128074e4def421db6c3d1fd396c98a045fac0)]



gTranscribe 0.7 Release Notes
=============================

New features
------------

  * Use Gspell if available and fallback to GtkSpell. Gspell is faster and much
    more reliable.
    [[b856011](https://github.com/innir/gtranscribe/commit/b8560119670be36b93c074ddc4a843e7cdda33b1)]

  * Pressing CTRL+J will move the audio file and the cursor to the beginning of
    the current paragraph.
    [[de322d2](https://github.com/innir/gtranscribe/commit/de322d2a2eef0a13dd596468a21c9e13c551ff3f)]
    [[fb81c24](https://github.com/innir/gtranscribe/commit/fb81c24995285cbdb13b1eba9a44eee3da6395ca)]


Bug fixes
---------

  * Always show application icon and logo in AboutDialog.
    [[c9e8686](https://github.com/innir/gtranscribe/commit/c9e8686b3efeda3a04d0c411f1b2044568b5ca75)]

  * Scroll Text to bottom after loading a text file.
    [[f9d9cb9](https://github.com/innir/gtranscribe/commit/f9d9cb91e0eebcb16fe343b8cd38117548082084)]

  * Don't freeze when opening a text file and no audio file is loaded.
    [[f8319b8](https://github.com/innir/gtranscribe/commit/f8319b867738579e83e13bb9c23f4464df0f1c4f)]
