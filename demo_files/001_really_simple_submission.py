

from outline import Outline, cuerun
from outline.modules.shell import Shell


CMD = 'echo "Hello Pipeline Folks #IFRAME#"'

# Setup some variables
job_name = 'pipeline-demo-001'
shot_name = '010A_020'
show_name = 'testing'
user = 'opencue_user'

# Layer variables
layer_name = 'silly-test'
chunk_size = 1
threads = 1.0
frame_range = '1000'
threadable=False


# Create an outline for the job
outline = Outline(job_name, shot=shot_name, show=show_name, user=user)

# create a layer
layer = Shell(layer_name, command=CMD.split(), chunk=chunk_size,
              threads=threads, range=frame_range, threadable=threadable)

outline.add_layer(layer)


# Submit job
cuerun.launch(outline, use_pycuerun=False)

