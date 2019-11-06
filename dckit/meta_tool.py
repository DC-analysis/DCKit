import numpy as np

import dclab
from shapeout import meta_tool

from shapeout.meta_tool import find_data  # noqa: F401


def get_date(path):
    with dclab.new_dataset(path) as ds:
        date = ds.config["experiment"]["date"]
    return date


def get_sample_name(path):
    sample = meta_tool.get_sample_name(path)
    if isinstance(sample, bytes):
        if isinstance(sample, bytes):
            sample = sample.decode("utf-8")
    return sample


def get_run_index(path):
    try:
        ridx = meta_tool.get_run_index(path)
    except BaseException:
        ridx = -1
    return ridx


def get_flow_rate(path):
    try:
        flr = meta_tool.get_flow_rate(path)
    except BaseException:
        flr = np.nan
    return flr


def get_event_count(path):
    try:
        ec = meta_tool.get_event_count(path)
    except BaseException:  # meta-tool Python2/3 issue
        # get event count using dclab (slower)
        with dclab.new_dataset(path) as ds:
            ec = ds.config["experiment"]["event count"]
    return ec
