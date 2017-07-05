from setuptools import setup

setup(
    name='pixelbot',
    version='0.1a',
    description='Create bots to paint pixels on pixelcanvas.io.',
    url='https://github.com/possatti/pixelbot',
    author='Lucas Possatti',
    author_email='lucas.cpossatti@gmail.com',
    license='MIT',
    packages=['pixelbot'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pixelbot = pixelbot.cli:main',
        ],
    },
    zip_safe=True)
