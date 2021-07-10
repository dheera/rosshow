from setuptools import setup, find_packages

package_name = 'librosshow'

setup(
    name='package_name',
    version='2.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pillow',
        'requests',
    ],
    maintainer='dheera',
    maintainer_email='dheera.r.e.m.o.v.e.t.h.i.s@dheera.net',
    description='rosshow: Visualize ROS topics in a terminal with ASCII art',
    license='bsd.threeclause',
    tests_require=['pytest'],
)
