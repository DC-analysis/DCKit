def main(splash=True):
    import os
    import pkg_resources
    import sys
    import time

    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QEventLoop

    app = QApplication(sys.argv)
    imdir = pkg_resources.resource_filename("dckit", "img")

    if splash:
        from PyQt5.QtWidgets import QSplashScreen
        from PyQt5.QtGui import QPixmap
        splash_path = os.path.join(imdir, "splash.png")
        splash_pix = QPixmap(splash_path)
        splash = QSplashScreen(splash_pix)
        splash.setMask(splash_pix.mask())
        splash.show()
        # make sure Qt really displays the splash screen
        time.sleep(.07)
        app.processEvents(QEventLoop.AllEvents, 300)

    from PyQt5 import QtCore, QtGui
    from .main import DCKit

    # Set Application Icon
    icon_path = os.path.join(imdir, "icon.png")
    app.setWindowIcon(QtGui.QIcon(icon_path))

    # Use dots as decimal separators
    QtCore.QLocale.setDefault(QtCore.QLocale(QtCore.QLocale.C))

    window = DCKit()

    if splash:
        splash.finish(window)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
