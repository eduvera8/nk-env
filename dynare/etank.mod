// =====================================================================
// E-TANK: Environmental New Keynesian model with hand-to-mouth households
// Dynare version of code/enk.py (same equations, same calibration).
// All endogenous variables are in logs -> IRFs are log-deviations.
//
// Usage (Dynare >= 5):   dynare etank.mod
//   switch regime / heterogeneity with the macro flags below, e.g.
//   dynare etank.mod -DCAP=1 -DLAM=0.3 -DREBATE=2
// =====================================================================

@#ifndef CAP
  @#define CAP = 0          // 0 = carbon tax, 1 = emissions cap (permit price endogenous)
@#endif
@#ifndef LAM
  @#define LAM = 0.0        // share of hand-to-mouth households
@#endif
@#ifndef REBATE
  @#define REBATE = 1       // 1 = uniform per capita, 2 = all to HtM, 3 = all to savers
@#endif

var cs ch ns nh w y mc pi r pstar x1 x2 disp u tau em x a z v c n;
varexo e_a e_z e_v;

parameters beta sigma phi eps theta lam chi
           phi_pi phi_y rho_i
           varphi theta1 theta2 delta_x E_row gamma_d tau_bar Em_bar
           rho_a rho_z rho_v sh ss_;

// ---------------- calibration (same as code/enk.py) ------------------
beta = 0.99; sigma = 1; phi = 1; eps = 6; theta = 0.75;
lam = @{LAM};
phi_pi = 1.5; phi_y = 0.125; rho_i = 0;
varphi = 1; theta1 = 0.05607; theta2 = 2.8;
delta_x = 0.0021;
rho_a = 0.95; rho_z = 0.95; rho_v = 0.5;

// closed-form RANK steady state, used to calibrate chi, tau_bar, E_row, gamma_d
U_   = 0.20;  N_ = 1/3;  dom_share = 0.10;  damage_ss = 0.005;
tau_bar = theta1*theta2*U_^(theta2-1)/varphi;
mc_  = (eps-1)/eps;
Y_   = (1-damage_ss)*N_;
w_   = (mc_ - theta1*U_^theta2 - tau_bar*varphi*(1-U_))*(1-damage_ss);
C_   = Y_*(1-theta1*U_^theta2);
chi  = w_/(N_^phi*C_^sigma);
Em_bar = varphi*(1-U_)*Y_;
E_row  = Em_bar*(1-dom_share)/dom_share;
X_   = (Em_bar+E_row)/delta_x;
gamma_d = -log(1-damage_ss)/X_;

// rebate shares (per-capita transfer to HtM = sh*rev, to savers = ss_*rev)
@#if REBATE == 1
  sh = 1; ss_ = 1;
@#elseif REBATE == 2
  sh = 1/max(lam,1e-8); ss_ = 0;
@#else
  sh = 0; ss_ = 1/(1-lam);
@#endif

model;
  // auxiliary (model-local) variables
  # dmg  = 1 - exp(-gamma_d*exp(x));
  # prod = exp(a)*(1-dmg);
  # rev  = exp(tau)*exp(em);
  # Lam  = exp(cs)^(-sigma);
  # Lamp = exp(cs(+1))^(-sigma);

  [name='Savers Euler']
  log(beta) - sigma*(cs(+1)-cs) + r - pi(+1) = 0;
  [name='Savers labor supply']
  log(chi) + phi*ns + sigma*cs = w;
  [name='HtM labor supply']
  log(chi) + phi*nh + sigma*ch = w;
  [name='HtM budget']
  exp(ch) = exp(w)*exp(nh) + sh*rev;
  exp(c) = lam*exp(ch) + (1-lam)*exp(cs);
  exp(n) = lam*exp(nh) + (1-lam)*exp(ns);
  [name='Resource constraint']
  exp(y) = exp(c) + theta1*exp(u)^theta2*exp(y)*exp(disp);
  [name='Production']
  y + disp = log(prod) + n;
  [name='Real marginal cost']
  exp(mc) = exp(w)/prod + theta1*exp(u)^theta2 + exp(tau)*varphi*(1-exp(u));
  [name='Abatement FOC']
  theta1*theta2*exp(u)^(theta2-1) = exp(tau)*varphi;
  [name='Emissions']
  exp(em) = varphi*(1-exp(u))*exp(y)*exp(disp);
  [name='Pollution stock']
  exp(x) = (1-delta_x)*exp(x(-1)) + exp(em) + E_row;
  [name='Environmental policy']
@#if CAP == 0
  tau = log(tau_bar) + z;
@#else
  em = log(Em_bar) + z;
@#endif
  z = rho_z*z(-1) + e_z;
  a = rho_a*a(-1) + e_a;
  v = rho_v*v(-1) + e_v;
  [name='Calvo: x1']
  exp(x1) = Lam*exp(mc)*exp(y) + beta*theta*exp(pi(+1))^eps*exp(x1(+1));
  [name='Calvo: x2']
  exp(x2) = Lam*exp(y) + beta*theta*exp(pi(+1))^(eps-1)*exp(x2(+1));
  pstar = log(eps/(eps-1)) + x1 - x2;
  1 = theta*exp(pi)^(eps-1) + (1-theta)*exp(pstar)^(1-eps);
  exp(disp) = theta*exp(pi)^eps*exp(disp(-1)) + (1-theta)*exp(pstar)^(-eps);
  [name='Taylor rule']
  r = rho_i*r(-1) + (1-rho_i)*(-log(beta) + phi_pi*pi + phi_y*(y - STEADY_STATE(y))) + v;
end;

initval;
  cs = log(C_); ch = log(C_); ns = log(N_); nh = log(N_); w = log(w_); y = log(Y_);
  mc = log(mc_); pi = 0; r = -log(beta); pstar = 0; disp = 0;
  x1 = log(C_^(-sigma)*mc_*Y_/(1-beta*theta)); x2 = log(C_^(-sigma)*Y_/(1-beta*theta));
  u = log(U_); tau = log(tau_bar); em = log(Em_bar); x = log(X_); a = 0; z = 0; v = 0;
  c = log(C_); n = log(N_);
end;

steady;
check;

shocks;
  var e_a; stderr 0.007;
  var e_z; stderr 0.10;
  var e_v; stderr 0.0025;
end;

stoch_simul(order=1, irf=24, nograph) y c ch cs n pi r em tau u;

// IRFs are stored in oo_.irfs, e.g. oo_.irfs.y_e_z (response of log output to a 1-s.d. carbon-tax shock)
save('etank_results.mat', 'oo_', 'M_');
