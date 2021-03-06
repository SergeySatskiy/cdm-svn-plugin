# -*- coding: utf-8 -*-
#
# cdmsvnplugin - Codimension IDE svn plugin
# Copyright (C) 2017  Sergey Satskiy <sergey.satskiy@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Setup script for the Codimension IDE svn plugin"""

import sys
import os.path
from setuptools import setup

description = 'Codimension IDE svn plugin'

plugin_desc_file = 'src/subversion.cdmp'

def getPluginVersion():
    """The version must be updated in the .cdmp file"""
    if not os.path.exists(plugin_desc_file):
        print('Cannot find the plugin description file. Expected here: ' +
              plugin_desc_file, file=sys.stderr)
        sys.exit(1)

    with open(plugin_desc_file) as dec_file:
        for line in dec_file:
            line = line.strip()
            if line.startswith('Version'):
                return line.split('=')[1].strip()
    print('Cannot find a version line in the ' + plugin_desc_file,
          file=sys.stderr)
    sys.exit(1)

def getFileList():
    """Provides a list of the package files"""
    files = [plugin_desc_file]
    dir_name = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + 'src'
    for item in os.listdir(dir_name):
        if item.endswith('.py') or item.endswith('.png'):
            files.append('src/' + item)
    return files


try:
    import pypandoc
    converted = pypandoc.convert('README.md', 'rst').splitlines()
    no_travis = [line for line in converted if 'travis-ci.org' not in line]
    long_description = '\n'.join(no_travis)
except ImportError:
    print('pypandoc package is not installed: the markdown '
          'README.md convertion to rst failed', file=sys.stderr)
    import io
    # pandoc is not installed, fallback to using raw contents
    with io.open('README.md', encoding='utf-8') as readme_file:
        long_description = readme_file.read()


setup(name='cdmsvnplugin',
      description=description,
      long_description=long_description,
      version=getPluginVersion(),
      author='Sergey Satskiy',
      author_email='sergey.satskiy@gmail.com',
      url='https://github.com/SergeySatskiy/cdm-svn-plugin',
      license='GPLv3',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3'],
      platforms=['any'],
      data_files=[('/cdmplugins/subversion', getFileList())])
