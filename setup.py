from setuptools import setup, find_packages

package_name = 'rosshow'

setup(
    name=package_name,
    version='2.0.0',
    packages=find_packages(),
    data_files=[
        ('share/' + package_name, ['package.xml']),
    ],
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
    entry_points={
        'console_scripts': [
            "rosshow = rosshow.rosshow:main",
        ],
    },
)
