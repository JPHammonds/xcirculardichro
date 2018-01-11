'''
 Copyright (c) 2017, UChicago Argonne, LLC
 See LICENSE file.
'''
from setuptools import setup
from setuptools import find_packages
import xcirculardichro
PACKAGE_NAME = 'xcirculardichro'
setup(name=PACKAGE_NAME,
      version='0.8rc5',
      description='Library to provide PyQt5 widgets to display spec file information read using ' +
                   'spec2nexus.spec file library',
      author = 'John Hammonds',
      author_email = 'JPHammonds@anl.gov',
      url = '',
      packages = find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
      install_requires = ['spec2nexus>=2017.901.4',
                          'specguiutils>=0.5',],
      #                    'pyqt>=5.6',],  Also requires pyqt>=5.6.  This is not distributed by pypi if using anacoda do conda install pyqt
      #                    'matplotlib>=2.1.0',],  Also requires pyqt>=5.6.  This is not distributed by pypi if using anacoda do conda install pyqt
      #                    'h5py>=2.7.1',],  Also requires pyqt>=5.6.  This is not distributed by pypi if using anacoda do conda install pyqt
      python_requires = ">=3.5, <4",
      license = 'See LICENSE File',
      platforms = 'any',
      scripts = ['Scripts/xcirculardichro',
                 'Scripts/xcirculardichro.bat']
      
)