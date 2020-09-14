# -*- mode: python ; coding: utf-8 -*-

import glob
import platform

block_cipher = None

# Plugins are not explicit imports, but get imported by name at runtime -- see Plugins.py.
# We need to build up a list of them to be passed to `hiddenimports` below.
def get_cuegui_plugins():
  for plugin_file in glob.glob('./cuegui/plugins/*.py'):
    plugin_name, _ = os.path.splitext(os.path.basename(plugin_file))
    if plugin_name != '__init__':
      yield 'cuegui.plugins.%s' % plugin_name

a = Analysis(['run.py'],
             pathex=['../pycue', './cuegui', './cuegui/plugins'],
             binaries=[],
             datas=[
               ('../pycue/opencue/default.yaml', 'opencue'),
               ('cuegui/config/*', 'cuegui/config'),
               ('cuegui/images/*.png', 'cuegui/images'),
               # It's a bit non-standard to add code as a data file, however with the one-file
               # bundling method the plugins get bundled into an archive to be used at runtime,
               # which breaks the plugin system as it looks for plugins in a separate plugins/
               # directory. Adding them manually here maintains that directory structure. This
               # could be improved in the future.
               ('cuegui/plugins/*.py', 'cuegui/plugins'),
             ],
             hiddenimports=[
               'pkg_resources',
               'cuegui.DarkPalette',
               'cuegui.images.bluecurve',
               'cuegui.images.bluecurve.icons_rcc',
               'cuegui.images.crystal',
               'cuegui.images.crystal.icons_rcc',
             ] + list(get_cuegui_plugins()),
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='CueGUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='../images/OpenCue.ico')

if platform.system() == 'Darwin':
  app = BUNDLE(exe,
               name='CueGUI.app',
               icon='../images/OpenCue.icns',
               bundle_identifier=None,
               info_plist={
                 # This is needed for the application to be rendered properly on retina screens.
                 'NSPrincipalClass': 'NSApplication',
               })
