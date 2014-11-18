# Sublime Kulture

A Sublime Text 3 extension for [ASP.NET vNext](https://github.com/aspnet/home)

In this readme you will learn how to install the components to get started with ASP.NET in Sublime Text 3.
There is also a getting started tutorial to show you some of the features included with this release.

[![Video](http://img.youtube.com/vi/1g2I9SJZ5XI/0.jpg)](https://www.youtube.com/watch?v=1g2I9SJZ5XI)

# Installation: Mac OS X

0. Install [ASP.NET vNext Command Line Tools](https://github.com/aspnet/home#getting-started)

0. Download [Sublime Text 3](http://www.sublimetext.com/3)

0. Install Sublime Kulture
  __Using the [Package Control Plugin](https://sublime.wbond.net/)__
  * Follow these [instructions to install package control](https://sublime.wbond.net/installation)
  * Bring up the Command Palette (Cmd + Shift + P on OS X, Ctrl + Shift + P on Windows).
  * Select `Package Control: Install Package`
  * Select `Kulture` when the list appears.
  * Package Control will automatically keep Kulture up to date with the latest version.

  __Manual Install__
  * Install Sublime Kulture by cloning this repo into `/Users/{user}/Library/Application\ Support/Sublime\ Text\ 3/Packages`
    <pre><code>git clone https://github.com/ligershark/Kulture.git</code></pre>

# Installation: Windows

0. Install [ASP.NET vNext Command Line Tools](https://github.com/aspnet/home#getting-started)
  * Perpare Powershell execution policy. In an Admin PowerShell window execute the following command.
  <pre><code>Set-ExecutionPolicy RemoteSigned</code></pre>
  * From an admin command prompt window run the following command
  <pre><code>powershell -NoProfile -ExecutionPolicy unrestricted -Command "iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/aspnet/Home/master/kvminstall.ps1'))"</code></pre>
  * Close the command prompt window and open a new command prompt window and run the following commands
  <pre><code>kvm upgrade</code></pre>
  * If Sublime was already installed and running while installing ASP.NET vNext Command Line Tools, you will need to restart Sublime for the changes to work.

0. Download and Install [Sublime Text 3](http://www.sublimetext.com/3)

0. Install Sublime Kulture

  __Using the [Package Control Plugin](https://sublime.wbond.net/)__
  * Follow these [instructions to install package control](https://sublime.wbond.net/installation)
  * Bring up the Command Palette (Cmd + Shift + P on OS X, Ctrl + Shift + P on Windows).
  * Select `Package Control: Install Package`
  * Select `Kulture` when the list appears.
  * Package Control will automatically keep Schema Validator up to date with the latest version.

  __Manual Install__
  * Install Sublime vNext by cloning this repo into `C:\Users\{user}\AppData\Roaming\Sublime Text 3\Packages`
    <pre><code>git clone https://github.com/ligershark/Kulture.git</code></pre>

  > Note: The Sublime Text 3 directory may not exist if you have never launched Sublime before. If you are unable to locate this directory try launching Sublime and try again


#Getting Started

This tutorial will show you how you can get started with ASP.NET vNext in Sublime Text 3. After completing this tutorial you will be familiar with how to use Sublime Kulture and its primary features.

The first thing we will do is grab the samples. Using your favorite git client clone the repo at [ASP.NET vNext Home](https://github.com/aspnet/home)

    git clone https://github.com/shirhatti/Home.git
    
If you prefering using `yo` instead you can download our yeoman generator
 > Note: This requires you to have node.js and npm already installed

    npm install -g yo
    npm install -g generator-aspnet
    
To run the yeoman scaffolder, type
    
    yo aspnet
    

Let's go ahead and open the included HelloMvc sample in Sublime. In Sublime, click on `File -> Open Folder` and navigate to the `Home\Samples\HelloMvc` to open it up.

  > Note: In Sublime for Mac use the `File -> Open` command

Since we just grabbed this from source control there are NuGet packages which this project requires that are missing. To restore the NuGet packages

- Press `Ctrl(Cmd) + Shift + P` to bring up the command palette
- Type `Run K Commands` and hit Enter (Return)
- Type `kpm restore` and hit Enter (Return)

_Note:_ when executing `kpm restore` if you get an error about missing NuGet packages you can execute the alternate command `kpm restore -s https://www.myget.org/F/aspnetvnext/api/v2`

You should see a Terminal/Powershell window launch and execute your commands.

Now, let's go ahead and tell Sublime to use `ASP.NET` as the build system. To do this, click `Tools -> Build System -> ASP.NET`

- Press `Ctrl(Cmd) + B` or `F7` to build projects

You should be able to see the output of your build in the output window towards the bottom of your screen. At this point your code should have built successfully.

Now let's see what the experience looks like if there is an error in your .cs file. Introduce an error in the Startup.cs file and try building again. You should now see errors in the output window. You can navigate through the errors as follows

- `F4` takes you to the next error
- `Shft + F4` takes you to the previous error

When an error has focus it will be highlighted in the build results and your cursor will be taken to the line and column where the error was reported.

After we resolve all the errors we have introduced, let us try and run the application

- Press `Ctrl(Cmd) + Shift + P` to bring up the command palette
- Type `Run K Commands` and hit Enter (Return)
- Type `k web` and hit Enter (Return)
- If you are on a Mac, type `k kestrel` and hit Enter (Return)

You should see a Terminal/Powershell window launch and start running your server. You can navigate to `http://localhost:5001` (or `http://localhost:5000` on a Mac) in your favorite browser you view the website.

#Intellisense

To be able to get intellisense working within Sublime please install [OmnisharpSublime](https://github.com/moonrabbit/OmniSharpSublime) (follow the instructions in the README).

To get intellisense with `ASP.Net vNext` projects you need to create a project file in Sublime. Go to `Project - Save Project As` and enter in a name for your project.  `OmniSharpSublime` will use this to know what files and assemblies it needs to provide intellisense for (**TIP** : Close & Re-Open Sublime if you do not see intellisense, it may take 10 secs for the intellisense server [OmniSharpServer](https://github.com/nosami/OmniSharpServer) to start once Sublime has loaded all the plugins)

Once OmniSharpSublime is installed and you have a project file you should be able to see intellisense:

![intellisense](http://i.imgur.com/YRBPzbO.png)


## Credits

### [Sublime Terminal](https://github.com/wbond/sublime_terminal)

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
