# If you change this version, change it also in docs/conf.py
# Packging guide: http://guide.python-distribute.org/quickstart.html
__version_info__ = {
    "major": 1,
    "minor": 0,
    "micro": 0,
    "releaselevel": "final",
    "serial": 0,
}


def get_version():
    vers = ["{major}.{minor}".format(**__version_info__)]

    if __version_info__["micro"]:
        vers.append(".{micro}".format(**__version_info__))
    if __version_info__["releaselevel"] != "final":
        vers.append("{releaselevel}{serial}".format(**__version_info__))
    return "".join(vers)


__version__ = get_version()
