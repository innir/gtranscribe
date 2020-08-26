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
