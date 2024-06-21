from setuptools import setup, find_packages

package_name = 'rosshow'

setup(
    name=package_name,
    version='2.0.1',
    packages=find_packages(),
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
    ],
    install_requires=[
        'numpy',
        'pillow',
        'requests',
    ],
    maintainer='dheera',
    maintainer_email='dheera@dheera.net',
    description='rosshow: Visualize ROS topics in a terminal with ASCII art',
    license='bsd.threeclause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "rosshow = rosshow.rosshow:main",
        ],
        'ros2cli.command': [
            'show = rosshow.command.show:ShowCommand',
        ]
    },
)
