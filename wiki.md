# Wiki

Remember, everything written down below is by a french student, it may contains errors, please report them to me if you see one.

In this wiki, you will get all the informations needed to install and run properly the Minecraft Mod Swapper.
Everything may not be explained so, if you need more informations about a specific topic, let me know, I will see what I can do.
The mod swapper only works on window because of displaying incompatibilities

## Downloads

To download the python version of the mod swapper, follow [this link](https://github.com/Navee82/Minecraft-mod-swapper/blob/main/mod_swapper.py) and click on the "dowlnload raw file" button :

![](https://i.postimg.cc/PfbyPwLx/Download-button.png)

The python file is always on the latest update but may require some installations and files modifications to run properly. Also it may contain bugs, since I upload the pythons file first, without being aware of bugs.

To download the executable (.exe) file, follow [this link](https://github.com/Navee82/Minecraft-mod-swapper/releases) (the release tab) and download the latest file version.
The exe file is slower to update because I work mainly on the python file to add features and fix bugs.

Lastly, you will need a language file. The languages files are located [here.](https://github.com/Navee82/Minecraft-mod-swapper/tree/main/messages) To download a language file, it is the same method as downloading the python file.

## Installation

Once you downloaded the file, put it in a dedicated folder, this folder should be the root of the modswapper arborescence. Like this :

![](https://i.postimg.cc/dVTcM613/Mod-Swapper-arborescence.png)

Do the same for the .exe file.

The directory of the language file does not really matter but i recommend putting it in the same directory as the other files.

**If you are using the python file, you need the current dependencies :**
- [Tkinter](https://docs.python.org/3/library/tkinter.html), install using ``pip install tk`` in a terminal.
- [PyYaml](https://pypi.org/project/PyYAML/), install using ``pip install PyYAML`` in a terminal.
- [Requests](https://pypi.org/project/requests/), install using ``pip install requests`` in a terminal.


## The program itself
### First startup
If you use the Minecraft Mod Swapper for the first time, the program will create a config file, located on the same directory as the pogram. This config basically contains everything the program needs to remember, please do not delete it or modify it unless you know what you are doing.

The program will ask you for your language file, select the one you downloaded earlier.

After that, it will ask you for your .minecraft folder, select yours and make sure you have the "mods" folder inside.

### Main console
The main console looks like this :

![](https://i.postimg.cc/sx662pQ0/main-console.png)

To navigate, simply input the number corresponding to the option you want and press enter.

### Swap profiles
This section is pretty self-explanatory, it allows you to activate the profile you want by entering its name.

### Manage profile
This section has varions options :
- Create a profile
- Import a profile from a folder
- Rename an existing profile
- Delete an existing profile
- Verify the profiles to avoid ghosts profiles

### Settings
The settings allows ou to :
- Completely reset the config, basically going back to the first startup section
- Change your .minecraft folder path
- Turn ON/OFF the transfer details:
  - ON : every mod swapped is displayed in the console
  - OFF : only the numbers of mods swapped is displayed
- Change your language file
- Turn ON/OFF the auto update

### Save
save the config values, if not done before exiting, everything done will be forgotten by the program

### Quit the program
Quit the program (Does not auto save the config !)

## More
If you need some help because something is not working, contact me, I'll be glad to help you !