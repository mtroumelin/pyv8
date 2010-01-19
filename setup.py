#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, os.path
from distutils.core import setup, Extension

if not os.environ.has_key('V8_HOME') or not os.path.exists(os.path.join(os.environ.get('V8_HOME'), 'include', 'v8.h')):
    print "ERROR: you should set V8_HOME to the Google v8 folder, or download and build it first. <http://code.google.com/p/v8/>"
    sys.exit()

source_files = ["Exception.cpp", "Context.cpp", "Engine.cpp", "Wrapper.cpp", "Debug.cpp", "Locker.cpp", "PyV8.cpp"]

macros = [
    ("BOOST_PYTHON_STATIC_LIB", None),
    ("V8_NATIVE_REGEXP", None),
    ("ENABLE_DISASSEMBLER", None),
    ("ENABLE_LOGGING_AND_PROFILING", None),
    ("ENABLE_DEBUGGER_SUPPORT", None),
    ]

include_dirs = [
  os.path.join(os.environ.get('V8_HOME'), 'include'),
  os.environ.get('V8_HOME'),
  os.path.join(os.environ.get('V8_HOME'), 'src'),
]
library_dirs = []
libraries = []
extra_compile_args = []
extra_link_args = []
  
v8_lib = 'v8_g' if os.environ.get('DEBUG') else 'v8' # contribute by gaussgss

if os.name == "nt":
  include_dirs += [
    os.environ.get('BOOST_HOME'),
    os.path.join(os.environ.get('PYTHON_HOME'), 'include'),
  ]
  library_dirs += [
    os.path.join(os.environ.get('V8_HOME'), 'tools\\visual_studio\\Release\\lib'),
    os.path.join(os.environ.get('BOOST_HOME'), 'stage/lib'),
    os.path.join(os.environ.get('PYTHON_HOME'), 'libs'),
  ]  
  
  include_dirs += [p for p in os.environ["INCLUDE"].split(';') if p]
  library_dirs += [p for p in os.environ["LIB"].split(';') if p]
  
  macros += [("V8_TARGET_ARCH_IA32", None), ("WIN32", None)]
  
  libraries += ["winmm", "ws2_32"]
  extra_compile_args += ["/O2", "/GL", "/MT", "/EHsc", "/Gy", "/Zi"]
  extra_link_args += ["/DLL", "/OPT:REF", "/OPT:ICF", "/MACHINE:X86"]
  
elif os.name == "posix" and sys.platform == "linux2":
  library_dirs += [
    os.environ.get('V8_HOME'),
  ]
  
  libraries += ["boost_python", v8_lib, "rt"]
  
  if hasattr(os, 'uname') and os.uname()[-1] == 'x86_64':
    extra_link_args += ["-fPIC"]
    macros += [("V8_TARGET_ARCH_X64", None)]
  else:
    macros += [("V8_TARGET_ARCH_IA32", None)]

elif os.name == "mac": # contribute by Artur Ventura
  include_dirs += [
    os.environ.get('BOOST_HOME'),
  ]
  library_dirs += [os.path.join('/lib')]
  libraries += ["boost_python", v8_lib, "c"]

elif os.name == "posix" and sys.platform == "darwin": # contribute by progrium
  include_dirs += [
    "/opt/local/include", # use MacPorts to install Boost
  ]
  
  library_dirs += [
    os.environ.get('V8_HOME'),
  ]
  
  libraries += ["boost_python-mt", v8_lib]
  
  if hasattr(os, 'uname') and os.uname()[-1] == 'x86_64':
    extra_link_args += ["-fPIC"]
    macros += [("V8_TARGET_ARCH_X64", None)]
  else:
    macros += [("V8_TARGET_ARCH_IA32", None)]
      
else:
  print "ERROR: unsupported OS (%s) and platform (%s)" % (os.name, sys.platform)

pyv8 = Extension(name = "_PyV8",
				 sources = [os.path.join("src", file) for file in source_files],                 
				 define_macros = macros,
				 include_dirs = include_dirs,
				 library_dirs = library_dirs,
				 libraries = libraries,
				 extra_compile_args = extra_compile_args,
				 extra_link_args = extra_link_args,
				 )

setup(name='PyV8',
    version='0.8',
    description='Python Wrapper for Google V8 Engine',
    long_description="PyV8? is a python wrapper for Google V8 engine, it act as a bridge between the Python and JavaScript? objects, and support to hosting Google's v8 engine in a python script.",
    platforms="x86",
    author='Flier Lu',
    author_email='flier.lu@gmail.com',
    url='http://code.google.com/p/pyv8/',
    download_url='http://code.google.com/p/pyv8/downloads/list',
    license="Apache Software License",
    py_modules=['PyV8'],
    ext_modules=[pyv8],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX', 
        'Programming Language :: C++',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities', 
    ])