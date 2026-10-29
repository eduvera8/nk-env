# Module 6: Open-economy New Keynesian models

> **Goal:** master the Galí–Monacelli small open economy (SOE), know the pricing paradigms
> (PCP / LCP / DCP), and see why open-economy NK is the natural home for **energy imports,
> carbon leakage and carbon border adjustments (CBAM)**.

**Core reading:** Galí & Monacelli (2005, *REStud*), "Monetary policy and exchange rate volatility in a small open economy";
Galí (2015) ch. 8; Clarida, Galí & Gertler (2002, *JME*), "A simple framework for international monetary policy analysis";
Corsetti & Pesenti (2001, *QJE*); Engel (2011, *AER*), "Currency misalignments and optimal monetary policy";
Gopinath et al. (2020, *AER*), "Dominant currency paradigm"; Schmitt-Grohé & Uribe (2003, *JIE*), "Closing small open economy models".

---

## 6.1 Galí–Monacelli in five equations

Home is small, with openness $\alpha$ (import share). Define the terms of trade $s_t = p_{F,t} - p_{H,t}$.

* CPI vs. domestic inflation: $\pi_t = \pi_{H,t} + \alpha \Delta s_t$.
* Complete markets / international risk sharing: $c_t = y^*_t + \frac{1-\alpha}{\sigma} s_t$.
* Goods market: $y_t = y^*_t + \frac{\omega_\alpha}{\sigma} s_t$ (with $\omega_\alpha$ depending on trade elasticities).
* Domestic NKPC: $\pi_{H,t} = \beta E_t \pi_{H,t+1} + \kappa_\alpha x_t$, with $\kappa_\alpha = \lambda(\sigma_\alpha + \varphi)$, $\sigma_\alpha = \sigma/(1 + \alpha(\omega - 1))$.
* Open-economy IS: $x_t = E_t x_{t+1} - \frac{1}{\sigma_\alpha}(i_t - E_t\pi_{H,t+1} - r^n_t)$.

**Key result:** in the special case ($\sigma = \eta = \gamma = 1$) the SOE is isomorphic to the closed economy, and
optimal policy targets **domestic (PPI) inflation**, not CPI, letting the exchange rate float.
That conclusion breaks under local-currency pricing (LCP: misalignments become a welfare cost, Engel 2011)
and with dominant-currency pricing (DCP: the dollar's role makes import prices sticky in dollars).

**Incomplete markets:** to close an SOE with a single bond, use a debt-elastic interest premium
(SGU 2003); otherwise the steady state is not unique.

## 6.2 Adding imported energy

Let consumption be a CES aggregate of core goods and energy, with energy imported at world price $p^E_t$.
Then $\pi_t = (1-\omega_E)\pi^{core}_t + \omega_E \pi^E_t$ and an energy price shock is a **CPI cost-push shock**
whose pass-through depends on the substitution elasticity and wage indexation. With low elasticity
(short run), energy shocks are stagflationary. Blanchard & Galí (2007, NBER), "The macroeconomic effects of
oil shocks: why are the 2000s so different from the 1970s?" is the key reference. Their answer: smaller
energy shares, more flexible labor markets, and more credible monetary policy.

## 6.3 Environmental angles

* **Carbon leakage and CBAM.** A unilateral carbon tax shifts dirty production abroad; a border adjustment
  taxes the carbon content of imports. In an NK SOE this changes the terms of trade, CPI inflation and the
  exchange rate. What should monetary policy target during the phase-in of CBAM?
* **Green transition for commodity exporters.** Airaudo, Pappa & Seoane, "The green metamorphosis of a small open economy"
  (working paper): a fossil-fuel-dependent SOE transitions to green production. Commodity exporters of
  "green minerals" (copper, lithium) are the mirror image: the transition is a **positive** terms-of-trade shock.
* **International spillovers of climate policy.** Annicchiarico & Diluiso (2019, *Resource and Energy Economics*),
  "International transmission of the business cycle and environmental policy": a two-country E-DSGE.
* **Energy-price shocks and monetary policy in 2021–23.** Huge empirical motivation; a SOE-NK with imported gas,
  hand-to-mouth households and wage rigidity is a natural framework (see Chan, Diz & Kanngiesser, "Energy prices and
  household heterogeneity: monetary policy in a Gas-TANK", *JME* 2024).

---

## Exercises
1. Derive the CPI–PPI relation and the risk-sharing condition. Show isomorphism in the special case.
2. Extend `code/enk.py` to an SOE: imported fossil energy as an input, carbon tax on its use, an exchange
   rate, UIP with a debt-elastic premium. Compare a carbon-tax shock under PPI vs. CPI inflation targeting.
