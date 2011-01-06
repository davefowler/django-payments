from distutils.core import setup
import os, sys

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

setup(name='django-payments',
      version='1.4.3',
      description='/dev/payments tornado python bindings',
      author='Dave Fowler',
      author_email='dave@chart.io',
      url='http://www.chart.io.com/',
      packages=['devpayments'],
      package_dir = {'devpayments' : 'src'}
)
