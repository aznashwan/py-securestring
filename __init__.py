# Copyright 2015, Nashwan Azhari.
# Licensed under the GPLv2, see LICENSE file for details.

import platform


if platform.system() != 'Windows':
    raise ImportError("securestring module only meant to run on Windows!")
