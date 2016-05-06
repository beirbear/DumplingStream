from setuptools import setup

setup(name='server_stream',
      version='0.1.0',
      install_requires=['falcon'],
      packages=['server_stream', 'client_stream'],
      entry_points={
          'console_scripts': [
              'server_stream = server_stream.__main__:main',
              'client_stream = client_stream.__main__:main'
          ]
      }
      )
