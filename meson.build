project('gTranscribe',
  version: '0.21',
  meson_version: '>= 0.59.0',
  license: 'GPL-3.0',
)

# Project information
app_id = 'org.innir.gtranscribe'
python = import('python').find_installation('python3')
i18n = import('i18n')
gnome = import('gnome')

# Paths
prefix = get_option('prefix')
bindir = prefix / get_option('bindir')
datadir = prefix / get_option('datadir')
pkgdatadir = datadir / meson.project_name()
localedir = prefix / get_option('localedir')

# Configuration
conf = configuration_data()
conf.set('PACKAGE_NAME', meson.project_name())
conf.set('PACKAGE_VERSION', meson.project_version())
conf.set('prefix', prefix)
conf.set('bindir', bindir)
conf.set('pkgdatadir', pkgdatadir)
conf.set('localedir', localedir)
conf.set('PYTHON', python.full_path())

# Subdirectories
subdir('data')
subdir('gtranscribe')
subdir('bin')
subdir('po')

# Post-install scripts
gnome.post_install(
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
