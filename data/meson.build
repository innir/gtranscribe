# Desktop file
desktop_file = i18n.merge_file(
  input: 'org.innir.gtranscribe.desktop.in',
  output: 'org.innir.gtranscribe.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: datadir / 'applications'
)

# Validate desktop file
if find_program('desktop-file-validate', required: false).found()
  test('Validate desktop file', find_program('desktop-file-validate'),
    args: [desktop_file]
  )
endif

# AppData file
appdata_file = i18n.merge_file(
  input: 'org.innir.gtranscribe.appdata.xml',
  output: 'org.innir.gtranscribe.appdata.xml',
  po_dir: '../po',
  install: true,
  install_dir: datadir / 'metainfo'
)

# Validate appdata file
if find_program('appstreamcli', required: false).found()
  test('Validate appdata file',
    find_program('appstreamcli'),
    args: ['validate', '--no-net', '--explain', appdata_file],
  )
elif find_program('appstream-util', required: false).found()
  test('Validate appdata file',
    find_program('appstream-util'),
    args: ['validate-relax', '--nonet', appdata_file],
  )
endif

# Install UI files
install_subdir('ui',
  install_dir: pkgdatadir
)

# Install icon files
install_subdir('icons',
  install_dir: pkgdatadir
)

# Man page
install_man('gtranscribe.1')
