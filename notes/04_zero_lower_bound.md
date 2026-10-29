# Module 4: The zero lower bound, liquidity traps, and NK "paradoxes"

> **Goal:** understand why the ZLB turns NK logic upside down (supply shocks, fiscal multipliers,
> forward guidance), how to solve models with occasionally binding constraints, and why this matters
> for carbon pricing in a low-rate world.

**Core reading:** Krugman (1998, *BPEA*), "It's baaack"; Eggertsson & Woodford (2003, *BPEA*);
Christiano, Eichenbaum & Rebelo (2011, *JPE*), "When is the government spending multiplier large?";
Werning (2011, NBER WP), "Managing a liquidity trap"; Eggertsson (2010), "The paradox of toil".
**Global multiplicity:** Benhabib, Schmitt-Grohé & Uribe (2001, *JET*), "The perils of Taylor rules".
**Methods:** Guerrieri & Iacoviello (2015, *JME*), OccBin. **Evidence:** Wieland (2019, *JPE*), "Are negative supply shocks expansionary at the zero lower bound?".

---

## 4.1 The two-state liquidity trap (do this by hand)

The natural rate falls to $r^n_L < 0$ and each period stays low with probability $p$ (returns to normal
and stays there forever with $1-p$). In the low state $i_t = 0$, so with $\pi_t = \pi_L$, $x_t = x_L$:

$$
\pi_L = \beta p\, \pi_L + \kappa x_L, \qquad
x_L = p\, x_L + \tfrac{1}{\sigma}\left(p\,\pi_L + r^n_L\right)
$$

(written with $\rho = 0$ for brevity). Solving:

$$
x_L = \frac{(1-\beta p)}{\sigma\,\Gamma} r^n_L, \qquad \pi_L = \frac{\kappa}{\sigma\,\Gamma} r^n_L,
\qquad \Gamma = (1-p)(1-\beta p) - \frac{p\kappa}{\sigma} > 0 .
$$

Read the denominator: as $p$ rises or prices become **more flexible** (higher $\kappa$), $\Gamma \to 0$
and the slump explodes. Expected deflation raises real rates, which deepens the slump, which deepens
deflation. *More price flexibility is destabilizing at the ZLB* (Eggertsson & Krugman; Werning).

## 4.2 The paradoxes (all from the same mechanism: at the ZLB, $\uparrow E\pi \Rightarrow \downarrow r$)

* **Paradox of toil:** a positive labor-supply shock lowers marginal cost → deflation → higher real rate → lower output.
* **Negative supply shocks are expansionary:** a cost increase raises expected inflation → lowers real rates.
  Wieland (2019) tests this with the Japanese earthquake and oil supply shocks and **rejects it**. That is a
  warning sign that standard NK expectations are too strong at the ZLB (see Module 9).
* **Large fiscal multipliers:** $G$ raises inflation and lowers real rates (CER 2011 find multipliers $\gg 1$).
* **Forward guidance puzzle:** promises about rates far in the future have huge effects today
  (Del Negro, Giannoni & Patterson; McKay, Nakamura & Steinsson 2016, *AER*). Fixes: HANK, behavioral discounting.

## 4.3 Solving models with the ZLB

| Method | Idea | Use when |
|---|---|---|
| Two-state Markov (above) | analytic | intuition, teaching |
| **OccBin** (Guerrieri–Iacoviello) | piecewise-linear, guess-and-verify regime durations | medium-scale models, estimation (Dynare `occbin_setup/occbin_solver`) |
| Perfect foresight with constraint | Newton on stacked nonlinear system | deterministic transitions (Dynare `perfect_foresight_solver` with `lmmcp`) |
| Global (time iteration / projection) | full nonlinearity, precautionary effects of ZLB risk | small models; risk-of-ZLB questions |

## 4.4 Environmental angles

1. **Carbon pricing at the ZLB.** In a standard NK model a carbon tax is a negative supply shock, so at the ZLB it is
   *expansionary* in the short run. Is that robust once you add HANK or bounded rationality? Wieland's
   evidence says probably not. That is a clean research question.
2. **ETS prices and recessions.** Under a cap the permit price collapses in a recession
   (EU ETS 2008–2012, see the `enk_tfp_tax_vs_cap.png` figure: under a cap the carbon price is very
   procyclical). At the ZLB, the cap therefore acts as an **automatic stabilizer**. How should a price
   floor/ceiling or the EU **Market Stability Reserve** interact with monetary policy at the ZLB?
3. **Green fiscal stimulus.** Multipliers of public green investment at the ZLB vs. normal times.

---

## Exercises
1. Verify the closed form for $(x_L, \pi_L)$ and plot $x_L$ against $p$ and $\theta$ (Calvo).
2. Implement the two-state trap in `code/` and add a carbon tax that stays high exactly while the trap lasts.
   Under which parameters is it expansionary?
