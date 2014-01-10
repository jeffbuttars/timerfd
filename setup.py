from distutils.core import setup, Extension

module1 = Extension('timerfd', sources=['timerfd/timerfd.c'])

setup(
    version="0.1",
    description="FD timer for python",
    ext_modules=[module1]
)
