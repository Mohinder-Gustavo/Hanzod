[app]

# (str) Title of your application
title = Hanzod

# (str) Package name
package.name = hanzod

# (str) Package domain (needed for android packaging)
package.domain = org.astroapp

# (str) VIERAM FALTANDO ESTAS LINHAS:
version = 0.1

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf,otf,json

# (list) Application requirements
# Incluímos o lunardate e o kivy
requirements = python3,kivy==2.3.0,lunardate

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# Para salvar o JSON internamente, geralmente não precisa de permissão extra
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Android API to use
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk build-tools
android.skip_update = False

# (bool) If True, then automatically accept SDK license
# Isso é importante para o GitHub Actions não travar
android.accept_sdk_license = True

# (str) The format used to package the app for release mode (aab or apk)
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aar)
android.debug_artifact = apk

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1