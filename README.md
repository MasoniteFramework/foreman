# Masonite Foreman

**Still under development. This project currently only works with Macs. Windows and Linux support coming soon.**

## Requirements:

* Python 3.4 +
* Mac

## Introduction

Masonite foreman is a way to automatically serve all (or some) of your python applications without needing to worry about activating virtual environments and running serve commands.

You can register a directory where your python projects live and all Python projects in that directory will be served under a `{your app}.test` domain. The `.test` tld can be changed.

## Getting Started

First install Masonite foreman using the terminal.

```
$ pip3 install masonite-foreman --user
```

**Make sure you use your python3 pip installation.**

Once pip installed you will need to run the `install` commands:

```
$ foreman install
```

This will add a few required packages by brew installing them.

## Registering Directories

One of the powerful features of Foreman is allowing you to register entire directories. Python applications will be found inside the directory and be served automatically.

Let's take a directory structure like this:

```
~/sites/
    app1/
        .. Masonite application ..
    app2/
        .. Masonite application ..
    app3/
        .. Django application ..
```

You can go to this directory and register it:

```
$ cd ~/sites
$ foreman register
```

This will register that directory and immediately start serving all python applications under that `{app}.test` domain:

You can then go to `app1.test`, `app2.test` and `app3.test` and see your applications. This is all done without needing to run each server.

This will also detect changes in your application as well so no needing to wait to reload the server.

## Starting Applications

When you first start your system up you can run all the applications inside registered directories again by running:

```
$ foreman start
```

## Starting Individual Applications

Sometimes you will not want to run all applicatons but just the ones you want to work on. You can do this by going to your application and running the `start .` command:

```
$ cd ~/sites/app1
$ foreman start .
```

This will only serve that application at `app1.test` but not any other apps.

## Registering Virtual Environments

Foreman will do its best to detect the virtual environment if it is inside the project directory but virtual environments can be literally anywhere.

If your virtual environment is not inside your project directory you can register it specifically.

First activate your virtual environment and thn run the virtual environment register command.

```
$ cd ~/sites/app1
$ source /virtualenvs/app1/bin/activate
$ foreman venv:register
```

This will register that virtual environment with that application with foreman. Then you can start that project:

```
$ foreman start .
```

## Deregister Directories

Just like registering directories you can register them as well:

```
$ foreman deregister
```

