# pysrvany

Run executable as Windows Service and respawn it in case of crash


## Usage

Installation

    pip install PyWin32  # PyWin32 is needed
    pip install pysrvany


Create a service for an executable

*use absolute path in arguments*

    pysrvany_cli.py install_exe <service-name> <executable> [<arguments>...] [--pysrvany-cwd <working-dir>]


Start/Stop/Delete the service

    sc {start|stop|delete} <service-name>


### Custom service

You can create a service for a custom class like this

    class SampleService:
        def __init__(self, *args):
            pass
    
        def run(self):
            pass
    
        def stop(self):
            pass

The command is:

    pysrvany_cli.py install_class <service-name> <class-dot-path> [<arguments>...]


```<class-dot-path>``` is the string you should use if you want 'locate' the class

Example ```mypck.mymod.MyClass``` means class ```MyClass``` in the module ```mymod``` in the package ```mypck```

Warning: ```mypck``` must be in ```sys.path```

**Example:**

Install:

    pysrvany_cli.py install_class test_pysrvany pysrvany.samples.MockService %TEMP%\pysrvany_log.log
    
Start the service:

    sc start test_pysrvany
    
Check log:

    type %TEMP%\pysrvany_log.log

Stop and delete service:

    sc stop test_pysrvany
    sc delete test_pysrvany


## Tests

To run tests install the package in developer mode:

    cd pysrvany
    pip install -e .

To run the test cases:

    cd pysrvany
    python -m unittest


## Package

To build a package:

    cd pysrvany
    python setup.py sdist
