"""Discrete-event simulation process for a single ICU patient."""

from __future__ import annotations

from typing import TYPE_CHECKING

import simpy

from simuci import distributions
from simuci._constants import EXPERIMENT_VARIABLES_LABELS

if TYPE_CHECKING:
    from simuci.experiment import Experiment

# Pre-unpack labels into constants so the hardcoded strings live in one place
_LBL_PRE_VAM: str = EXPERIMENT_VARIABLES_LABELS[0]      # "Tiempo Pre VAM"
_LBL_VAM: str = EXPERIMENT_VARIABLES_LABELS[1]          # "Tiempo VAM"
_LBL_POST_VAM: str = EXPERIMENT_VARIABLES_LABELS[2]     # "Tiempo Post VAM"
_LBL_UCI: str = EXPERIMENT_VARIABLES_LABELS[3]          # "Estadia UCI"
_LBL_POST_UCI: str = EXPERIMENT_VARIABLES_LABELS[4]     # "Estadia Post UCI"


class Simulation:
    """SimPy process that models an ICU patient's journey through VAM stages."""

    def __init__(self, experiment: "Experiment", cluster: int) -> None:
        self.experiment = experiment
        self.cluster = cluster

    def uci(self, env: simpy.Environment):
        """Run the patient through pre-VAM → VAM → post-VAM → post-ICU stages."""

        is_cluster_zero: bool = self.cluster == 0

        post_uci = int(
            distributions.tiemp_postUCI_cluster0() if is_cluster_zero else distributions.tiemp_postUCI_cluster1()
        )
        uci = int(
            distributions.estad_UTI_cluster0() if is_cluster_zero else distributions.estad_UTI_cluster1()
        )

        # Ensure VAM ≤ UCI stay; retry up to 1000 draws then clamp
        for _ in range(1000):
            vam = int(
                distributions.tiemp_VAM_cluster0() if is_cluster_zero else distributions.tiemp_VAM_cluster1()
            )
            if vam <= uci:
                break
        else:
            vam = uci

        pre_vam = int((uci - vam) * self.experiment.porcentaje / 100)
        post_vam = uci - pre_vam - vam

        self.experiment.result[_LBL_PRE_VAM] = pre_vam
        self.experiment.result[_LBL_VAM] = vam
        self.experiment.result[_LBL_POST_VAM] = post_vam
        self.experiment.result[_LBL_UCI] = uci
        self.experiment.result[_LBL_POST_UCI] = post_uci

        yield env.timeout(pre_vam)
        yield env.timeout(vam)
        yield env.timeout(post_vam)
        yield env.timeout(post_uci)
