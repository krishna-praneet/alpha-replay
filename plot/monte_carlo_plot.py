import matplotlib.pyplot as plt
import os

# Read prices from file
def read_prices(filename):
    # Look in parent directory where C++ program runs
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(parent_dir, filename)
    
    with open(filepath) as f:
        return [float(line.strip()) for line in f if line.strip()]

call_prices = read_prices('call_simulated_prices.txt')
put_prices = read_prices('put_simulated_prices.txt')

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.hist(call_prices, bins=100, alpha=0.7, color='blue')
plt.title('Monte Carlo Simulated End Prices (Call)')
plt.xlabel('End Price (ST)')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
plt.hist(put_prices, bins=100, alpha=0.7, color='green')
plt.title('Monte Carlo Simulated End Prices (Put)')
plt.xlabel('End Price (ST)')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()