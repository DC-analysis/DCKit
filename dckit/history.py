import json
import pathlib

import dclab
import h5py


def append_history(path, hdict):
    """Append DCKit history to an .rtdc file

    Parameters
    ----------
    path: str or pathlib.Path
        Path to .rtdc file
    hdict_element: dict
        History element (not the full history)
    """
    path = pathlib.Path(path)
    hlist = read_history(path)
    hlist.append(hdict)
    write_history(path, hlist)


def read_history(path):
    """Read DCKit history from an .rtdc file

    Parameters
    ----------
    path: str or pathlib.Path
        Path to .rtdc file

    Returns
    -------
    hlist: list of dicts
        Full history (containing history elements)
    """
    path = pathlib.Path(path)
    with dclab.new_dataset(path) as ds:
        if "dckit-history" in ds.logs:
            hdump = ds.logs["dckit-history"]
            hlist = json.loads("\n".join(hdump))
        else:
            hlist = []
    return hlist


def write_history(path, hlist):
    """Write DCKit history to .rtdc file

    Parameters
    ----------
    path: str or pathlib.Path
        Path to .rtdc file
    hlist: list of dicts
        Full history (containing history elements)
    """
    path = pathlib.Path(path)
    # remove previous log
    with h5py.File(path) as h5:
        if "dckit-history" in h5["logs"]:
            del h5["logs"]["dckit-history"]
    # dump json log
    hlog = json.dumps(hlist, sort_keys=True, indent=2).split("\n")
    # write dump as log
    with dclab.rtdc_dataset.write(
            path_or_h5file=path,
            logs={"dckit-history": hlog},
            mode="append",
            compression="gzip"):
        pass
