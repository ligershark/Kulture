#vNext


Sublime extension for [ASP.NET vNext](https://github.com/aspnet/home)

## Compatibility

This package has **ONLY** been tested on ST3 [**Build 3059**](http://www.sublimetext.com/3) of Sublime on Windows 8.1 and OS X 10.9.4

## Dependencies

### ASP.NET vNext
You must have ASP.NET vNext installed on your machine. Follow the instructions at [ASP.NET Home](https://github.com/aspnet/home)

**NOTE:** Installation of ASP.NET vNext on Mac requires Mono >= 3.4.1 which requires you to Compile Mono from source

### [jsonschema](https://pypi.python.org/pypi/jsonschema/2.3.0) - A Python package

- Download [jsonschema 2.3.0](https://pypi.python.org/packages/source/j/jsonschema/jsonschema-2.3.0.zip#md5=0275f70c5f7c65657555ff478a4fc89c)
- Unzip the archive

#### On Win 8.1
Copy jsonschema folder to `C:\Program Files\Sublime Text 3`
#### On OS X 10.9.4
Copy jsonschema folder to `/Applications/Sublime\ Text.app/Contents/MacOS/`

##Features

- [Build Integration](#build-integration)
- [JSON Schema Validation](#json-schema-validation)
- [Ability to Run K Commands from inside Sublime](#k-commands)

###Build Integration

Select `Tools -> Build System -> vNext`

- Press `Ctrl(Cmd) + B` or `F7` to build projects
- `F4` takes you to the next error
- `Shft + F4` takes you to the previous error

###JSON Schema Validation

- Press `Ctrl(Cmd) + Shift + P` to bring up the command palette
- Type `Validate JSON Schema`
- View results of the validation in  the status bar

###K Commands

Ability to execute K Commands specified in Project.json as well as common kpm tasks

- Press `Ctrl(Cmd) + Shift + P` to bring up the command palette
- Type `Run K Commands`
- Powershell/Terminal will launch and execute specified task

## Credits

### [jsonschema](https://github.com/Julian/jsonschema)

<pre>
Copyright (c) 2013 Julian Berman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
</pre>

### [Sublime Terminal]()

<pre>
All of Sublime Terminal is licensed under the MIT license.

  Copyright (c) 2011 Will Bond <will@wbond.net>

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
</pre>