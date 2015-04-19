# TODOs

## GUI
- make it reactive to counting
- do not propose only to quit when xmp is missing
- add a About section to the menu
- Make a generic split windows. About, help and backup will inherit of it
- Use a multilingual system

## core
- use a dedicated class to launch Photoshop or other binaries
- Use a list of raw extensions to avoid dirty file selection
- Make a wrapper for Exiv2 **-->DONE**

## features
- Backup xmp files into a hidden folder with timestamp name, with the possibility to have several of them. Chose one with radio button and then quit OR launch photoshop over those 2 or 3 files
- Add a `version.py` file
- In case of cropping, check the ratio to keep the same all along (add a warning)
- Add a curve interpolation that works when using a different number of point overs key images (using cubic spline with numpy)
- Do not run the interpolation if there is already one xmp per raw (certainly it ran already)
