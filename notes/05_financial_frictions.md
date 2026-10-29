# Module 5: Financial frictions — the financial accelerator and banks

> **Goal:** know the three canonical ways to put finance into an NK model, the amplification mechanism
> each one delivers, and how this connects to **transition risk, stranded assets and green QE**.

**Core reading:** Bernanke, Gertler & Gilchrist (1999), "The financial accelerator in a quantitative business cycle
framework", *Handbook of Macro* vol. 1C; Kiyotaki & Moore (1997, *JPE*), "Credit cycles"; Gertler & Karadi (2011, *JME*),
"A model of unconventional monetary policy"; Gertler & Kiyotaki (2010), *Handbook of Monetary Economics*;
Iacoviello (2005, *AER*); Christiano, Motto & Rostagno (2014, *AER*), "Risk shocks".

---

## 5.1 BGG: costly state verification

Entrepreneurs buy capital $Q_tK_{t+1}$ with net worth $N_t$ plus debt. Because lenders must pay a
monitoring cost to see the idiosyncratic return, the optimal contract implies an **external finance
premium** that rises with leverage:

$$
\frac{E_t R^k_{t+1}}{R_t} = s\!\left(\frac{Q_t K_{t+1}}{N_t}\right), \qquad s' > 0.
$$

Net worth accumulates from retained returns: $N_{t+1} = \gamma [R^k_{t+1}Q_tK_{t+1} - R_t(Q_tK_{t+1}-N_t)\cdot(\dots)]$.
**Accelerator:** a bad shock → asset prices $Q$ fall → net worth falls → premium rises → investment falls → $Q$ falls more.
CMR (2014) add **risk shocks** (time-varying dispersion of idiosyncratic returns) and find they drive a large
share of US cycles.

## 5.2 Gertler–Karadi: bank balance sheets

Bankers can divert a fraction $\lambda$ of assets, so depositors limit leverage:
$Q_t S_t = \phi_t N_t$, with $\phi_t$ rising in the excess return $E_t(R^k_{t+1} - R_t)$. The **spread** is
the key endogenous variable. A central bank that buys assets (no diversion problem, but an efficiency
cost) relaxes the constraint → **credit policy / QE** works in this model through the spread.

## 5.3 Kiyotaki–Moore: collateral constraints

$b_t \le m E_t[q_{t+1}k_t/R_t]$. Asset prices enter borrowing capacity, which creates a dynamic multiplier.
Iacoviello (2005) uses housing as collateral with nominal debt (debt-deflation channel).

## 5.4 Environmental angles (an active literature)

* **Transition risk & stranded assets.** A credible carbon tax lowers the value of brown capital ($Q^{brown}$
  falls), which hits the net worth of the firms or banks that hold it, so a financial accelerator amplifies
  the transition. Carattini, Heutel & Melkadze (2023, *RED*), "Climate policy, financial frictions, and transition risk",
  show this and study **macroprudential** tools that smooth it.
* **Green macroprudential policy.** Diluiso, Annicchiarico, Kalkuhl & Minx (2021, *JEEM*), "Climate actions and
  macro-financial stability: the role of central banks", compare green QE and green capital requirements in an E-DSGE with GK banks.
* **Green QE.** Ferrari & Nispi Landi (2023, *IJCB*), "Toward a green economy: the role of central bank's asset purchases":
  purchases tilted to green bonds reduce emissions modestly; effect depends on green/brown substitutability. Nakov & Thomas
  (2026, *JPE Macro*) find tilting is optimal but limited by small spreads.
* **Asset pricing of carbon.** Benmir, Jaccard & Vermandel (2020, ECB WP 2477), "Green asset pricing": an asset-pricing
  E-DSGE (habits, pollution externality) in which risk premia shape the optimal carbon price. Read it for the
  methods: it shows how much a model's welfare conclusions depend on matching asset-price moments.

Research gap to think about: **who holds the brown assets** (households in HANK vs. banks) determines whether
transition risk is a demand shock, a financial shock, or both.

---

## Exercises
1. Write down the GK model's bank problem and derive $\phi_t$. Implement a two-sector (green/brown capital)
   version in Dynare where a carbon-tax shock lowers $Q^{brown}$.
2. Compare the output response to the same carbon-tax shock with and without the GK friction. What is the
   "transition-risk multiplier"?
