# Option Pricing with Black-Scholes Model

This project contains a simple C++ implementation of the Black-Scholes model for pricing European call and put options. The implementation calculates various option Greeks and other relevant parameters.

## Notes

- This implementation uses an approximation for the error function (erf), which might introduce minor inaccuracies in the cumulative standard normal distribution calculation.
- The program assumes the input parameters are valid and does not include extensive error handling.
- Feel free to modify/extend!
  
## Features

- Models the underlying using Monte-Carlo strategy
- Calculates the premium of European call and put options.
- Computes option Greeks: Delta, Gamma, Theta, Vega, and Rho.
- Calculates the implied volatility.
- Determines the intrinsic value of the options.

## Getting Started

### Prerequisites

- C++ compiler (e.g., g++, clang++)
- Standard C++ Library

### Compilation

To compile the code, use the following command:

```sh
g++ -o option_pricing main.cpp -lm
```

### Running the Program

After compiling the code, you can run the program using:

```sh
./option_pricing
```

### Example Output

The program calculates the option prices and Greeks for a sample set of input parameters and prints the results:

```sh
European Call Option Price: 10.4506, dte: 365, delta: 0.6368, gamma: 0.0189, theta: -6.4157, vega: 37.5764, rho: 53.2325, implied volatility: 0.2000, intrinsic value: 0.0000
European Put Option Price: 5.5735, dte: 365, delta: -0.3632, gamma: 0.0189, theta: -1.9332, vega: 37.5764, rho: -41.8905, implied volatility: 0.2000, intrinsic value: 0.0000
```

## Project Structure

- include/         # Header files (classes, interfaces)
- src/             # Source files (implementations)
- simulators/      # Simulation scripts and experiments
- CMakeLists.txt   # CMake build configuration
- README.md        # Project documentation

## Building with CMake

1. Install CMake (https://cmake.org/download/)
2. From the project root, run:

```sh
mkdir build
cd build
cmake ..
make
```

3. Run the executable (e.g., `./OptionPricingDemo`)

---
Thanks!
