"""
Module 1: the textbook three-equation New Keynesian model (Galí 2015, ch. 3),
already log-linearized. Variables are deviations from steady state.

    x_t  = E_t x_{t+1} - (1/sigma) (i_t - E_t pi_{t+1} - rn_t)     (dynamic IS)
    pi_t = beta E_t pi_{t+1} + kappa x_t + u_t                      (NKPC)
    i_t  = phi_pi pi_t + phi_x x_t + v_t                            (Taylor rule)

Run:  python code/nk3.py      -> figures/nk3_irfs.png + Taylor-principle check
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from solver import Model

VARS = ["x", "pi", "i", "rn", "u", "v"]
SHOCKS = ["e_rn", "e_u", "e_v"]


def build(beta=0.99, sigma=1.0, phi=1.0, theta=0.75, eps=6.0,
          phi_pi=1.5, phi_x=0.125, rho_rn=0.8, rho_u=0.5, rho_v=0.5):
    # Calvo slope:  kappa = lambda (sigma + phi),  lambda = (1-theta)(1-beta theta)/theta
    lam = (1 - theta) * (1 - beta * theta) / theta
    kappa = lam * (sigma + phi)

    def f(yp, y, ym, e):
        x, pi, i, rn, u, v = y
        xp, pip = yp[0], yp[1]
        return np.array([
            x - xp + (i - pip - rn) / sigma,
            pi - beta * pip - kappa * x - u,
            i - phi_pi * pi - phi_x * x - v,
            rn - rho_rn * ym[3] - e[0],
            u - rho_u * ym[4] - e[1],
            v - rho_v * ym[5] - e[2],
        ])

    return Model(VARS, SHOCKS, f, np.zeros(len(VARS)))


if __name__ == "__main__":
    m = build()
    titles = {"e_v": "Monetary shock (e_v = 0.25)", "e_u": "Cost-push shock", "e_rn": "Natural-rate (demand) shock"}
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))
    for ax, s in zip(axes, ["e_v", "e_u", "e_rn"]):
        r = m.irf(s, size=0.25, T=16)
        for v, lab in [("x", "output gap"), ("pi", "inflation (q/q)"), ("i", "policy rate (q/q)")]:
            ax.plot(r[v], label=lab)
        ax.axhline(0, color="k", lw=0.5)
        ax.set_title(titles[s]); ax.set_xlabel("quarters")
    axes[0].legend()
    fig.tight_layout(); fig.savefig("figures/nk3_irfs.png", dpi=130)
    print("saved figures/nk3_irfs.png")

    # Taylor principle: determinacy requires (roughly) phi_pi > 1
    for phi_pi in [0.8, 1.0 - 1e-3, 1.01, 1.5]:
        try:
            build(phi_pi=phi_pi, phi_x=0.0)
            print(f"phi_pi = {phi_pi:5.3f}: determinate")
        except ValueError as err:
            print(f"phi_pi = {phi_pi:5.3f}: {err}")
