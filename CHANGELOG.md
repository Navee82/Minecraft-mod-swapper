# Changelog

All notable changes to this project will be documented in this file.

The format is inspired from [Keep a Changelog](https://keepachangelog.com).

🟩 stands for added<br>
🟦 stands for changed<br>
🟥 stands for removed<br>
🟪 stands for fixed<br>
🟧 stands for work in progress<br>


## [v1.1.2] - Unreleased

### **General**

**Added**
- 🟩 Added the possibility to cancel actions by typing "CANCEL".
- 🟩 Added a dependency check, to prevent the program to instantly close if something is missing

**Changed**
- 🟦 Changed the normalisation of path case, now using ``os.path.normcase()`` instead of ``path.replace("\\","/")``

**Removed**
- 🟥 Removed the RELEASE variable and the release check in the get_latest_version() function since it has no sense to keep it in the python file.

### **Settings**

**Changed**
- 🟦 Changed the way renaming profiles was handeled. Does not affect the UX.

**Fixed**
- 🟪 Fixed a non translated message in the renaming process, added it to the language file.
<br>

## [v1.1.1] - 05/18/24

### **General**

**Fixed**
- 🟪 Fixed an auto config update error, version was updated to 1.0.6 instead of 1.1.0

<br>

## [v1.1.0] - 05/15/24

### **General**

**Added**
- 🟩 New dependency : requests
- 🟩 Auto file update feature
- 🟩 Auto config update feature
- 🟩 Added credits at the end of the file

**Changed**
- 🟦 All loop-related variables are now identifiables by their name (loop_variable_name)
- 🟦 Supported language version is 1.1.0

**Fixed**
- 🟪 Fixed a bug when importing a wrong language file

### **Language files**

**Added**
- 🟩 Added 20 messages

**Changed**
- 🟦 Languages files version is now 1.1.0

### **Profiles swap**

**Changed**
- 🟩 other files than .jar files are not longer moved by the mod swapper

### **Profiles gestion**

**Added**
- 🟩 New profiles can now be imported via folders

### **Settings**

**Added**
- 🟩 Users can now change their language file
- 🟩 Auto update can be turned on/off