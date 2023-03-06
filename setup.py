
from setuptools import setup, find_packages

setup(name='wdl_array_tools',
      version=0.1,
      author='Aaron Maurais',
      packages=find_packages(),
      package_dir={'wdl_array_tools': 'src'},
      python_requires='>=3.8',
      install_requires=[],
      entry_points={'console_scripts': ['wdl_array_tools=src:wdl_array_tools',
                                        'tsv_to_gct=src:tsv_to_gct']}
)
