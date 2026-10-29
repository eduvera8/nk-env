# Module 1: The canonical New Keynesian model (refresher, done properly)

> **Goal:** be able to derive the 3-equation model in an afternoon, know where every
> parameter comes from, and know exactly which assumption each frontier literature relaxes.
> Everything after this module modifies one or more of these steps.

**Core reading:** Galí (2015), *Monetary Policy, Inflation, and the Business Cycle*, 2nd ed., ch. 1–5.
**Deeper:** Woodford (2003), *Interest and Prices*, ch. 2–4, 6. Clarida, Galí & Gertler (1999, *JEL*), "The Science of Monetary Policy".

---

## 1.1 Environment

**Households** maximize

$$
E_0 \sum_{t=0}^{\infty} \beta^t \left[ \frac{C_t^{1-\sigma}}{1-\sigma} - \chi \frac{N_t^{1+\varphi}}{1+\varphi} \right],
\qquad C_t = \left( \int_0^1 C_t(j)^{\frac{\varepsilon-1}{\varepsilon}} dj \right)^{\frac{\varepsilon}{\varepsilon-1}}
$$

subject to $P_t C_t + B_t = (1+i_{t-1}) B_{t-1} + W_t N_t + D_t$ (profits $D_t$).

FOCs:

* **Demand for variety $j$:** $C_t(j) = (P_t(j)/P_t)^{-\varepsilon} C_t$, with $P_t = \left(\int P_t(j)^{1-\varepsilon}dj\right)^{1/(1-\varepsilon)}$.
* **Euler equation:** $1 = \beta E_t \left[ \left(\frac{C_{t+1}}{C_t}\right)^{-\sigma} \frac{1+i_t}{\Pi_{t+1}} \right]$.
* **Labor supply:** $\chi N_t^{\varphi} C_t^{\sigma} = W_t/P_t$.

**Firms** produce $Y_t(j) = A_t N_t(j)$ and face Calvo frictions: each period a firm can reset its
price with probability $1-\theta$. Real marginal cost is common to all firms (constant returns):
$MC_t = (W_t/P_t)/A_t$.

## 1.2 Calvo pricing → the NKPC

A resetting firm chooses $P_t^{\ast}$ to maximize expected discounted profits **while the price is stuck**:

$$
\max_{P_t^{\ast}} \; E_t \sum_{k=0}^{\infty} (\beta\theta)^k \Lambda_{t,t+k}
\left[ \frac{P_t^{\ast}}{P_{t+k}} - MC_{t+k} \right] \left(\frac{P_t^{\ast}}{P_{t+k}}\right)^{-\varepsilon} Y_{t+k}.
$$

FOC: $\sum_k (\beta\theta)^k E_t\lbrace \Lambda_{t,t+k} Y_{t+k} P_{t+k}^{\varepsilon}[P_t^{\ast} - \mathcal{M} P_{t+k} MC_{t+k}]\rbrace  = 0$,
where $\mathcal{M} = \varepsilon/(\varepsilon-1)$ is the desired markup. Two facts:

1. **Recursive form (what you code):** $p^{\ast}_t \equiv P^{\ast}_t/P_t = \mathcal{M}\, x_{1t}/x_{2t}$ with
   $x_{1t} = \Lambda_t MC_t Y_t + \beta\theta E_t \Pi_{t+1}^{\varepsilon} x_{1,t+1}$ and
   $x_{2t} = \Lambda_t Y_t + \beta\theta E_t \Pi_{t+1}^{\varepsilon-1} x_{2,t+1}$.
   The price index gives $1 = \theta \Pi_t^{\varepsilon-1} + (1-\theta) (p_t^{\ast})^{1-\varepsilon}$ and
   **price dispersion** $\Delta_t = \int (P_t(j)/P_t)^{-\varepsilon}dj$ evolves as
   $\Delta_t = \theta \Pi_t^{\varepsilon} \Delta_{t-1} + (1-\theta)(p^{\ast}_t)^{-\varepsilon}$, with $Y_t \Delta_t = A_t N_t$.
   This is exactly what `code/enk.py` and `dynare/etank.mod` implement.
2. **Log-linear form:** $p^{\ast}_t - p_{t-1} = (1-\beta\theta) \sum_k (\beta\theta)^k E_t[\widehat{mc}_{t+k} + p_{t+k} - p_{t-1}]$
   and $\pi_t = (1-\theta)(p^{\ast}_t - p_{t-1})$. Combining:

$$
\boxed{\pi_t = \beta E_t \pi_{t+1} + \lambda\, \widehat{mc}_t, \qquad \lambda = \frac{(1-\theta)(1-\beta\theta)}{\theta}}
$$

Price dispersion is **second order** around a zero-inflation steady state, so it drops out of the
linear model but is *the* source of the welfare cost of inflation (see Module 3).

**Rotemberg equivalence.** With quadratic adjustment costs $\frac{\phi_R}{2}(\Pi_t-1)^2 Y_t$ the slope is
$(\varepsilon-1)/\phi_R$. Setting $\phi_R = \theta(\varepsilon-1)/[(1-\theta)(1-\beta\theta)]$ gives identical first-order
dynamics. They differ in nonlinear solutions, in welfare (adjustment costs use resources vs. dispersion),
and at the ZLB / with trend inflation. Many E-DSGE papers use Rotemberg because it is easy in levels.

## 1.3 From marginal cost to the output gap

Market clearing $Y_t = C_t$, labor supply and $Y_t = A_t N_t$ give
$\widehat{mc}_t = (\sigma+\varphi)(y_t - y^n_t)$ where $y_t^n = \frac{1+\varphi}{\sigma+\varphi} a_t$ is **natural (flex-price)
output**. Define the gap $x_t \equiv y_t - y_t^n$:

$$
\pi_t = \beta E_t \pi_{t+1} + \kappa x_t + u_t, \qquad \kappa = \lambda(\sigma+\varphi)
$$

$u_t$ is a **cost-push shock**: anything that moves marginal cost *without* moving efficient output
(markup shocks, wage markups, … **and a carbon tax that is not set optimally**; see Module 11).

The Euler equation in gaps is the **dynamic IS curve**:

$$
x_t = E_t x_{t+1} - \frac{1}{\sigma}\left( i_t - E_t \pi_{t+1} - r^n_t \right), \qquad r^n_t = \rho + \sigma E_t \Delta y^n_{t+1}.
$$

Close with a rule, e.g. $i_t = \rho + \phi_\pi \pi_t + \phi_x x_t + v_t$.

## 1.4 Three results you must be able to state

1. **Taylor principle / determinacy.** The model has a unique bounded equilibrium iff
   $\kappa(\phi_\pi - 1) + (1-\beta)\phi_x > 0$ (Bullard & Mitra 2002). Run `python code/nk3.py`: it
   counts generalized eigenvalues (Blanchard–Kahn 1980) and reports indeterminacy for $\phi_\pi < 1$.
2. **Divine coincidence.** Without $u_t$, $\pi_t = 0 \Rightarrow x_t = 0$: stabilizing inflation also
   stabilizes the welfare-relevant gap. With $u_t$ there is a **trade-off**. *Most of the
   "monetary policy and climate" debate is about whether climate policy creates a $u_t$.*
3. **Analytical solution with AR(1) shocks** (method of undetermined coefficients). For
   $u_t = \rho_u u_{t-1} + \epsilon_t$ and $\phi_x = 0$, guess $\pi_t = a u_t$, $x_t = b u_t$:

$$
a = \frac{\sigma(1-\rho_u)}{\Omega}, \quad b = -\frac{\phi_\pi - \rho_u}{\Omega}, \quad
\Omega = \sigma(1-\rho_u)(1-\beta\rho_u) + \kappa(\phi_\pi - \rho_u).
$$

   Do this by hand once. A more hawkish $\phi_\pi$ lowers $a$ and raises $\lvert b\rvert$: the policy trade-off in two lines.

## 1.5 Solving linear rational-expectations models (what Dynare does)

Write the model as $A E_t y_{t+1} + B y_t + C y_{t-1} + D \epsilon_t = 0$. Seek $y_t = P y_{t-1} + Q \epsilon_t$.
$P$ solves the matrix quadratic $AP^2 + BP + C = 0$; stack it as a generalized eigenvalue problem and
use the QZ (generalized Schur) decomposition to pick the stable roots (Klein 2000; Sims 2002).
Then $Q = -(AP+B)^{-1}D$. Read `code/solver.py`: it is about 40 lines and has no black box.

## 1.6 Welfare (preview of Module 3)

A second-order approximation of household utility around an efficient steady state gives

$$
\mathbb{W} \approx -\frac{1}{2}\, E_0 \sum_t \beta^t \left[ \frac{\varepsilon}{\lambda}\pi_t^2 + (\sigma+\varphi) x_t^2 \right]
\;\propto\; - E_0 \sum_t \beta^t \left[ \pi_t^2 + \frac{\kappa}{\varepsilon} x_t^2 \right].
$$

Inflation is costly because it creates price dispersion (misallocation across varieties). The large
relative weight on $\pi$ (with $\varepsilon = 6$, $\kappa/\varepsilon \approx 0.02$) is why NK models like inflation targeting.

---

## Exercises

1. Derive the NKPC including **decreasing returns** $Y = AN^{1-\alpha}$: show $\lambda$ gets multiplied by
   $\frac{1-\alpha}{1-\alpha+\alpha\varepsilon}$ (strategic complementarity).
2. Using `code/nk3.py`, verify numerically the closed form for $a, b$ above.
3. Change `phi_x` and find the determinacy frontier in $(\phi_\pi, \phi_x)$ space. Compare to the Bullard–Mitra condition.
4. *Env warm-up:* Suppose firms pay a tax $\tau_t$ per unit of output. Show that it enters the NKPC
   like $u_t$ if $\tau_t$ does not change efficient output, and like a natural-rate shock if it does.
   You'll redo this properly in Module 11.
