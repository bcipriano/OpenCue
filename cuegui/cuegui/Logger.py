#  Copyright Contributors to the OpenCue Project
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


"""
Allows the creation of a logger.
"""


from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import logging
import os
import sys

import cuegui.Constants


def getLogger(name):
    """Returns or creates and returns a logger of the given name.
    @param name: The name of this logging handler
    @type  name: string
    @return: The new handler
    @rtype:  Handler"""
    os.makedirs(os.path.dirname(cuegui.Constants.LOG_FILE_PATH), exist_ok=True)

    logger_format = logging.Formatter(cuegui.Constants.LOGGER_FORMAT)
    logger = logging.getLogger(name)
    # This prevents duplicate logging to stderr.
    logger.propagate = False

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(getattr(logging, cuegui.Constants.LOGGER_LEVEL))
    stderr_handler.setFormatter(logger_format)
    logger.addHandler(stderr_handler)

    file_handler = logging.FileHandler(cuegui.Constants.LOG_FILE_PATH)
    file_handler.setLevel(getattr(logging, cuegui.Constants.LOGGER_LEVEL))
    file_handler.setFormatter(logger_format)
    logger.addHandler(file_handler)

    return logger
