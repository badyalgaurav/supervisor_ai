from setuptools import setup, find_packages

setup(
    name='geofence',
    version='0.2.0',
    packages=find_packages(),
    package_data={
        'my_package': ['content/*.wav', 'content/*.mp3'],
    },
)