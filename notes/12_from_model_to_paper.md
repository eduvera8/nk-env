# Module 12: From model to paper

## 12.1 What makes an NK + environment paper publishable

A field journal (JEEM, JAERE, ERE, RED, JEDC, EER, JME, *JPE Macro*) wants **one sharp question**, a
**mechanism** you can explain in one paragraph (ideally an analytical result in a simple version), and a **quantitative**
answer in a richer model that is disciplined by data, plus policy implications. Avoid "I added X to an E-DSGE".
Instead: "X changes the answer to policy question Y because of mechanism Z".

## 12.2 Candidate questions (ranked for a first paper)

**A. Carbon-tax revenue recycling as a macro-stabilization tool (THANK/HANK).** *Recommended.*
*Question:* How should carbon revenue be recycled, and how should monetary policy react, when MPCs and energy budget
shares are heterogeneous? *Mechanism:* recycling changes χ (Module 7), so it changes both the aggregate demand
effect and the inflation–output trade-off of carbon pricing. *Discipline:* Känzig's (2023) evidence on unequal effects;
Consumer Expenditure Survey energy shares. *Path:* analytical THANK version → quantitative HANK with `sequence-jacobian`.
*Why it's good:* strong empirical motivation, clear policy relevance (EU Social Climate Fund, carbon dividends), and frontier tools.
**Check novelty carefully:** this area is active (Gas-TANK, energy-shock HANK, HA carbon-tax papers), so your contribution
must be specific, e.g. the *monetary–fiscal* interaction of recycling, or the *transition-path* dimension.

**B. Emissions trading, the ZLB and the Market Stability Reserve.**
*Question:* Does a cap-and-trade system with price-stabilizing mechanisms (MSR, price floors) help or hurt macro
stabilization when monetary policy is constrained by the ZLB? *Tools:* the `etank.mod` cap regime + OccBin.
*Why it's good:* clean, policy-relevant, technically manageable. You can build directly on the code here.

**C. Greenflation with state-dependent pricing.**
*Question:* Is the inflation cost of a carbon-price path nonlinear in its speed? *Tools:* multisector NK with a
nonlinear (menu-cost-consistent) Phillips curve; perfect-foresight transitions. Harder, more novel.

**D. A small open economy in the green transition.**
Energy importer with CBAM phase-in, or green-mineral exporter: what should the central bank target (PPI vs. CPI vs. core)?
Good if you have a specific country in mind and its data.

**E. Credibility of carbon-price paths.**
Imperfect credibility or cognitive discounting (Module 9) in an E-NK: how much of the "announcement effect" of carbon
policy survives? Pairs well with survey data on household inflation expectations and energy prices.

## 12.3 Workflow

1. **Literature (2–3 weeks).** Read the Annicchiarico et al. (2022) primer plus the 5 papers closest to your chosen question. Write a
   one-page "what is known / what is not" memo. Search RePEc/NBER/CEPR/ECB WP series for 2024–2026 work.
2. **Simple model (3–4 weeks).** Smallest model that has your mechanism. Get an analytical result if you can (THANK, two-state ZLB,
   two-sector NKPC). This becomes Section 3 of the paper.
3. **Quantitative model (6–10 weeks).** Add only the frictions that matter (Module 11.5). Calibrate/estimate. Match one empirical IRF
   (e.g. Känzig's carbon-policy shock) as external validation.
4. **Policy experiments.** Welfare in consumption-equivalent terms (second order), optimal simple rules, Ramsey benchmark.
5. **Robustness.** Calvo vs. Rotemberg, parameter sensitivity, alternative rules.
6. **Write.** Intro with question, answer, mechanism and contribution in the first two pages.

## 12.4 Paper skeleton

1. Introduction (question, answer, mechanism, contribution vs. 3–5 closest papers)
2. Empirical motivation (one figure/LP)
3. Simple model and analytical results
4. Quantitative model, calibration/estimation
5. Results: transmission, then policy
6. Extensions/robustness
7. Conclusion
