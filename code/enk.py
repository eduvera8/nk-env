"""
Module 11: an Environmental New Keynesian model with hand-to-mouth households (E-TANK).

Ingredients (each one maps to a module of the notes):
  * Calvo pricing, written recursively (x1, x2, price dispersion)          -> Module 1
  * Savers (share 1-lam) with a Euler equation, hand-to-mouth households
    (share lam) who consume their income each period (TANK)                 -> Module 7
  * Emissions proportional to gross output, endogenous abatement with a
    convex cost, a pollution stock with slow decay, damages on productivity
    (Heutel 2012; Annicchiarico & Di Dio 2015)                             -> Module 11
  * Environmental policy regime: carbon TAX (tau exogenous) or emissions
    CAP (emissions exogenous, tau = endogenous permit price)
  * Carbon revenue rebated lump-sum: uniformly, all to HtM, or all to savers
  * Taylor rule with smoothing

All variables are in logs (except the exogenous states z, v), so IRFs are
log-deviations x 100 = % deviations. Inflation and the interest rate are
quarterly log gross rates.

Run:  python code/enk.py   ->  figures/enk_*.png and a volatility table.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from solver import Model

VARS = ["cs", "ch", "ns", "nh", "w", "y", "mc", "pi", "r", "pstar", "x1", "x2",
        "disp", "u", "tau", "em", "x", "a", "z", "v", "c", "n"]
SHOCKS = ["e_a", "e_z", "e_v"]

BASE = dict(
    # preferences / technology / prices
    beta=0.99, sigma=1.0, phi=1.0, eps=6.0, theta=0.75, N_target=1/3,
    # TANK
    lam=0.0, rebate="uniform",            # 'uniform' | 'htm' | 'savers'
    # monetary policy
    phi_pi=1.5, phi_y=0.125, rho_i=0.0,
    # environment (Nordhaus-style abatement cost, Heutel-style decay)
    varphi=1.0,           # emissions per unit of gross output, before abatement
    theta1=0.05607, theta2=2.8,
    U_target=0.20,        # steady-state abatement share pins down the carbon tax
    delta_x=0.0021,       # quarterly decay of the pollution stock
    dom_share=0.10,       # domestic share of world emissions (rest is exogenous)
    damage_ss=0.005,      # output lost to pollution damages in steady state
    # policy regime and shocks
    regime="tax",         # 'tax' | 'cap'
    rho_a=0.95, rho_z=0.95, rho_v=0.5,
)


def calibrate(p):
    """Closed-form steady state of the representative-agent (lam=0) economy.
    Pins down chi (so N=1/3), tau_bar (so U=U_target), E_row and gamma_d."""
    U = p["U_target"]
    tau = p["theta1"] * p["theta2"] * U ** (p["theta2"] - 1) / p["varphi"]
    mc = (p["eps"] - 1) / p["eps"]
    one_minus_d = 1 - p["damage_ss"]
    N = p["N_target"]
    Y = one_minus_d * N
    w = (mc - p["theta1"] * U ** p["theta2"] - tau * p["varphi"] * (1 - U)) * one_minus_d
    C = Y * (1 - p["theta1"] * U ** p["theta2"])
    chi = w / (N ** p["phi"] * C ** p["sigma"])
    Em = p["varphi"] * (1 - U) * Y
    E_row = Em * (1 - p["dom_share"]) / p["dom_share"]
    X = (Em + E_row) / p["delta_x"]
    gamma_d = -np.log(one_minus_d) / X
    ss = dict(cs=C, ch=C, ns=N, nh=N, w=w, y=Y, mc=mc, pi=1.0, r=1 / p["beta"], pstar=1.0,
              x1=C ** -p["sigma"] * mc * Y / (1 - p["beta"] * p["theta"]),
              x2=C ** -p["sigma"] * Y / (1 - p["beta"] * p["theta"]),
              disp=1.0, u=U, tau=tau, em=Em, x=X, a=1.0, c=C, n=N)
    guess = np.array([np.log(ss[v]) if v not in ("z", "v") else 0.0 for v in VARS])
    return dict(chi=chi, tau_bar=tau, E_row=E_row, gamma_d=gamma_d, Em_bar=Em), guess


def build(**kw):
    p = {**BASE, **kw}
    cal, guess = calibrate(p)
    p.update(cal)
    p.setdefault("y_bar", None)
    m = _make(p, guess)
    # second pass: Taylor rule responds to output relative to its own steady state,
    # and the cap is set at the steady-state level of emissions under the tax
    p["y_bar"] = m.ss("y")
    if p["regime"] == "cap":
        p["Em_bar"] = np.exp(_make({**p, "regime": "tax"}, guess).ss("em"))
    m = _make(p, m.ys)
    m.params = p
    return m


def _make(p, guess):
    beta, sigma, phi, eps, theta = p["beta"], p["sigma"], p["phi"], p["eps"], p["theta"]
    lam, chi = p["lam"], p["chi"]
    th1, th2, varphi = p["theta1"], p["theta2"], p["varphi"]
    I = {v: i for i, v in enumerate(VARS)}
    y_bar = p["y_bar"]

    def transfers(rev):
        if p["rebate"] == "uniform" or lam == 0:
            return rev, rev                                   # (T_H, T_S) per capita
        if p["rebate"] == "htm":
            return rev / lam, 0.0 * rev
        if p["rebate"] == "savers":
            return 0.0 * rev, rev / (1 - lam)
        raise ValueError(p["rebate"])

    def f(yp, y, ym, e):
        L = {v: y[i] for v, i in I.items()}
        Lp = {v: yp[i] for v, i in I.items()}
        Lm = {v: ym[i] for v, i in I.items()}
        E = {v: np.exp(L[v]) for v in VARS if v not in ("z", "v")}
        Ep = {v: np.exp(Lp[v]) for v in ("cs", "pi", "x1", "x2")}

        dmg = 1 - np.exp(-p["gamma_d"] * E["x"])               # damage share d(X)
        prod = E["a"] * (1 - dmg)                              # effective TFP
        rev = E["tau"] * E["em"]                               # carbon revenue
        T_H, _ = transfers(rev)
        Lam = E["cs"] ** -sigma                                # savers' marginal utility (SDF)
        ygap = 0.0 if y_bar is None else L["y"] - y_bar
        r_star = -np.log(beta) + p["phi_pi"] * L["pi"] + p["phi_y"] * ygap

        res = [
            # households
            np.log(beta) - sigma * (Lp["cs"] - L["cs"]) + L["r"] - Lp["pi"],
            np.log(chi) + phi * L["ns"] + sigma * L["cs"] - L["w"],
            np.log(chi) + phi * L["nh"] + sigma * L["ch"] - L["w"],
            E["ch"] - (E["w"] * E["nh"] + T_H),
            # aggregation and resource constraint (savers' budget holds by Walras)
            E["c"] - (lam * E["ch"] + (1 - lam) * E["cs"]),
            E["n"] - (lam * E["nh"] + (1 - lam) * E["ns"]),
            E["y"] - (E["c"] + th1 * E["u"] ** th2 * E["y"] * E["disp"]),
            # production, marginal cost, abatement, emissions, pollution
            L["y"] + L["disp"] - np.log(prod) - L["n"],
            E["mc"] - (E["w"] / prod + th1 * E["u"] ** th2 + E["tau"] * varphi * (1 - E["u"])),
            th1 * th2 * E["u"] ** (th2 - 1) - E["tau"] * varphi,
            E["em"] - varphi * (1 - E["u"]) * E["y"] * E["disp"],
            E["x"] - ((1 - p["delta_x"]) * np.exp(Lm["x"]) + E["em"] + p["E_row"]),
            # environmental policy regime
            (L["tau"] - np.log(p["tau_bar"]) - L["z"]) if p["regime"] == "tax"
            else (L["em"] - np.log(p["Em_bar"]) - L["z"]),
            # exogenous processes
            L["z"] - p["rho_z"] * Lm["z"] - e[1],
            L["a"] - p["rho_a"] * Lm["a"] - e[0],
            L["v"] - p["rho_v"] * Lm["v"] - e[2],
            # Calvo pricing (recursive form)
            E["x1"] - (Lam * E["mc"] * E["y"] + beta * theta * Ep["pi"] ** eps * Ep["x1"]),
            E["x2"] - (Lam * E["y"] + beta * theta * Ep["pi"] ** (eps - 1) * Ep["x2"]),
            L["pstar"] - (np.log(eps / (eps - 1)) + L["x1"] - L["x2"]),
            1 - (theta * E["pi"] ** (eps - 1) + (1 - theta) * E["pstar"] ** (1 - eps)),
            E["disp"] - (theta * E["pi"] ** eps * np.exp(Lm["disp"]) + (1 - theta) * E["pstar"] ** -eps),
            # monetary policy
            L["r"] - (p["rho_i"] * Lm["r"] + (1 - p["rho_i"]) * r_star + L["v"]),
        ]
        return np.array(res)

    return Model(VARS, SHOCKS, f, guess)


def pct(r, v):
    return 100 * r[v]


if __name__ == "__main__":
    T = 24
    q = np.arange(T)

    # ---- Experiment 1: TFP shock under a carbon tax vs an emissions cap -------------
    tax, cap = build(regime="tax"), build(regime="cap")
    fig, axes = plt.subplots(2, 4, figsize=(14, 6))
    panels = [("y", "Output"), ("n", "Hours"), ("c", "Consumption"), ("em", "Emissions"),
              ("tau", "Carbon price"), ("u", "Abatement rate"), ("pi", "Inflation (q/q)"), ("r", "Policy rate (q/q)")]
    for m, lab, ls in [(tax, "carbon tax", "-"), (cap, "emissions cap", "--")]:
        r = m.irf("e_a", size=0.01, T=T)
        for ax, (v, title) in zip(axes.flat, panels):
            ax.plot(q, pct(r, v), ls, label=lab); ax.set_title(title)
    for ax in axes.flat:
        ax.axhline(0, color="k", lw=0.5)
    axes[0, 0].legend(); fig.suptitle("1% TFP shock: tax vs cap (% deviation from steady state)")
    fig.tight_layout(); fig.savefig("figures/enk_tfp_tax_vs_cap.png", dpi=130)

    print("Std. dev. (%) under TFP shocks (sigma_a = 0.7%), RANK:")
    print(f"{'':>14}{'output':>9}{'hours':>9}{'emiss.':>9}{'infl.':>9}{'c. price':>10}")
    for name, m in [("carbon tax", tax), ("emissions cap", cap)]:
        s = m.simulate({"e_a": 0.007}, T=20_000)
        print(f"{name:>14}" + "".join(f"{100*np.std(s[v]):9.3f}" for v in ["y", "n", "em", "pi"])
              + f"{100*np.std(s['tau']):10.3f}")

    # ---- Experiment 2: a persistent 10% carbon-tax increase, RANK vs TANK -------------
    cases = [("RANK", dict(lam=0.0)),
             ("TANK, uniform rebate", dict(lam=0.3, rebate="uniform")),
             ("TANK, rebate to HtM", dict(lam=0.3, rebate="htm")),
             ("TANK, rebate to savers", dict(lam=0.3, rebate="savers"))]
    fig, axes = plt.subplots(2, 3, figsize=(13, 6))
    panels = [("y", "Output"), ("pi", "Inflation (q/q)"), ("r", "Policy rate (q/q)"),
              ("ch", "HtM consumption"), ("cs", "Saver consumption"), ("em", "Emissions")]
    for lab, kw in cases:
        r = build(regime="tax", **kw).irf("e_z", size=0.10, T=T)
        for ax, (v, title) in zip(axes.flat, panels):
            ax.plot(q, pct(r, v), label=lab); ax.set_title(title)
    for ax in axes.flat:
        ax.axhline(0, color="k", lw=0.5)
    axes[0, 0].legend(fontsize=8); fig.suptitle("Carbon tax +10%: who bears it depends on heterogeneity and recycling")
    fig.tight_layout(); fig.savefig("figures/enk_tax_shock_tank.png", dpi=130)

    # ---- Experiment 3: same tax shock, different monetary policy reactions ------------
    rules = [("phi_pi=1.5, phi_y=0.125", dict(phi_pi=1.5, phi_y=0.125)),
             ("hawkish: phi_pi=3", dict(phi_pi=3.0, phi_y=0.125)),
             ("dovish/accommodative: phi_pi=1.1, phi_y=0.5", dict(phi_pi=1.1, phi_y=0.5))]
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))
    for lab, kw in rules:
        r = build(regime="tax", lam=0.3, **kw).irf("e_z", size=0.10, T=T)
        for ax, (v, title) in zip(axes, [("y", "Output"), ("pi", "Inflation (q/q)"), ("ch", "HtM consumption")]):
            ax.plot(q, pct(r, v), label=lab); ax.set_title(title)
    for ax in axes:
        ax.axhline(0, color="k", lw=0.5)
    axes[0].legend(fontsize=8); fig.suptitle("Carbon tax +10% in TANK (lam=0.3): the monetary policy trade-off")
    fig.tight_layout(); fig.savefig("figures/enk_tax_shock_monpol.png", dpi=130)
    print("saved figures/enk_tfp_tax_vs_cap.png, enk_tax_shock_tank.png, enk_tax_shock_monpol.png")
