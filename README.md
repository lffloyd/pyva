# pyva
A compiler written in Python for a subset of Java language.

### Installation

Make sure to have:

* [Python](https://www.python.org/downloads/) >= [3.5](https://www.python.org/downloads/release/python-350/)
    * [pipenv](https://pypi.org/project/pipenv/) - can be installed with ```pip3 install pipenv```. If you have Python >= 3.4, pip is already installed. 
    Otherwise, [here's](https://pip.pypa.io/en/stable/installing/) a tutorial to install it.

### Setup

Create a pipenv environment in your root folder with:
```pipenv shell```

Then, you can install the dependencies through:
```pipenv install```

Once finished, you can run or edit the project.

### Build instructions

To build the project, you'll need pyinstaller. If you've followed the previous steps, you already have it.

So move to the root folder of the project. There, execute
the following command to build:

```pyinstaller cli.py --name pyva --add-data src/parsetab.py:src```

The last parameter is a parsing table. Notice that is recommended to have previously created this table, 
because otherwise, on every execution of the program, a new parsing table will
be generated. You can easily create a parsing table by executing the program once.

If success ensues, an executable file called ```pyva``` will be present in your ```dist/```
 folder. Every file inside it is needed for the program execution.
 
### Ply documentation

You can find simple step-by-step implementations of lexers and parsers using
Ply [here](http://www.dabeaz.com/ply/ply.html).

### Additional links

* [Python docs about Regex](https://docs.python.org/3.3/howto/regex.html#matching-characters) - to learn how Python 
treats regex
* [Regexr](https://regexr.com) - to try some regex
