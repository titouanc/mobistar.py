from setuptools import setup

setup(
    name='mobistarpy',
    version='0.1',
    description='Send SMS with your Mobistar phone number',
    url='https://github.com/titouanc/mobistar.py',
    author='iTitou',
    author_email='moiandme@gmail.com',
    license='Beerware',
    packages=['mobistarpy'],
    install_requires=['requests'],
    zip_safe=False,
    scripts=['bin/mobistar.py'],
)
