# Module 11: Environmental New Keynesian models (E-DSGE)

> **Goal:** know the literature map, understand the canonical E-NK model line by line (it is coded
> in `code/enk.py` and `dynare/etank.mod`), and read its results the way a referee would.

## 11.1 Literature map

**Foundations (RBC + environment)**
* Fischer & Springborn (2011, *JEEM*), "Emissions targets and the real business cycle: intensity targets versus caps or taxes".
* Heutel (2012, *RED*), "How should environmental policy respond to business cycles?". Emissions are procyclical (elasticity < 1);
  the optimal policy lets emissions be procyclical, but less than a fixed tax would.
* Angelopoulos, Economides & Philippopoulos (2013), optimal environmental policy under uncertainty.
* Survey you should read first: **Annicchiarico, Carattini, Fischer & Heutel (2022), "Business cycles and environmental policy: a primer",
  *Environmental and Energy Policy and the Economy* 3.**
* Long-run climate macro: Golosov, Hassler, Krusell & Tsyvinski (2014, *Econometrica*); Hassler, Krusell & Smith (2016, *Handbook of Macro*);
  Acemoglu, Aghion, Bursztyn & Hemous (2012, *AER*) on directed technical change; Nordhaus's DICE.

**New Keynesian E-DSGE**
* **Annicchiarico & Di Dio (2015, *JEEM*), "Environmental policy and macroeconomic dynamics in a New Keynesian model"**: tax vs. cap vs.
  intensity target under nominal rigidities; Ramsey policy. *The paper closest to `code/enk.py`.*
* Annicchiarico & Di Dio (2017, *Environmental and Resource Economics*), "GHG emissions control and monetary policy".
* Economides & Xepapadeas (2018, CESifo/Bank of Greece WP), "Monetary policy under climate change".
* Nakov & Thomas (2026, *JPE Macro*), "Climate-conscious monetary policy" (Module 3).
* Del Negro, di Giovanni & Dogra (FRBNY SR 1053), "Is the green transition inflationary?" (Module 8).
* Olovsson & Vestin (2023, Riksbank WP), "Greenflation?".
* Ferrari & Nispi Landi (2022, ECB WP 2726), expectations and the green transition (Module 9).
* Coenen, Lozej & Priftis (2024, *European Economic Review*): carbon transition in the ECB's NAWM with a disaggregated energy sector,
  an example of a policy-institution-scale model.

**Frontier combinations** (Modules 5–9): financial frictions (Carattini, Heutel & Melkadze 2023; Diluiso et al. 2021; Ferrari &
Nispi Landi 2023), open economy (Annicchiarico & Diluiso 2019; Airaudo, Pappa & Seoane), heterogeneity (Känzig 2023; Gas-TANK;
HANK with energy), price setting (Del Negro et al.).

> **Caveat on references:** listed from memory and spot-checked. Before citing, confirm each one's final journal/year
> on Google Scholar/RePEc. Working papers in this field get published fast.

## 11.2 The canonical E-NK model (as coded)

Everything from Module 1, plus:

**Emissions and abatement.** Firm $j$ emits $E_t(j) = \varphi(1-U_t(j))Y_t(j)$ and pays an abatement cost
$\theta_1 U_t(j)^{\theta_2} Y_t(j)$ (DICE form) plus a tax $\tau_t$ per unit of emissions. Cost minimization per unit of output:

$$
\min_U\; \theta_1 U^{\theta_2} + \tau_t\varphi(1-U) \;\Rightarrow\; \theta_1\theta_2 U_t^{\theta_2-1} = \tau_t\varphi .
$$

**Real marginal cost now has an environmental component:**

$$
MC_t = \underbrace{\frac{W_t/P_t}{A_t(1-d(X_t))}}_{\text{labor}} + \underbrace{\theta_1 U_t^{\theta_2}}_{\text{abatement}} + \underbrace{\tau_t\varphi(1-U_t)}_{\text{carbon tax bill}} .
$$

So a carbon-tax increase raises marginal cost and enters the NKPC like a **cost-push** shock, unless it also moves
natural/efficient output by the same amount (Module 3, §3.4).

**Pollution and damages.** $X_t = (1-\delta_X)X_{t-1} + E_t + E^{row}$ and output loss $d(X_t) = 1 - e^{-\gamma_d X_t}$ (Heutel uses a quadratic).
With a domestic share of world emissions of 10% and quarterly decay of 0.21%, $X$ barely moves at business-cycle
frequencies: **damages are a long-run issue; business-cycle E-DSGE is mostly about the cost side.**

**Policy regimes.** *Tax*: $\tau_t = \bar\tau e^{z_t}$. *Cap*: $E_t = \bar E e^{z_t}$, so $\tau_t$ is the endogenous permit price.
**Revenue** $\tau_tE_t$ is rebated lump-sum: uniformly, to HtM only, or to savers only.
**Households**: a share $\lambda$ of HtM (Module 7). **Monetary policy**: Taylor rule.

Calibration (in `BASE` in `code/enk.py`): quarterly, $\beta = 0.99$, $\sigma=\varphi=1$, $\varepsilon = 6$, $\theta = 0.75$,
$\theta_1 = 0.056$, $\theta_2 = 2.8$, steady-state abatement 20%, $\delta_X = 0.0021$, steady-state damages 0.5% of output.

## 11.3 Results (run `python code/enk.py`)

**(a) TFP shock, tax vs. cap** (`figures/enk_tfp_tax_vs_cap.png`)
* Under a **tax**, emissions rise one-for-one with output (procyclical, as in the data).
* Under a **cap**, emissions are fixed, so the **permit price absorbs the shock**: +6% for a 1% TFP shock. In a boom firms
  pay more for permits, and that dampens the boom: the cap is an automatic stabilizer for output but transmits volatility to
  carbon prices. Hours fall more under the cap.
* Volatility (simulated, σ_a = 0.7%): output 2.08% (tax) vs 2.03% (cap); emissions 2.08% vs 0; carbon price 0 vs 14.6%.
  This qualitatively matches Fischer & Springborn and Annicchiarico & Di Dio.

**(b) Carbon tax +10%, RANK vs. TANK and recycling** (`figures/enk_tax_shock_tank.png`)
* Output falls, inflation **rises**, and the central bank raises rates: a cost-push shock. Emissions fall ~1.4%.
* Aggregates barely depend on λ or the rebate (χ ≈ 1 in this baseline, see Module 7). **Distribution** depends a lot on the rebate:
  rebating to HtM makes their consumption rise while savers bear the cost; rebating to savers nearly doubles the HtM loss.
* The rebate to HtM raises aggregate demand a bit, so inflation and rates rise more: recycling design interacts with monetary policy.

**(c) Same shock, different monetary rules** (`figures/enk_tax_shock_monpol.png`)
* Hawkish rules cut the inflation response but deepen the output/HtM consumption loss: the standard cost-push trade-off.

**Magnitudes are small** because the carbon-tax bill is ~0.7% of output in this calibration. Real-world questions
(a path to 100+ €/t, energy as a separate input with low substitutability) need a richer energy block and nonlinear
transitions (Module 10).

## 11.4 What a "sophisticated" version adds (pick 1–2, not all)

1. A separate **energy** input (fossil vs. clean), CES with low short-run substitutability. This is where real inflation effects come from.
2. **Capital** with adjustment costs; green vs. brown capital (transition risk).
3. **Sticky wages** (who absorbs the cost?).
4. **Heterogeneity**: TANK/THANK (analytic) or HANK (quantitative), with non-homothetic energy demand.
5. **Open economy**: imported energy, CBAM, exchange rate.
6. **Financial frictions**: GK banks holding brown assets.
7. **Nonlinearities**: ZLB, state-dependent pricing.
8. **Expectations**: credibility of the announced carbon path.
