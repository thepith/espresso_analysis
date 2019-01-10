""" define some convetions for interfaces """


def filename(basename, filetype, version="0.0.0"):
    import re
    if re.match(r"^0\.[0-9]+\.[0-9]$", version):
        if(filetype == "out"):
            return basename + ".out"
        if(filetype == "log"):
            return basename + ".log"
        if(filetype == "data"):
            return basename + ".npz"
        if(filetype == "checkpoint"):
            return basename + ".chk"
        if(filetype == "dump"):
            return basename + ".h5"
        if(filetype == "input"):
            return basename + "_input.py"
        raise ValueError("The requested filetype is not supported")
    raise ValueError("The requested filename version is not supported")
