# Module 3: Optimal monetary policy (and why it is the tool for policy-mix questions)

> **Goal:** compute optimal policy under discretion and commitment, evaluate rules with
> welfare, and set up **Ramsey problems with several instruments** (interest rate + carbon tax),
> which is the natural framework for "monetary and environmental policy interaction" papers.

**Core reading:** Galí (2015) ch. 5; Woodford (2003) ch. 6–7; Clarida, Galí & Gertler (1999, *JEL*).
**Ramsey methods:** Schmitt-Grohé & Uribe (2007, *JME*), "Optimal simple and implementable monetary and fiscal rules";
Dynare's `ramsey_model`, `discretionary_policy`, `osr`.

---

## 3.1 Linear-quadratic problem

Minimize $\frac{1}{2}E_0\sum_t \beta^t(\pi_t^2 + \vartheta x_t^2)$, $\vartheta = \kappa/\varepsilon$, s.t. $\pi_t = \beta E_t\pi_{t+1} + \kappa x_t + u_t$.

**Discretion** (re-optimize each period, taking expectations as given):

$$
x_t = -\frac{\kappa}{\vartheta}\pi_t = -\varepsilon\,\pi_t \qquad\Rightarrow\qquad
\pi_t = \frac{\vartheta}{\kappa^2 + \vartheta(1-\beta\rho_u)}u_t .
$$

**Commitment** (timeless perspective): $x_t - x_{t-1} = -\varepsilon\,\pi_t$, so $\hat p_t = -\frac{1}{\varepsilon}x_t$:
the price **level** is stationary. The central bank promises to undershoot later, which lowers inflation
expectations today, so a cost-push shock is absorbed with less output loss.
**Stabilization bias** is the gap between the two.

**Why you care:** if a carbon-tax path acts as a sequence of cost-push shocks, commitment means the
central bank can "look through" the transition *without* de-anchoring, as long as it is credible.

## 3.2 Optimal simple rules

Search over $(\phi_\pi, \phi_x, \rho_i)$ to maximize welfare (or minimize an ad hoc loss) across the
shock distribution. In Dynare: `osr` with `optim_weights`. Report welfare in **consumption-equivalent**
terms: the % of steady-state consumption households would give up to live under rule A rather than B.

## 3.3 Ramsey with multiple instruments

Write the planner's Lagrangian with **all private equilibrium conditions** as constraints
(nonlinear), and choose all allocations and instruments. Dynare does this automatically:

```
planner_objective log(C) - chi*N^(1+phi)/(1+phi) - (environmental disutility if any);
ramsey_model(planner_discount=0.99, instruments=(r, tau));
stoch_simul(order=1);
```

This is how Annicchiarico & Di Dio (2015, *JEEM*) characterize jointly optimal monetary and environmental
policy in an NK model, and how Nakov & Thomas ("Climate-conscious monetary policy", *JPE Macro* 2026)
show:

* if the carbon tax is set **optimally** (Pigouvian), there is no trade-off: monetary policy should
  simply stabilize inflation (divine coincidence holds w.r.t. the welfare-relevant gap);
* if the carbon tax is **too low**, a trade-off arises, but it is resolved mostly in favor of price
  stability: interest rates are a poor tool for the climate externality.

This "Tinbergen" structure (one instrument per distortion) is the right benchmark to keep in mind
whenever someone proposes "green monetary policy".

## 3.4 Welfare-relevant vs. natural vs. efficient output

With an externality there are *three* output concepts:
1. **Natural**: flexible prices, *given* the actual (possibly suboptimal) carbon tax;
2. **Efficient**: flexible prices **and** the externality internalized;
3. **Actual**.

The NKPC is driven by $y - y^{natural}$; welfare depends on $y - y^{efficient}$. The wedge between the two
is the climate-policy gap. Getting this decomposition right is the core analytical content of any
"monetary policy + carbon tax" paper.

---

## Exercises
1. Derive the discretion and commitment solutions above. Simulate both with `code/solver.py`
   (commitment needs the lagged Lagrange multiplier as a state).
2. In `code/enk.py`, add a quadratic loss and search over $\phi_\pi \in [1.1, 5]$ for a carbon-tax shock.
   How does the optimal $\phi_\pi$ depend on `lam` (TANK)?
3. Write the Ramsey problem for the E-NK model of Module 11 in Dynare (`ramsey_model` with
   instruments `r` and `tau`). Add the damage externality to the objective via the production function
   (it is already there through $d(X)$). Is the optimal carbon tax procyclical?
   (Compare Heutel 2012, who finds optimal emissions are procyclical but less so than under a fixed tax.)
