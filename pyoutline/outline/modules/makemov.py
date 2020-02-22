
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from past.builtins import execfile
import logging
import os

from outline import util
from outline.layer import Layer, Frame


logger = logging.getLogger("outline.modules.shell")

__all__ = ["MakeMov"]


FFMPEG_CMD = 'ffmpeg -r 60 -f image2 -s 1920x1080 -start_number #IFRAME# -i ' + \
             '{input} -vframes 1 -vcodec libx264 -crf 25  -pix_fmt yuv420p {output}'


class MakeMov(Layer):
  """
  Provides a method of executing a shell command over an
  arbitrary frame range.
  """
  def __init__(self, name, **args):
    Layer.__init__(self, name, **args)

    self.require_arg("input")
    self.require_arg("output")
    command = FFMPEG_CMD.format(input=self.get_arg('input'), output=self.get_arg('output')).split()
    self.set_arg('command', command)
    self.set_arg("proxy_enable", False)
  
  def _execute(self, frame_set):
    """Execute the shell command."""
    for frame in frame_set:
      self.system(self.get_arg("command"), frame=frame)
