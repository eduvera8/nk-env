# Module 2: Medium-scale NK models and how they are taken to data

> **Goal:** understand what each "bell and whistle" in Christiano–Eichenbaum–Evans / Smets–Wouters is for,
> so that in your paper you add the frictions your question needs and nothing else.

**Core reading:** Christiano, Eichenbaum & Evans (2005, *JPE*); Smets & Wouters (2007, *AER*);
Erceg, Henderson & Levin (2000, *JME*) for sticky wages.
**Methods:** Herbst & Schorfheide (2015), *Bayesian Estimation of DSGE Models*; An & Schorfheide (2007, *Econometric Reviews*);
Fernández-Villaverde, Rubio-Ramírez & Schorfheide (2016), "Solution and Estimation Methods for DSGE Models", *Handbook of Macro* vol. 2.

---

## 2.1 The empirical target

CEE estimate a monetary VAR and ask a model to match its impulse responses: output and consumption
respond in a **hump shape**, inflation responds **sluggishly** (peaks after 1–2 years), real wages barely
move. The 3-equation model gets none of these: its responses are largest on impact.

## 2.2 Frictions and what each one buys you

| Friction | Equation it changes | What it fixes |
|---|---|---|
| **External habit** $u(C_t - hC_{t-1})$ | Euler becomes backward-looking: $c_t = \frac{h}{1+h}c_{t-1} + \frac{1}{1+h}E_t c_{t+1} - \frac{1-h}{\sigma(1+h)}(i_t - E_t\pi_{t+1})$ | hump-shaped consumption |
| **Capital + investment adjustment costs** $K_{t+1} = (1-\delta)K_t + [1-S(I_t/I_{t-1})]I_t$ | Tobin's $q$ equation | hump-shaped investment; $q$ moves with shocks |
| **Variable capital utilization** | marginal cost less sensitive to output | flatter marginal cost, more persistence |
| **Sticky wages (EHL 2000)**: Calvo on wages set by unions | wage Phillips curve $\pi^w_t = \beta E_t\pi^w_{t+1} + \lambda_w(\text{mrs}_t - w_t)$ | sluggish real wages, sluggish marginal cost, inflation persistence |
| **Indexation** $P_t(j) = P_{t-1}(j)\Pi_{t-1}^{\iota}$ for non-resetters | hybrid NKPC $\pi_t = \frac{\iota}{1+\beta\iota}\pi_{t-1} + \frac{\beta}{1+\beta\iota}E_t\pi_{t+1} + \dots$ | inflation inertia (ad hoc, but it fits) |
| **Monetary rule with smoothing** $i_t = \rho_i i_{t-1} + (1-\rho_i)(\dots)$ | — | realistic rate paths |

Smets–Wouters add seven structural shocks (TFP, investment-specific, risk premium, government spending,
price markup, wage markup, monetary) so the model can be estimated on seven US series.

**Lesson for your paper:** sticky wages matter a lot for any question about **who bears a carbon tax**
(the split between labor income and profits) and about whether a carbon tax is inflationary
(it is if real wages can't absorb the cost increase). Blanchard & Galí (2007, *JMCB*), "Real wage rigidities
and the New Keynesian model", show real-wage rigidity is exactly what breaks divine coincidence after
oil-type shocks. That is directly relevant for energy and carbon-price shocks.

## 2.3 Taking it to data

1. **Calibrate** the steady-state parameters (β, δ, α, great ratios, environmental parameters).
2. **Estimate** the dynamic parameters by Bayesian methods: likelihood from the Kalman filter on the
   linearized state space, priors, MCMC (random-walk Metropolis–Hastings or SMC). In Dynare:
   `varobs`, `estimated_params`, `estimation(...)`.
3. Alternatively, use **impulse-response matching**: choose parameters to match IRFs from an identified VAR
   or local projections. This is attractive for environmental questions because there now exist
   identified **carbon policy shocks** (Känzig 2023, using EU ETS regulatory news; see Module 11).

## 2.4 Beyond first order

* Welfare comparisons need a **second-order** approximation (Schmitt-Grohé & Uribe 2004, *JEDC*):
  first-order solutions are certainty-equivalent, so every policy delivers the same mean welfare.
* Simulating higher-order solutions needs **pruning** (Kim, Kim, Schaumburg & Sims 2008; Andreasen,
  Fernández-Villaverde & Rubio-Ramírez 2018, *REStud*). In Dynare: `stoch_simul(order=2, pruning)`.
* **Deterministic transitions** (perfect foresight, solved with Newton on the stacked system) are what
  you use to study **a green transition**: a known, gradually rising carbon price path. Dynare:
  `perfect_foresight_setup; perfect_foresight_solver;`. This distinction (fluctuations vs. transitions) is
  central in environmental macro, so expect to use both.

---

## Exercises
1. Add external habits to `code/nk3.py` and show the hump-shaped output response to a monetary shock.
2. Add capital with investment adjustment costs to `code/enk.py`. *Env question:* do emissions now
   respond more or less to a TFP shock under a carbon tax? Why? (Hint: investment is the most cyclical demand component.)
3. Read SW (2007) section 2 and write down which of their 7 shocks would show up as a carbon-tax shock in
   an estimated model that omits environmental policy. (It loads on the price-markup shock, mainly.)
