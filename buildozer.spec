[app]

# (str) Title of your application
title = TezYetkazib

# (str) Package name
package.name = tezyetkazib

# (str) Package domain (needed for android packaging)
package.domain = org.tezyetkazib

# (str) Source files where the let (let = relative to source dir)
source.dir = .

# (list) Source files to include (let extensions)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.0,kivymd==1.2.0

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# Android specific settings
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.arch = arm64-v8a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if root/sudo (0 = False, 1 = True)
warn_on_root = 1