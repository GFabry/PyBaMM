"""
SimulationAdvanced - Simulation class with per-step dt_max support.

Usage:
    import pybamm

    exp = pybamm.ExperimentAdvanced([
        pybamm.steps_dt.current(-1, dt_max=0.1, duration=400),
        pybamm.steps_dt.voltage(4.2, dt_max=1, termination="C/20"),
    ])

    model = pybamm.lithium_ion.SPM()
    sim = pybamm.SimulationAdvanced(model, experiment=exp)
    sim.solve()
"""

import pybamm
from pybamm.simulation import Simulation


class SimulationAdvanced(Simulation):
    """
    Simulation class that supports per-step dt_max.

    Use with ExperimentAdvanced and steps created via pybamm.steps_dt.

    Parameters
    ----------
    Same as pybamm.Simulation
    """

    def build_for_experiment(
        self, initial_soc=None, direction=None, inputs=None, solve_kwargs=None
    ):
        """
        Build models and solvers for experiment, applying per-step dt_max.
        """
        if initial_soc is not None:
            self.set_initial_state(initial_soc, direction=direction, inputs=inputs)

        if self.steps_to_built_models:
            self._update_experiment_models_for_capacity(solve_kwargs)
            return
        else:
            self._set_up_and_parameterise_experiment(solve_kwargs)

            self._parameter_values.process_geometry(self._geometry)
            self._mesh = pybamm.Mesh(self._geometry, self._submesh_types, self._var_pts)
            self._disc = pybamm.Discretisation(
                self._mesh, self._spatial_methods, **self._discretisation_kwargs
            )

            # Build mapping from basic_repr to step object (to access dt_max)
            step_repr_to_step = {
                step.basic_repr(): step for step in self.experiment.unique_steps
            }

            # Process all the different models
            self.steps_to_built_models = {}
            self.steps_to_built_solvers = {}
            for (
                step_repr,
                model_with_set_params,
            ) in self.experiment_unique_steps_to_model.items():
                built_model = self._disc.process_model(
                    model_with_set_params,
                    inplace=True,
                    delayed_variable_processing=True,
                )
                solver = self._solver.copy()

                # Apply dt_max from step to solver options
                if step_repr in step_repr_to_step:
                    step = step_repr_to_step[step_repr]
                    if hasattr(step, 'dt_max') and step.dt_max is not None:
                        # Copy _options dict to avoid shared reference
                        solver._options = solver._options.copy()
                        solver._options['dt_max'] = step.dt_max

                self.steps_to_built_solvers[step_repr] = solver
                self.steps_to_built_models[step_repr] = built_model

            self._built_nominal_capacity = self._parameter_values.get(
                "Nominal cell capacity [A.h]", None
            )
