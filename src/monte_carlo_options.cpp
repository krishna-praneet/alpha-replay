#include "../include/monte_carlo_options.h"
#include <cmath>
#include <random>
#include <algorithm>
#include <fstream>
#include <vector>

// Function to generate normally distributed random numbers
double generateGaussianNoise(double mean, double stddev) {
    static std::mt19937 generator(std::random_device{}());
    std::normal_distribution<double> distribution(mean, stddev);
    return distribution(generator);
}

// Function to calculate the payoff of a European call option
double callOptionPayoff(double S, double K) {
    return std::max(S - K, 0.0);
}

// Function to calculate the payoff of a European put option
double putOptionPayoff(double S, double K) {
    return std::max(K - S, 0.0);
}

// Monte Carlo Simulation for European option pricing
double monteCarloOptionPricing(
    double S0, double K, double r, double sigma, double T,
    int numSimulations, bool isCallOption, const std::string& outputFile = "")
{
    double payoffSum = 0.0;
    std::vector<double> prices;

    for (int i = 0; i < numSimulations; ++i) {
        double ST = S0 * std::exp((r - 0.5 * sigma * sigma) * T +
                                  sigma * std::sqrt(T) * generateGaussianNoise(0.0, 1.0));
        prices.push_back(ST);
        double payoff = isCallOption ? callOptionPayoff(ST, K) : putOptionPayoff(ST, K);
        payoffSum += payoff;
    }

    // Write prices to file if requested
    if (!outputFile.empty()) {
        std::ofstream out(outputFile);
        for (double price : prices) {
            out << price << "\\n";
        }
    }

    double averagePayoff = payoffSum / static_cast<double>(numSimulations);
    return std::exp(-r * T) * averagePayoff;
} 