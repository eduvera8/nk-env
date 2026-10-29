# Module 7: Heterogeneous agents — TANK, THANK and HANK

> **Goal:** understand *why* heterogeneity changes aggregate NK dynamics (it is not just about
> distribution), solve TANK on paper, understand the sequence-space approach to HANK, and see why
> carbon pricing is a prime HANK application.

**TANK:** Galí, López-Salido & Vallés (2007, *JEEA*); Bilbiie (2008, *JET*), "Limited asset markets participation, monetary policy
and (inverted) aggregate demand logic"; Bilbiie (2020, *JME*), "The New Keynesian cross".
**THANK:** Bilbiie, "Monetary policy and heterogeneity: an analytical framework" (*REStud*).
**HANK:** Kaplan, Moll & Violante (2018, *AER*), "Monetary policy according to HANK"; McKay, Nakamura & Steinsson (2016, *AER*);
Auclert (2019, *AER*), "Monetary policy and the redistribution channel".
**Methods:** Auclert, Bardóczy, Rognlie & Straub (2021, *Econometrica*), "Using the sequence-space Jacobian to solve and estimate
heterogeneous-agent models" (Python package `sequence-jacobian`); Auclert, Rognlie & Straub, "The intertemporal Keynesian cross".

---

## 7.1 TANK on paper

A share $\lambda$ of households are hand-to-mouth (HtM): $C^H_t = \text{income}_t$. Let $\chi$ be the elasticity of
HtM income to aggregate income: $c^H_t = \chi y_t$. Savers obey the Euler equation. Aggregating
$y_t = \lambda c^H_t + (1-\lambda)c^S_t$:

$$
\boxed{\;y_t = E_t y_{t+1} - \frac{1-\lambda}{1-\lambda\chi}\cdot\frac{1}{\sigma}\left(i_t - E_t\pi_{t+1} - r^n_t\right)\;}
$$

* $\chi > 1$ (HtM income more cyclical than average, e.g. profits not distributed to them, sticky wages): **amplification**.
* $\chi < 1$: dampening. $\lambda\chi > 1$: the IS curve flips sign, the "inverted aggregate demand logic" (Bilbiie 2008), and the Taylor principle changes.
* The value of $\chi$ depends on **how profits and transfers are distributed**, which is exactly where revenue recycling of a carbon tax enters.

**What our code shows.** In `code/enk.py` with log utility, endogenous HtM labor supply and uniform rebates,
HtM and saver consumption move almost one-for-one after a carbon-tax shock (see `figures/enk_tax_shock_tank.png`):
the economy is close to $\chi = 1$, so TANK barely changes aggregates. The **rebate design** is what moves the needle:
giving all revenue to HtM turns their consumption response positive while savers bear the cost. To get aggregate
amplification you need a $\chi \neq 1$ mechanism: sticky wages with union-set hours, profit distribution, or
heterogeneous energy shares. That is Exercise 1.

## 7.2 THANK: idiosyncratic risk in two agents

Let savers become HtM with probability $1-s$ each period. Then the aggregate Euler equation becomes
$y_t = \delta E_t y_{t+1} - \zeta(i_t - E_t\pi_{t+1} - r^n_t)$, with $\delta = 1 + (\chi-1)\frac{1-s}{1-\lambda\chi}$.

* $\chi > 1 \Rightarrow \delta > 1$: **compounding** in the aggregate Euler equation. This makes the forward guidance puzzle worse.
* $\chi < 1 \Rightarrow \delta < 1$: **discounting**. This resolves the puzzle, like McKay–Nakamura–Steinsson and Gabaix (Module 9).

THANK reproduces most of the analytical insights of quantitative HANK with pen and paper. Use it for an analytical
section of your paper.

## 7.3 Quantitative HANK

Households face uninsurable income risk and borrowing limits (Aiyagari–Bewley–Huggett), plus (KMV) liquid and
illiquid assets, so many households are **wealthy hand-to-mouth**. Main findings:

* Monetary transmission is mostly **indirect** (general-equilibrium labor income), not intertemporal substitution (KMV).
* What matters for aggregates are **intertemporal MPCs** (iMPCs): how spending at all dates responds to income at all dates.
* Fiscal policy (who receives transfers, how they are financed) matters for aggregate demand, so Ricardian equivalence fails.

## 7.4 The sequence-space method (why HANK is now feasible for a paper)

Write the model as a set of blocks mapping sequences to sequences. Stack the market-clearing conditions as
$H(U, Z) = 0$ with unknown sequences $U$ (e.g. output path) and shocks $Z$. To first order:

$$
dU = -H_U^{-1} H_Z\, dZ,
$$

where the Jacobians of the heterogeneous-household block are computed in one shot by the **fake-news algorithm**.
Example, the **intertemporal Keynesian cross**: with iMPC matrix $\mathbf{M}$,
$d\mathbf{Y} = d\mathbf{G} + \mathbf{M}(d\mathbf{Y} - d\mathbf{T}) \Rightarrow d\mathbf{Y} = (\mathbf{I}-\mathbf{M})^{-1}(d\mathbf{G} - \mathbf{M}\,d\mathbf{T})$.
The `sequence-jacobian` package solves and estimates HANK models in seconds. **Learn it**; it is the most valuable
tool investment for a "sophisticated NK + environment" paper.

## 7.5 Environmental angles (strongest area for a first paper)

* **Evidence.** Känzig (2023, NBER WP 31221), "The unequal economic consequences of carbon pricing": EU ETS carbon-policy
  shocks raise energy prices, cut emissions, reduce activity, and **lower-income households' consumption falls much
  more**, through both energy expenditure shares and **indirect income effects**. He rationalizes it with a model with
  heterogeneous households. This is the empirical anchor for HANK + carbon pricing.
* **Energy shocks in HANK.** Auclert, Monnery, Rognlie & Straub (2023, NBER WP), "Managing an energy shock: fiscal and monetary
  policy"; Pieroni (2023, *European Economic Review*), "Energy shortages and aggregate demand: output loss and unequal burden from HANK";
  Chan, Diz & Kanngiesser (2024, *JME*), Gas-TANK.
* **Open questions:** optimal **revenue recycling** as a stabilization tool (lump-sum vs. targeted vs. labor-tax cuts) in HANK;
  monetary policy response to a carbon tax when MPCs are heterogeneous; non-homothetic energy demand (Stone–Geary);
  who holds the brown capital (Module 5); optimal carbon tax with uninsurable risk.

---

## Exercises
1. Modify `code/enk.py` so that hours are set by a union and rationed equally ($N^H = N^S = N$), and profits go only to
   savers. Compute the implied $\chi$ and show amplification of the carbon-tax shock.
2. Add non-homothetic energy consumption: HtM households spend a larger share on energy, which bears the carbon tax directly.
3. Install `sequence-jacobian`, run its one-asset HANK notebook, then add a carbon tax on a polluting intermediate input and rebate it.
