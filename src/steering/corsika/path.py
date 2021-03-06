import os
import glob

from .. import get_install_path
import src.utils
log = src.utils.getLogger(__name__)


# setup path and runpath
try:
    search_expr = os.path.join(get_install_path(), "corsika-*")
    corsika_paths = glob.glob(search_expr)
    corsika_paths.sort()
    corsika_path = corsika_paths[-1]
except:
    corsika_path = None
    log.warning("cannot find any corsika version")

def get_path():
    """Return CORSIKA base install path.

    Returns
    -------
    path : str
        Path to the CORSIKA install directory (e.g. /.../install/corsika-*)
    """
    return corsika_path

def get_run_path():
    """Return CORSIKA run directory path.

    Returns
    -------
    path : str
        Path to the CORSIKA run directory (e.g. /.../install/corsika-*/run)
    """
    return os.path.join(get_path(), "run")

def set_version(version):
    """Set CORSIKA version.

    If there are several CORSIKA versions inside /.../install, this function
    sets the currently used one. By default the latest version is used. Also
    performs checks if the version is installed.

    Paramters
    ---------
    version : str
        Version string such that /.../install/corsika-version is a valid path.
    """
    global corsika_path
    newpath = os.path.join(get_install_path(), "corsika-" + version)
    if os.path.isdir(newpath):
        corsika_path = newpath
        try:
            binary = os.path.split(get_binary())[-1].split("_", 1)[-1]
            set_binary(binary)
        except RuntimeError:
            log.warning(f"cannot find corresponding binary for new corsika version {version}")
    else:
        raise RuntimeError(f"cannot find version corsika-{version}")


# setup binary path
try:
    search_expr = os.path.join(get_run_path(), "corsika*Linux_*")
    corsika_filenames = glob.glob(search_expr)
    corsika_filenames.sort()
    corsika_filename = corsika_filenames[-1]
except:
    corsika_path = None
    log.warning("cannot find any corsika binary")

def get_binary():
    """Return CORSIKA binary path.

    Returns
    -------
    path : str
        Path to the CORSIKA binary inside /.../install/corsika-*/run.
    """
    runpath = get_run_path()
    return os.path.join(runpath, corsika_filename)

def set_binary(binary):
    """Set the CORSIKA binary.

    Because CORSIKA can be compiled with different options, this function
    enables the selection of a specific binary inside the run directory. One
    can either give a full path, full name or part of the binary name.
    Glob autocompletion is used to identify a binary. If there is more than
    one possible candidate, the last one in a sorted list is used (i.e. the
    alphanumerical last one). Checks are done if a given binary exists.

    Parameters
    ----------
    binary : str
        Either
            1) Full path to the binary
            2) Full name of the binary
            3) Part of the name where globbing is done on corsika*Linux-*part*
    """
    global corsika_filename
    binary = os.path.split(binary)[-1]

    if os.path.isfile(os.path.join(get_run_path(), binary)):
        corsika_filename = os.path.join(get_run_path(), binary)
        return

    search_expr = os.path.join(get_run_path(), "corsika*Linux_*" + binary + "*")
    corsika_filenames = glob.glob(search_expr)
    corsika_filenames.sort()
    if len(corsika_filenames) > 0:
        corsika_filename = corsika_filenames[-1]
        return
    
    raise RuntimeError(f"cannot find corsika binary {binary}")

