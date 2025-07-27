#include "option_pricer.h"
#include <iostream>
#include <fstream>
#include <cmath> // For exp and sqrt
#include <vector> // For vector
#include <random> // For random number generation

// Helper function for Monte Carlo simulation
double generateGaussianNoise(double mean, double stddev) {
    static std::mt19937 gen(std::random_device{}());
    std::normal_distribution<> d(mean, stddev);
    return d(gen);
}

// Placeholder for option payoff functions (replace with actual implementations)
double callOptionPayoff(double ST, double K) {
    return std::max(0.0, ST - K);
}

double putOptionPayoff(double ST, double K) {
    return std::max(0.0, K - ST);
}

double monteCarloOptionPricing(
    double S0, double K, double r, double sigma, double T,
    int numSimulations, bool isCallOption, const std::string& outputFile = "")
{
    double payoffSum = 0.0;
    std::vector<double> finalPrices;
    std::vector<std::vector<double>> pricePaths;

    // Number of time steps for the path
    int numSteps = 252; // Daily steps for 1 year
    double dt = T / numSteps;

    for (int i = 0; i < numSimulations; ++i) {
        std::vector<double> path;
        double St = S0;
        path.push_back(St);
        
        for (int step = 1; step <= numSteps; ++step) {
            double dW = generateGaussianNoise(0.0, 1.0) * std::sqrt(dt);
            St = St * std::exp((r - 0.5 * sigma * sigma) * dt + sigma * dW);
            path.push_back(St);
        }
        
        pricePaths.push_back(path);
        finalPrices.push_back(St);
        
        double payoff = isCallOption ? callOptionPayoff(St, K) : putOptionPayoff(St, K);
        payoffSum += payoff;
    }

    // Write price paths to file if requested
    if (!outputFile.empty()) {
        std::ofstream out(outputFile);
        for (const auto& path : pricePaths) {
            for (size_t i = 0; i < path.size(); ++i) {
                out << path[i];
                if (i < path.size() - 1) out << ",";
            }
            out << "\n";
        }
    }

    double averagePayoff = payoffSum / static_cast<double>(numSimulations);
    return std::exp(-r * T) * averagePayoff;
}

void generateBlackScholesData(double S0, double K, double r, double sigma) {
    std::ofstream outFile("black_scholes_data.txt");
    outFile << "S,K,T,r,sigma,call_price,put_price\n";
    
    // Stock price range
    std::vector<double> S_values;
    for (double S = 80.0; S <= 120.0; S += 1.0) {
        S_values.push_back(S);
    }
    
    // Time to expiry values
    std::vector<double> T_values = {0.2, 0.4, 0.6, 0.8, 1.0};
    
    for (double T : T_values) {
        for (double S : S_values) {
            OptionPricer pricer(S, K, r, sigma, T);
            Contract callContract = pricer.price(true);
            Contract putContract = pricer.price(false);
            
            outFile << S << "," << K << "," << T << "," << r << "," << sigma 
                   << "," << callContract.premium << "," << putContract.premium << "\n";
        }
    }
    outFile.close();
    std::cout << "Black-Scholes data saved to black_scholes_data.txt" << std::endl;
}

int main() {
    // Option parameters
    double S0 = 100.0;   // Initial stock price
    double K = 100.0;    // Strike price
    double r = 0.05;     // Risk-free rate
    double sigma = 0.2;  // Volatility
    double T = 1;        // Time to maturity (in years)

    int numSimulations = 100000; // Number of Monte Carlo simulations

    OptionPricer pricer(S0, K, r, sigma, T);
    Contract callContract = pricer.price(true);
    Contract putContract = pricer.price(false);

    std::cout << "European Call Option Price: " << callContract.premium << ", dte: " << callContract.dte << ", delta: " << callContract.delta << ", gamma: " << callContract.gamma << ", theta: " << callContract.theta << ", vega: " << callContract.vega  << ", rho: " << callContract.rho << ", implied volatility: " << callContract.implied_volatility  << ", intrinsic value: " << callContract.intrinsic_value << std::endl;
    std::cout << "European Put Option Price: " << putContract.premium << ", dte: " << putContract.dte << ", delta: " << putContract.delta << ", gamma: " << putContract.gamma << ", theta: " << putContract.theta << ", vega: " << putContract.vega << ", rho: " << putContract.rho << ", implied volatility: " << putContract.implied_volatility  << ", intrinsic value: " << putContract.intrinsic_value << std::endl;

    // Monte Carlo simulation for European Call Option
    double callPrice = monteCarloOptionPricing(S0, K, r, sigma, T, numSimulations, true, "call_simulated_prices.txt");
    std::cout << "Monte Carlo European Call Option Price: " << callPrice << std::endl;

    // Monte Carlo simulation for European Put Option
    double putPrice = monteCarloOptionPricing(S0, K, r, sigma, T, numSimulations, false, "put_simulated_prices.txt");
    std::cout << "Monte Carlo European Put Option Price: " << putPrice << std::endl;

    // Generate Black-Scholes data for plotting
    generateBlackScholesData(S0, K, r, sigma);

    return 0;
} 