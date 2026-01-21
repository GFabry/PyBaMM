"""
Step functions with dt_max support.

These functions wrap PyBaMM's step classes and add a dt_max attribute
for per-step maximum timestep control.

Usage:
    import pybamm_extensions.steps_dt as step_dt

    exp = ExperimentAdvanced([
        step_dt.current(-1, dt_max=0.1, duration=400),
        step_dt.voltage(4.2, dt_max=1, termination="C/20"),
    ])
"""

import pybamm


def _add_dt_max(step, dt_max):
    """Add dt_max attribute to a step object."""
    step.dt_max = dt_max
    return step


def current(value, dt_max, **kwargs):
    """
    Current-controlled step with dt_max.

    Parameters
    ----------
    value : float
        Current in A. Positive for discharge, negative for charge.
    dt_max : float
        Maximum timestep in seconds.
    **kwargs
        Passed to pybamm.step.Current (duration, termination, period, etc.)

    Returns
    -------
    pybamm.step.Current with dt_max attribute
    """
    step = pybamm.step.Current(value, **kwargs)
    return _add_dt_max(step, dt_max)


def c_rate(value, dt_max, **kwargs):
    """
    C-rate-controlled step with dt_max.

    Parameters
    ----------
    value : float
        C-rate. Positive for discharge, negative for charge.
    dt_max : float
        Maximum timestep in seconds.
    **kwargs
        Passed to pybamm.step.CRate (duration, termination, period, etc.)

    Returns
    -------
    pybamm.step.CRate with dt_max attribute
    """
    step = pybamm.step.CRate(value, **kwargs)
    return _add_dt_max(step, dt_max)


def voltage(value, dt_max, **kwargs):
    """
    Voltage-controlled step with dt_max.

    Parameters
    ----------
    value : float
        Voltage in V.
    dt_max : float
        Maximum timestep in seconds.
    **kwargs
        Passed to pybamm.step.Voltage (duration, termination, period, etc.)

    Returns
    -------
    pybamm.step.Voltage with dt_max attribute
    """
    step = pybamm.step.Voltage(value, **kwargs)
    return _add_dt_max(step, dt_max)


def power(value, dt_max, **kwargs):
    """
    Power-controlled step with dt_max.

    Parameters
    ----------
    value : float
        Power in W. Positive for discharge, negative for charge.
    dt_max : float
        Maximum timestep in seconds.
    **kwargs
        Passed to pybamm.step.Power (duration, termination, period, etc.)

    Returns
    -------
    pybamm.step.Power with dt_max attribute
    """
    step = pybamm.step.Power(value, **kwargs)
    return _add_dt_max(step, dt_max)


def resistance(value, dt_max, **kwargs):
    """
    Resistance-controlled step with dt_max.

    Parameters
    ----------
    value : float
        Resistance in Ohm.
    dt_max : float
        Maximum timestep in seconds.
    **kwargs
        Passed to pybamm.step.Resistance (duration, termination, period, etc.)

    Returns
    -------
    pybamm.step.Resistance with dt_max attribute
    """
    step = pybamm.step.Resistance(value, **kwargs)
    return _add_dt_max(step, dt_max)


def rest(dt_max, **kwargs):
    """
    Rest step with dt_max.

    Parameters
    ----------
    dt_max : float
        Maximum timestep in seconds.
    **kwargs
        Passed to pybamm.step.Current (duration, termination, period, etc.)

    Returns
    -------
    pybamm.step.Current (value=0) with dt_max attribute
    """
    step = pybamm.step.Current(0, **kwargs)
    return _add_dt_max(step, dt_max)
