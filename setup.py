from setuptools import setup

setup(name='pypeds',
      version='0.1.5',
      python_requires='>=3.6',
      description='Python package to work with IPEDS and other higher education datasets.',
      url='https://brocktibert.com/',
      author='@brocktibert',
      author_email='btibert3@gmail.com',
      license='MIT',
      packages=['pypeds'],
      zip_safe=False,
      include_package_data=True,
      install_requires=['pandas',
                        'requests',
                        'altair',
                        'dfply',
                        'numpy'])
