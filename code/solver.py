"""
Minimal first-order perturbation toolkit for DSGE models (a tiny "Dynare in Python").

A model is a residual function

    f(yp, y, ym, e) = 0          (n equations, n endogenous variables)

where yp = y_{t+1}, y = y_t, ym = y_{t-1}, e = shocks. We

  1. find the deterministic steady state  f(ys, ys, ys, 0) = 0,
  2. linearize:  A dy_{t+1} + B dy_t + C dy_{t-1} + D e_t = 0  (E_t implicit),
  3. solve for the stable recursive law of motion  dy_t = P dy_{t-1} + Q e_t
     with a QZ (generalized Schur) decomposition, checking Blanchard-Kahn.

If variables are written in logs inside f, then dy are log-deviations
(i.e. approximately % deviations from steady state).
"""
import numpy as np
from scipy.linalg import ordqz, solve
from scipy.optimize import root


def jacobians(f, ys, n_shocks, h=1e-6):
    """Numerical Jacobians of f w.r.t. y_{t+1}, y_t, y_{t-1}, e (central differences)."""
    n = len(ys)
    e0 = np.zeros(n_shocks)

    def jac(which, dim):
        J = np.zeros((n, dim))
        for j in range(dim):
            args_p = [ys.copy(), ys.copy(), ys.copy(), e0.copy()]
            args_m = [ys.copy(), ys.copy(), ys.copy(), e0.copy()]
            args_p[which][j] += h
            args_m[which][j] -= h
            J[:, j] = (f(*args_p) - f(*args_m)) / (2 * h)
        return J

    return jac(0, n), jac(1, n), jac(2, n), jac(3, n_shocks)


def solve_linear(A, B, C, D, tol=1e-9):
    """Solve A E_t y_{t+1} + B y_t + C y_{t-1} + D e_t = 0 for y_t = P y_{t-1} + Q e_t.

    Companion form with x_t = [y_{t-1}; y_t]:
        [I 0; 0 A] x_{t+1} = [0 I; -C -B] x_t
    A unique stable solution requires exactly n generalized eigenvalues
    inside the unit circle (Blanchard-Kahn).
    """
    n = A.shape[0]
    I, Z0 = np.eye(n), np.zeros((n, n))
    E = np.block([[I, Z0], [Z0, A]])
    F = np.block([[Z0, I], [-C, -B]])
    # F v = lambda E v ; put |lambda| < 1 first
    S, T, alpha, beta, Qz, Zz = ordqz(F, E, sort="iuc", output="complex")
    with np.errstate(divide="ignore", invalid="ignore"):
        eig = np.where(np.abs(beta) > tol, np.abs(alpha / np.where(beta == 0, 1, beta)), np.inf)
    n_stable = int(np.sum(eig < 1 - tol))
    if n_stable != n:
        msg = "indeterminacy (too many stable roots)" if n_stable > n else "no stable solution (too few stable roots)"
        raise ValueError(f"Blanchard-Kahn violated: {n_stable} stable roots for {n} variables -> {msg}")
    Z11, Z21 = Zz[:n, :n], Zz[n:, :n]
    P = np.real(Z21 @ np.linalg.inv(Z11))
    Q = -solve(A @ P + B, D)
    return P, Q, np.sort(eig)


class Model:
    """Container: names, residual function, steady state, linear solution."""

    def __init__(self, var_names, shock_names, f, ys_guess):
        self.var_names = list(var_names)
        self.shock_names = list(shock_names)
        self.f = f
        self.idx = {v: i for i, v in enumerate(self.var_names)}
        self.ys = self.steady_state(np.asarray(ys_guess, dtype=float))
        self.A, self.B, self.C, self.D = jacobians(f, self.ys, len(self.shock_names))
        self.P, self.Q, self.eigs = solve_linear(self.A, self.B, self.C, self.D)

    def steady_state(self, guess):
        e0 = np.zeros(len(self.shock_names))
        g = lambda y: self.f(y, y, y, e0)
        if np.max(np.abs(g(guess))) < 1e-10:
            return guess
        sol = root(g, guess, method="hybr", options={"xtol": 1e-12})
        if not sol.success or np.max(np.abs(g(sol.x))) > 1e-8:
            raise RuntimeError(f"steady state not found: {sol.message}")
        return sol.x

    def irf(self, shock, size=1.0, T=40):
        """Impulse responses (deviations from steady state) to a one-off shock at t=0."""
        e = np.zeros(len(self.shock_names))
        e[self.shock_names.index(shock)] = size
        out = np.zeros((T, len(self.var_names)))
        out[0] = self.Q @ e
        for t in range(1, T):
            out[t] = self.P @ out[t - 1]
        return {v: out[:, i] for v, i in self.idx.items()}

    def simulate(self, sigmas, T=10_000, seed=0, burn=500):
        rng = np.random.default_rng(seed)
        y = np.zeros(len(self.var_names))
        out = np.zeros((T, len(self.var_names)))
        sig = np.array([sigmas.get(s, 0.0) for s in self.shock_names])
        for t in range(T + burn):
            y = self.P @ y + self.Q @ (sig * rng.standard_normal(len(sig)))
            if t >= burn:
                out[t - burn] = y
        return {v: out[:, i] for v, i in self.idx.items()}

    def ss(self, name):
        return self.ys[self.idx[name]]
