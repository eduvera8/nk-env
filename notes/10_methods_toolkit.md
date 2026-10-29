# Module 10: The computational toolkit for a sophisticated NK paper

> **Goal:** know which tool solves which problem, so that your model choice is not limited by your tools.

| Task | Tool | Notes |
|---|---|---|
| First/second/third-order perturbation, IRFs, moments | **Dynare** (MATLAB or free Octave) | the lingua franca; referees can run your `.mod` |
| Bayesian estimation | Dynare `estimation` | Kalman filter; MH or SMC |
| Ramsey / discretion / optimal simple rules | Dynare `ramsey_model`, `discretionary_policy`, `osr` | Module 3 |
| ZLB and other occasionally binding constraints | Dynare **OccBin** | piecewise linear |
| Deterministic transitions (e.g. a carbon price path to 2050) | Dynare `perfect_foresight_solver` | exact nonlinear, no uncertainty |
| HANK | **sequence-jacobian** (Python) | estimation also possible |
| Global solutions | Python/Julia: time iteration, projection, endogenous grid | small models, strong nonlinearities |
| Empirical IRFs to validate the model | local projections (Jordà 2005, *AER*), SVARs, external instruments | e.g. Känzig's carbon-policy surprise series |

This repo contains:

* `code/solver.py`: a ~100-line perturbation solver (steady state, numerical Jacobians, QZ, Blanchard–Kahn). Read it once
  so that Dynare is never a black box.
* `code/nk3.py`, `code/enk.py`: the models of Modules 1 and 11.
* `dynare/etank.mod`: the same E-TANK model in Dynare, with macro flags for regime, HtM share and rebate design.
  **Verified to reproduce the Python IRFs to 6 decimal places.** Run with
  `octave --eval "addpath /usr/lib/dynare/matlab; dynare etank.mod -DCAP=1 -DLAM=0.3"`.

## Two distinctions that matter in environmental macro

1. **Fluctuations vs. transitions.** Business-cycle E-DSGE (how should emissions policy respond to the cycle?) uses
   stochastic perturbation around a steady state. Transition questions (what does a rising carbon price path do to
   inflation over 2025–2050?) need **deterministic or perfect-foresight paths** and possibly a moving steady state.
   Many good papers do both: a perfect-foresight transition plus stochastic shocks around it.
2. **Linear vs. nonlinear.** Welfare rankings need second order. Large carbon-price changes, the ZLB, and state-dependent
   pricing need nonlinear methods. A 10% carbon-tax shock in a linear model is fine; a carbon price going from 0 to 150
   €/t is not a "small" shock.

## Calibration sources for environmental parameters

* Abatement cost $\theta_1 U^{\theta_2}$: DICE (Nordhaus), $\theta_2 = 2.6$–$2.8$.
* Pollution decay and damages: Heutel (2012) quarterly calibration; for climate, use carbon-cycle and temperature blocks (DICE,
  or Golosov et al. 2014's simple linear carbon-depreciation structure).
* Emission intensity and its cyclicality: Doda (2014) and Heutel (2012) estimate an elasticity of emissions to GDP below 1 for the US.
* Carbon prices: EU ETS futures; Känzig's carbon-policy surprise series for identification.
