# Module 8: Price-setting microfoundations — menu costs, state dependence, multisector models

> **Goal:** understand what micro price data say, why Calvo is a modeling convenience,
> when state-dependent pricing (menu costs) changes answers, and why **large, sectoral shocks
> like a carbon tax** are exactly where it does.

**Facts:** Bils & Klenow (2004, *JPE*); Nakamura & Steinsson (2008, *QJE*), "Five facts about prices".
**Menu cost models:** Caplin & Spulber (1987, *QJE*); Dotsey, King & Wolman (1999, *QJE*); Golosov & Lucas (2007, *JPE*);
Midrigan (2011, *Econometrica*); Nakamura & Steinsson (2010, *QJE*); Alvarez & Lippi (2014, *Econometrica*);
Alvarez, Le Bihan & Lippi (2016, *AER*), sufficient-statistic approach; Auclert, Rigato, Rognlie & Straub (2024, *QJE*),
"New pricing models, old Phillips curves".
**Information frictions:** Mankiw & Reis (2002, *QJE*), sticky information.
**Multisector / networks:** Carvalho (2006, *B.E. J. Macro*); Aoki (2001, *JME*); Benigno (2004, *JIE*); Rubbo (2023, *Econometrica*), "Networks, Phillips curves,
and monetary policy"; La'O & Tahbaz-Salehi (2022, *Econometrica*), "Optimal monetary policy in production networks".

---

## 8.1 Facts

* Median price duration (excluding sales) is around 8–11 months in US CPI data. **Enormous heterogeneity** exists across sectors:
  energy and fresh food change prices almost every month, while services change roughly once a year or less.
* Price changes are **large** on average (≈10%) but many are small: the distribution has fat tails.
* The **frequency** of price changes rises with inflation (state dependence; very visible in 2021–23).

## 8.2 Time- vs. state-dependent pricing

* **Calvo:** the probability of adjusting is exogenous. Every firm is equally likely to adjust, regardless of how far its price is from optimal.
* **Menu cost:** firms adjust when the gap from the optimal price exceeds an $(S,s)$ band. **Selection effect**: the firms
  that adjust after a monetary shock are those far from optimal, so they make large changes, and the aggregate price level responds faster.
  * Caplin–Spulber: in the extreme case, money is neutral.
  * Golosov–Lucas: real effects are much smaller than Calvo with the same frequency.
  * Midrigan / multiproduct firms / fat-tailed shocks: weaken selection and bring back Calvo-like non-neutrality.
* **Sufficient statistic** (Alvarez–Le Bihan–Lippi): in a broad class of models, the cumulative output effect of a small
  monetary shock is proportional to $\frac{\text{kurtosis of price changes}}{\text{frequency of price changes}}$.
* **For small shocks,** menu-cost models generate a linear Phillips curve close to Calvo with suitably chosen parameters (Auclert et al. 2024).
  **For large shocks,** the frequency responds and the Phillips curve becomes **nonlinear**: inflation responds more, and more quickly.

## 8.3 Multisector NK

With sectors differing in stickiness, a shock to a flexible-price sector (energy) moves relative prices.
The optimal policy stabilizes a **weighted index that puts more weight on sticky sectors** (Aoki 2001; Benigno 2004);
in production networks the right index also depends on input–output linkages (Rubbo 2023; La'O & Tahbaz-Salehi 2022).
This is the formal case for "core" inflation targeting.

## 8.4 Environmental angles

* **"Greenflation" and sectoral stickiness.** Del Negro, di Giovanni & Dogra, "Is the green transition inflationary?"
  (FRBNY Staff Report 1053): in a multisector network NK model, whether climate policy creates an inflation–output trade-off
  depends on the relative price stickiness of dirty vs. clean sectors and on taxes vs. subsidies; for a carbon tax, the
  trade-off is sizable but short-lived. See also Olovsson & Vestin (2023, Riksbank WP), "Greenflation?".
* **State-dependent pass-through of carbon prices.** A large carbon-price increase is precisely the kind of shock where
  menu-cost models predict faster pass-through than Calvo. A **menu-cost or nonlinear-Phillips-curve E-NK** model is a
  plausible research niche: does the speed of a transition affect its inflation cost nonlinearly?
* **Which inflation to target during the transition?** A Rubbo/Aoki-style optimal index in an economy where energy is
  flexible-price and taxed.

---

## Exercises
1. Build a two-sector version of `code/enk.py` with a flexible-price energy sector (θ_E ≈ 0.1) and a sticky core
   (θ = 0.75). Compare headline vs. core inflation targeting after a carbon-tax shock.
2. Read Alvarez–Le Bihan–Lippi and compute the sufficient statistic from published frequency/kurtosis numbers for energy vs. services.
