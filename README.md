# fix-conda-ssl

Fix the dreaded Conda SSLError on Windows by copying DDLs. This is not about validating certificates behind a corporate firewall but about Python not being able to `import ssl` inside conda environments resulting in "SSL module is not available" errors.


## The Problem

Every once in a while, the planets are out of alignment and conda on Windows is broken again. Sometimes it is only the conda-forge channel for the newest version of Python, sometimes it is (much) worse. Reinstalling the latest version of Anaconda is, unfortunately, not a quick solution for my lab full of university-managed Windows PCs without administrator access. After noticing on a Friday late-afternoon that SSL was broken again and you could not only not install packages into a conda environment but also not run pipx-installed applications like Poetry inside of an environment, I needed a student-friendly solution to the problem. After all, when my students come in after the weekend I don't want to send them home because of broken machines. So, I sat down to write this tool.


## The solution

Many reports can be found detailing the problem starting years ago. The solution seems to be pretty straight-forward, although it can be a bit cumbersome to perform. Basically, you just need to copy libcrypo-something.dll and libssl-something.dll from the environments Library/bin folder to its DLLs folder. So, enter `fixconda`.

![Screenshot of the terminal user interface](https://raw.githubusercontent.com/davidfokkema/fix-conda-ssl/main/fixcondasslapp_screenshot.svg)


## Installation and usage

You probably won't be able to install this package inside broken environments. Usually, the base environment works well so be sure to activate the base environment before performing these steps.

It is best to install using pipx to keep this application out of your base conda environment:
```
> pipx install fix-conda-ssl
```
If needed, you can also install using pip but won't be able to fix the environment fix-conda-ssl is installed to:
```
> pip install fix-conda-ssl
```
Start the application by typing:
```
> fixconda
```
Select an environment using the mouse or cursor keys and click or press enter to fix the environment.