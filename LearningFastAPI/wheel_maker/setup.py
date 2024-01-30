from setuptools import setup, find_packages

setup(
    name='geo_fence',
    version='0.1.0',
    packages=find_packages(),
    package_data={
        'my_package': ['content/*.wav', 'content/*.mp3'],
    },
)