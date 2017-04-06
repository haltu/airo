# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# Licensed under the EUPL v1.1
#

from setuptools import setup, find_packages


def get_version():
  try:
    import subprocess
    p = subprocess.Popen('hg id -t', shell=True, stdout=subprocess.PIPE)
    tag = p.stdout.read()[1:].strip()
    return tag
  except:
    return 'dev'

setup(
    name = 'wilma',
    version = get_version(),
    license = 'Haltu',
    description = "Desktop Lite Wilma integration",
    author = 'Haltu',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
      'requests',
      ]
)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

