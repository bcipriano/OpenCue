
import xml.dom.minidom

import outline
import outline.backend.cue

outline_path = '/opt/opencue/demo_files/demo.outline'

# load the outline
ol = outline.load_outline(outline_path)
launcher = outline.cuerun.OutlineLauncher(ol)

# print what the xml looks like
xml_str = launcher.serialize(use_pycuerun=True)
dom = xml.dom.minidom.parseString(xml_str)
print dom.toprettyxml()

# Launch the job
# outline.cuerun.launch(ol, use_pycuerun=True)

