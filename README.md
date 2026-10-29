# nk-env: New Keynesian macro, from the canonical model to environmental applications

A self-study course written for someone who knows the basics (DSGE, Calvo) and wants to reach the research
frontier (TANK/HANK, financial accelerator, ZLB, open economy, menu costs, behavioral NK) in order to
**write a paper applying a sophisticated NK model to an environmental question**.

Every module ends with **environmental angles**: open questions where that frontier piece meets climate/environmental policy.
The code builds up to an environmental TANK model in Python *and* Dynare (cross-validated).

## Map

| # | Module | Key idea | Env-econ hook |
|---|---|---|---|
| 1 | [Canonical NK](notes/01_canonical_nk.md) | NKPC, DIS, divine coincidence, Taylor principle, QZ solution | is a carbon tax a cost-push shock? |
| 2 | [Medium-scale & estimation](notes/02_medium_scale_and_estimation.md) | CEE/SW frictions, Bayesian estimation, pruning, perfect foresight | sticky wages decide who bears carbon costs |
| 3 | [Optimal policy](notes/03_optimal_policy.md) | discretion vs commitment, Ramsey with many instruments | Nakov–Thomas: Tinbergen in climate + monetary policy |
| 4 | [Zero lower bound](notes/04_zero_lower_bound.md) | liquidity traps, paradoxes, OccBin | carbon tax at the ZLB; ETS as automatic stabilizer |
| 5 | [Financial frictions](notes/05_financial_frictions.md) | BGG, Gertler–Karadi, Kiyotaki–Moore | transition risk, green QE, green macroprudential |
| 6 | [Open economy](notes/06_open_economy.md) | Galí–Monacelli, PCP/LCP/DCP | energy imports, CBAM, leakage |
| 7 | [TANK / THANK / HANK](notes/07_tank_hank.md) | χ, compounding/discounting, sequence-space Jacobian | unequal effects of carbon pricing, revenue recycling |
| 8 | [Price setting](notes/08_price_setting_menu_costs.md) | menu costs, selection, multisector/networks | greenflation, which inflation to target |
| 9 | [Behavioral NK](notes/09_behavioral_expectations.md) | cognitive discounting, level-k, learning | credibility of carbon-price paths, salience |
| 10 | [Methods toolkit](notes/10_methods_toolkit.md) | which tool for which problem | fluctuations vs transitions |
| 11 | [Environmental NK](notes/11_environmental_nk.md) | how the environment enters (4 blocks, physical vs transition risk, 5 channels), literature map, the E-TANK model | the core of your paper |
| 12 | [From model to paper](notes/12_from_model_to_paper.md) | candidate questions, workflow, skeleton | — |

## Suggested schedule (~14 weeks, part-time)

| Weeks | Do |
|---|---|
| 1–2 | Module 1 with Galí ch. 3–5: derive everything by hand, run `code/nk3.py`, do the exercises |
| 3 | Modules 3 + 11 (first pass): read the Annicchiarico–Carattini–Fischer–Heutel primer and Annicchiarico–Di Dio (2015); run `code/enk.py` |
| 4 | Module 2 + 10: install Dynare, run `dynare/etank.mod`, learn `stoch_simul`, `perfect_foresight_solver` |
| 5–6 | Module 7 (TANK/HANK): Bilbiie's papers, KMV; install `sequence-jacobian` and run its notebooks |
| 7 | Module 4 (ZLB) + OccBin |
| 8 | Module 5 (financial frictions) |
| 9 | Module 6 (open economy) |
| 10 | Modules 8 + 9 (pricing, behavioral) |
| 11–12 | Module 12: pick the question, write the 1-page literature memo, build the simple model |
| 13–14 | First quantitative results; draft introduction |

Modules 4–9 are independent; reorder them toward the question you are converging on.
If you already know you want, say, HANK + carbon tax, do 1 → 3 → 11 → 7 → 10 → 12 and skim the rest.

## Code

```
code/solver.py   # ~100-line perturbation solver: steady state, Jacobians, QZ, Blanchard–Kahn, IRFs, simulation
code/nk3.py      # Module 1: 3-equation NK model, IRFs, Taylor-principle check
code/enk.py      # Module 11: E-TANK (Calvo, HtM households, abatement, pollution, tax vs cap, revenue recycling)
dynare/etank.mod # same E-TANK in Dynare, with macro flags for regime / HtM share / rebate
figures/         # output of the scripts
```

Run (Python ≥ 3.10, numpy, scipy, matplotlib):

```bash
pip install numpy scipy matplotlib
```

```bash
python code/nk3.py
```

```bash
python code/enk.py
```

Dynare (≥ 5, MATLAB or Octave), from `dynare/`:

```bash
octave --no-gui --eval "addpath /usr/lib/dynare/matlab; dynare etank.mod -DCAP=1 -DLAM=0.3 -DREBATE=2"
```

The Python and Dynare versions produce identical impulse responses (checked for tax/RANK, cap/RANK and TANK with HtM rebate).

## Core textbooks

* Galí (2015), *Monetary Policy, Inflation, and the Business Cycle*, 2nd ed.: the spine of this course.
* Woodford (2003), *Interest and Prices*: depth on optimal policy.
* Herbst & Schorfheide (2015), *Bayesian Estimation of DSGE Models*.
* Annicchiarico, Carattini, Fischer & Heutel (2022), "Business cycles and environmental policy: a primer": read early.

References in the notes were written from memory and spot-checked. Confirm journal/year before citing.
