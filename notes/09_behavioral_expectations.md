# Module 9: Behavioral NK and expectations

> **Goal:** understand why rational-expectations NK models give implausible answers about the far future
> (forward guidance puzzle, ZLB paradoxes), the main fixes, and why **credibility of announced
> climate policy paths** is an expectations problem.

**Core reading:** Gabaix (2020, *AER*), "A behavioral New Keynesian model"; Farhi & Werning (2019, *AER*), "Monetary policy,
bounded rationality, and incomplete markets"; Angeletos & Lian (2018, *AER*), "Forward guidance without common knowledge";
García-Schmidt & Woodford (2019, *AER*), "Are low interest rates deflationary? A paradox of perfect-foresight analysis";
Woodford (2019, *NBER Macro Annual*), "Monetary policy analysis when planning horizons are finite"; Angeletos & Huo (2021, *AER*),
"Myopia and anchoring".
**Learning:** Evans & Honkapohja (2001), *Learning and Expectations in Macroeconomics*; Eusepi & Preston (2011, *AER*).
**Survey evidence:** Coibion & Gorodnichenko (2015, *AER*), information rigidity; Bordalo, Gennaioli, Ma & Shleifer (2020, *AER*),
overreaction; Coibion & Gorodnichenko (2015, *AEJ: Macro*), "Is the Phillips curve alive and well after all?": household
inflation expectations track **gasoline prices**.

---

## 9.1 The problem

Iterate the DIS forward: $x_t = -\frac{1}{\sigma}\sum_{k\ge 0} E_t(i_{t+k} - \pi_{t+k+1} - r^n_{t+k})$.
A promised rate cut at $t+20$ has the **same** effect on $x_t$ as a cut today, and through the NKPC an
even larger effect on inflation. This is implausible and contradicts evidence.

## 9.2 Gabaix's cognitive discounting

Agents perceive deviations from steady state as smaller the further out they are, with attention parameter $\bar m \in [0,1]$:

$$
x_t = M\,E_t x_{t+1} - \frac{1}{\sigma}(i_t - E_t\pi_{t+1} - r^n_t), \qquad
\pi_t = \beta M^f E_t\pi_{t+1} + \kappa x_t,
$$

with $M, M^f < 1$. Consequences:
* forward guidance is weaker and the puzzle disappears;
* ZLB spirals are bounded;
* determinacy can hold **even with a passive rule** when inattention is strong enough;
* fiscal policy becomes more powerful (agents are non-Ricardian).

It costs you one parameter and almost no extra code: put `M` in `code/nk3.py`.

## 9.3 Other routes to the same place

* **Level-$k$ thinking / reflective equilibrium** (Farhi–Werning; García-Schmidt–Woodford): agents iterate a finite number of
  steps of reasoning about others' behavior, so GE feedback is truncated. Interacts strongly with incomplete markets.
* **Incomplete information / higher-order beliefs** (Angeletos–Lian): lack of common knowledge about others' responses dampens GE effects.
* **Finite planning horizons** (Woodford 2019): agents plan $k$ periods ahead with a value function learned from experience.
* **Adaptive learning:** agents run regressions. E-stability selects equilibria. Expectations can drift and de-anchor.
* **Diagnostic expectations** (BGMS): overreaction to news.

## 9.4 Environmental angles

* **Credibility of carbon-price paths.** The green transition is a long *announced* path of rising carbon prices. Under RE,
  a credible future tax raises expected marginal costs and **today's** inflation; under cognitive discounting or imperfect
  credibility, much less. Ferrari & Nispi Landi (2022, ECB WP 2726), "Will the green transition be inflationary? Expectations matter",
  is the starting point.
* **Salience and de-anchoring.** Households form inflation expectations from salient prices: energy, gasoline. A carbon tax
  raises the most salient prices, so it may de-anchor expectations more than its CPI weight suggests. A model with learning or
  salience-weighted expectations plus a carbon tax is a strong idea with an obvious empirical counterpart (household surveys).
* **Policy-uncertainty about climate policy itself:** regime-switching beliefs about whether the tax will be repealed.

---

## Exercises
1. Add Gabaix's $M$ and $M^f$ to `code/nk3.py`. Plot the response to a rate cut announced for $t = 8$ (news shock) for $M = 1$ vs. $M = 0.85$.
2. In `code/enk.py`, model a pre-announced carbon tax increase 8 quarters ahead (add news shocks, i.e. lags of `e_z`). Compare RE vs. cognitive discounting.
