import numpy as np
import time_series_utils as tsu


# global constants
#TODO: read them from the config file

NOISE_EPOCH = 0.0015
PRESTIM_STABILITY_EPOCH = 0.5
POSTSTIM_STABILITY_EPOCH = 0.5
LONG_RESPONSE_DURATION = 5  # this will count long ramps as completed


def get_last_vm_epoch(idx1, hz):
    """
    Get epoch lasting LAST_STABILITY_EPOCH before the end of recording

    Parameters
    ----------
    idx1
    hz

    Returns
    -------

    """
    return idx1-int(POSTSTIM_STABILITY_EPOCH * hz), idx1


def get_first_vm_noise_epoch(idx, hz):

    return idx, idx + int(NOISE_EPOCH * hz)


def get_last_vm_noise_epoch(idx1, hz):

    return idx1-int(NOISE_EPOCH * hz), idx1


def get_stability_vm_epoch(stim_start, hz):
    num_steps = int(PRESTIM_STABILITY_EPOCH * hz)
    if num_steps > stim_start-1:
        num_steps = stim_start-1
    elif num_steps <= 0:
        return 0, 0
    assert num_steps > 0, "Number of steps should be a positive integer"

    return stim_start-1-num_steps, stim_start-1


def get_recording_end_idx(v):

    end_idx = np.nonzero(v)[0][-1]  # last non-zero index along the only dimension=0.
    return end_idx

def get_sweep_epoch(response):

    sweep_end_idx = np.nonzero(response)[0][-1]  # last non-zero index along the only dimension=0.

    return (0, sweep_end_idx)

def get_experiment_epoch(i,v,hz):
    """
    Find index range for the experiment epoch.
    The start index of the experiment epoch is defined as stim_start_idx - PRESTIM_DURATION*sampling_rate
    The end is defined by the last nonzero response.


    Parameters
    ----------
    i : stimulus
    v : response
    hz: sampling rate

    Returns
    -------
    start and end indices

    """
    # TODO: deal with non iclamp sweeps and non experimental sweeps
    di = np.diff(i)
    diff_idx = np.flatnonzero(di)  # != 0)

    if len(diff_idx) == 0:
        raise ValueError("Empty stimulus trace")
    if len(diff_idx) >= 4:
        idx = 2  # skip the first up/down assuming that there is a test pulse
    else:
        idx = 0

    stim_start_idx = diff_idx[idx] + 1  # shift by one to compensate for diff()
    expt_start_idx = stim_start_idx - int(PRESTIM_STABILITY_EPOCH * hz)
    #       Recording ends when zeros start
    expt_end_idx = np.nonzero(v)[0][-1]  # last non-zero index along the only dimension=0.

    return expt_start_idx,expt_end_idx


def find_stim_window(stim, idx0=0):
    """
    Find the index of the first nonzero positive or negative jump in an array and the number of timesteps until the last such jump.

    Parameters
    ----------
    stim: np.ndarray
        Array to be searched

    idx0: int
        Start searching with this index (default: 0).

    Returns
    -------
    start_index, duration
    """

    di = np.diff(stim)
    idxs = np.flatnonzero(di)
    idxs = idxs[idxs >= idx0]

    if len(idxs) == 0:
        return -1, 0

    stim_start = idxs[0]+1

    if len(idxs) == 1:
        return stim_start, len(stim)-stim_start

    stim_end = idxs[-1]+1

    return stim_start, stim_end - stim_start

