from .interim import clear_run as clear_interim
from .processed import clear_run as clear_processed


def clear_run(run):
    """Remove all derived data files (not raw).

    Parameters
    ----------
    run : str
        Name of the subfolder in data/interim and data/processed.
        Accepts glob expressions.
    """
    clear_interim(run)
    clear_processed(run)

