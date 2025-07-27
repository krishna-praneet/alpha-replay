#include "../include/monte_carlo_options.h"
#include <iostream>

int main() {
    // Option parameters
    double S0 = 100.0;   // Initial stock price
    double K = 100.0;    // Strike price
    double r = 0.05;     // Risk-free rate
    double sigma = 0.2;  // Volatility
    double T = 1;      // Time to maturity (1 year)
    int numSimulations = 100000; // Number of simulations

    // Calculate option prices
    double callPrice = monteCarloOptionPricing(S0, K, r, sigma, T, numSimulations, true);
    double putPrice = monteCarloOptionPricing(S0, K, r, sigma, T, numSimulations, false);

    // Output the results
    std::cout << "European Call Option Price: " << callPrice << std::endl;
    std::cout << "European Put Option Price: " << putPrice << std::endl;

    return 0;
}