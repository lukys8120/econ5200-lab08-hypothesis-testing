"""Power analysis helpers for two-group t-tests (ECON 5200, Lab 8)."""

import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.power import TTestIndPower


def compute_power_summary(effect_size, n_obs, alpha=0.05, target_power=0.80, ratio=1.0):
    """Power at n_obs per group, and the n per group that reaches target_power.

    float() and bool() turn NumPy values into plain Python ones, which print plainly.
    """
    assert effect_size > 0, "Effect size must be positive"

    pa = TTestIndPower()
    achieved = pa.solve_power(effect_size=effect_size, nobs1=n_obs, alpha=alpha,
                              ratio=ratio, alternative="two-sided")
    n_required = pa.solve_power(effect_size=effect_size, alpha=alpha, power=target_power,
                                ratio=ratio, alternative="two-sided")

    return {
        "effect_size": effect_size,
        "n_obs": n_obs,
        "alpha": alpha,
        "achieved_power": float(round(achieved, 4)),
        "target_power": target_power,
        "n_required": int(np.ceil(n_required)),      # round up: whole people
        "adequately_powered": bool(achieved >= target_power),
    }


def plot_power_curves(effect_sizes=(0.2, 0.5, 0.8), alpha=0.05, max_n=500,
                      current_n=None, save_path=None):
    """Power against n per group, one line per effect size. Returns the figure."""
    pa = TTestIndPower()
    fig, ax = plt.subplots(figsize=(10, 6))
    sample_sizes = np.arange(10, max_n)

    for d in effect_sizes:
        powers = [pa.solve_power(effect_size=d, nobs1=n, alpha=alpha, ratio=1.0,
                                 alternative="two-sided") for n in sample_sizes]
        ax.plot(sample_sizes, powers, label=f"d={d}")

    ax.axhline(y=0.80, color="gray", linestyle="--", label="80% power")
    if current_n is not None:
        ax.axvline(x=current_n, color="red", linestyle=":", label=f"Current n={current_n}")

    ax.set_xlabel("Sample Size per Group")
    ax.set_ylabel("Statistical Power")
    ax.set_title("Power Curves by Effect Size")
    ax.legend(loc="lower right")
    ax.set_ylim(0, 1.05)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig
