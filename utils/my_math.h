#include<iostream>
#include<cmath>

static double OptionPricer::erf(double x) {
    const double A1 = 0.254829592;
    const double A2 = -0.284496736;
    const double A3 = 1.421413741;
    const double A4 = -1.453152027;
    const double A5 = 1.061405429;
    const double P = 0.3275911;
    int sign = (x >= 0) ? 1 : -1;
    x = fabs(x);
    double t = 1.0 / (1.0 + P * x);
    double y = 1.0 - (((((A5 * t + A4) * t) + A3) * t + A2) * t + A1) * t * exp(-x * x);
    return sign * y;
}

static double cumulativeStandardNormal(double x) {
    return 0.5 * (1.0 + erf(x / sqrt(2.0)));
}