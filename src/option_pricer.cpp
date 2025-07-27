#include "option_pricer.h"
#include <cmath>
#include <algorithm>

OptionPricer::OptionPricer(double S0, double K, double r, double sigma, double T)
    : S0(S0), K(K), r(r), sigma(sigma), T(T) {}



Contract OptionPricer::price(bool isCallOption) const {
    Contract con;
    int days_till_expiry = T * 365.2425;
    con.dte = days_till_expiry;
    double d1 = (log(S0/K) + (r + ((sigma * sigma) / 2)) * T) / (sigma * std::sqrt(T));
    double d2 = d1 - (sigma * std::sqrt(T));
    if (isCallOption) {
        con.premium = S0 * cumulativeStandardNormal(d1) - K * std::exp(-r * T) * cumulativeStandardNormal(d2);
        con.delta = cumulativeStandardNormal(d1);
        con.gamma = cumulativeStandardNormal(d1) / (S0 * sigma * std::sqrt(T));
        con.theta = (-(S0 * cumulativeStandardNormal(d1) * sigma) / (2 * std::sqrt(T))) - (r * K * std::exp(-r * T) * cumulativeStandardNormal(d2));
        con.vega = S0 * cumulativeStandardNormal(d1) * std::sqrt(T);
        con.rho = K * T * std::exp(-r * T) * cumulativeStandardNormal(d2);
        con.implied_volatility = sigma - ((con.premium - (con.premium - 0.01))/(con.vega));
        con.intrinsic_value = std::max(S0 - K, 0.0);
    } else {
        con.premium = K * std::exp(-r * T) * cumulativeStandardNormal(-d2) - S0 * cumulativeStandardNormal(-d1);
        con.delta = cumulativeStandardNormal(d1) - 1;
        con.gamma = cumulativeStandardNormal(d1) / (S0 * sigma * std::sqrt(T));
        con.theta = (-(S0 * cumulativeStandardNormal(d1) * sigma) / (2 * std::sqrt(T))) + (r * K * std::exp(-r * T) * cumulativeStandardNormal(-d2));
        con.vega = S0 * cumulativeStandardNormal(d1) * std::sqrt(T);
        con.rho = -K * T * std::exp(-r * T) * cumulativeStandardNormal(-d2);
        con.implied_volatility = sigma - (((con.premium - 0.01) - con.premium)/(con.vega));
        con.intrinsic_value = std::max(K - S0, 0.0);
    }
    return con;
} 