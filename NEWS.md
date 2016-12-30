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
