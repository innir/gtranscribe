project('gtranscribe',
  version: '0.20',
  meson_version: '>= 0.59.0',
  license: 'GPL-3.0-or-later',
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

# Python dependencies (checked at runtime)
python_modules = [
  'gi',
  'dbus',
]

foreach module : python_modules
  if run_command(python, '-c', 'import @0@'.format(module), check: false).returncode() != 0
    warning('Python module @0@ not found, it is required at runtime'.format(module))
  endif
endforeach

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
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
