from setuptools import setup

package_name = 'drive'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='alex',
    maintainer_email='akm16929@gmail.com',
    description='Control node for driving along wall',
    license='MIt',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'drive = drive.drive:main'
        ],
    },
)
