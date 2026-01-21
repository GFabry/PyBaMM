"""
ExperimentAdvanced - Experiment class with dt_max support.

Usage:
    import pybamm

    exp = pybamm.ExperimentAdvanced([
        pybamm.steps_dt.current(-1, dt_max=0.1, duration=400),
        pybamm.steps_dt.voltage(4.2, dt_max=1, termination="C/20"),
    ])
"""

from pybamm.experiment.experiment import Experiment


class ExperimentAdvanced(Experiment):
    """
    Experiment class that supports per-step dt_max.

    All steps must have a dt_max attribute. Use pybamm.steps_dt functions
    to create steps with dt_max.

    Parameters
    ----------
    operating_conditions : list
        List of steps created with pybamm.steps_dt functions.
    period : str, optional
        Period at which to record outputs. Default is 1 minute.
    temperature : float or string, optional
        The temperature of the experiment.
    termination : list[str], optional
        Conditions to terminate the experiment.
    """

    @staticmethod
    def process_steps(unprocessed_steps, period, temp):
        """
        Process steps while preserving dt_max attribute.

        Raises ValueError if any step is missing dt_max.
        """
        # First, validate all steps have dt_max
        for i, step in enumerate(unprocessed_steps):
            if not hasattr(step, 'dt_max'):
                raise ValueError(
                    f"Step {i} is missing 'dt_max'. Use pybamm.steps_dt functions."
                )

        # Use parent's process_steps
        processed_steps = Experiment.process_steps(unprocessed_steps, period, temp)

        # Restore dt_max to processed steps
        # processed_steps is a dict: {repr(step): processed_step}
        for original_step in unprocessed_steps:
            key = repr(original_step)
            if key in processed_steps:
                processed_steps[key].dt_max = original_step.dt_max

        return processed_steps

    def copy(self):
        """
        Return a copy of the experiment, preserving dt_max on steps.
        """
        return ExperimentAdvanced(*self.args)
