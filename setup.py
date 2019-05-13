from setuptools import setup

setup(name='pypeds',
      version='0.1.0',
      python_requires='>=3.7',
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
                        'jupyterlab'])
