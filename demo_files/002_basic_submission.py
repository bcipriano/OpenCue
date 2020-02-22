
import os

from outline import Outline, cuerun
from outline.modules.shell import Shell
from outline.modules.makemov import MakeMov


BLENDER_CMD = 'blender -b -noaudio /shots/scenes/pipe_demo/blend/demo_001.blend '+ \
              '-o /shots/scenes/pipe_demo/blend/images/demo_001_ -F PNG -x 1 '+ \
              '-f #IFRAME#'

RENDER_OUTPOUT = '/shots/scenes/pipe_demo/blend/images/demo_001_%04d.png '
MOV_OUTPUT = '/shots/scenes/pipe_demo/blend/images/test.mp4'

WRAPPER_DIR = '/opt/opencue/demo_files'


# Create an outline for the job
job_name = 'pipeline-demo-001'
shot_name = '010A_020'
show_name = 'testing'
user = 'opencue_user'
outline = Outline(job_name, shot=shot_name, show=show_name, user=user)

wrapper_path = os.path.join(WRAPPER_DIR, 'simple_dummy_wrapper')

# create a layer
layer_name = 'blender-test'
chunk_size = 1
threads = 1.0
frame_range = '1000'
threadable=False
blender_layer = Shell(layer_name, command=BLENDER_CMD.split(), chunk=chunk_size,
                      threads=threads, range=frame_range, threadable=threadable)
blender_layer.set_arg('wrapper', wrapper_path)

outline.add_layer(blender_layer)


# Create a makemov layer
layer_name = 'ffmpeg-test'
chunk_size = 1
threads = 1.0
frame_range = '1000'
threadable=False
makemov_layer = MakeMov(layer_name, input=RENDER_OUTPOUT, output=MOV_OUTPUT,
                        chunk=chunk_size, threads=threads, range=frame_range,
                        threadable=threadable)

# Add dependency
makemov_layer.depend_all(blender_layer)
makemov_layer.set_arg('wrapper', wrapper_path)

outline.add_layer(makemov_layer)


# Submit job
cuerun.launch(outline, use_pycuerun=False)

