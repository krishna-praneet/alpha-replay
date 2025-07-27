import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

def read_price_paths(filename):
    """Read price paths from CSV file"""
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(parent_dir, filename)
    
    paths = []
    with open(filepath, 'r') as f:
        for line in f:
            path = [float(x) for x in line.strip().split(',')]
            paths.append(path)
    return paths

def plot_price_paths(call_paths, put_paths, S0, K, T):
    """Plot price paths showing evolution from initial to final prices"""
    
    # Create time axis (daily steps for 1 year)
    num_steps = len(call_paths[0]) if call_paths else 252
    time_axis = np.linspace(0, T, num_steps)
    
    plt.figure(figsize=(12, 8))
    
    # Plot stock price paths (same for both call and put options)
    plt.subplot(2, 1, 1)
    for i, path in enumerate(call_paths[:50]):  # Plot first 50 paths for clarity
        plt.plot(time_axis, path, alpha=0.6, color='blue', linewidth=0.8)
    plt.axhline(y=S0, color='black', linestyle='--', alpha=0.7, label=f'Initial Price: {S0}')
    plt.axhline(y=K, color='red', linestyle='--', alpha=0.7, label=f'Strike Price: {K}')
    plt.title('Monte Carlo Stock Price Paths')
    plt.xlabel('Time (years)')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Calculate option payoffs and profit/loss
    call_payoffs = []
    put_payoffs = []
    call_profit_loss = []
    put_profit_loss = []
    
    # Estimate option premiums (you can replace these with actual calculated premiums)
    # For now, using rough estimates based on Black-Scholes approximation
    call_premium = 10.0  # Rough estimate for call option premium
    put_premium = 10.0   # Rough estimate for put option premium
    
    for path in call_paths:
        final_price = path[-1]
        call_payoff = max(0, final_price - K)  # Call payoff: max(0, S_T - K)
        put_payoff = max(0, K - final_price)   # Put payoff: max(0, K - S_T)
        
        # Calculate profit/loss: payoff - premium paid
        call_pl = call_payoff - call_premium
        put_pl = put_payoff - put_premium
        
        call_payoffs.append(call_payoff)
        put_payoffs.append(put_payoff)
        call_profit_loss.append(call_pl)
        put_profit_loss.append(put_pl)
    
    # Calculate profit/loss percentages
    call_profitable = sum(1 for pl in call_profit_loss if pl > 0)
    call_losing = sum(1 for pl in call_profit_loss if pl <= 0)
    call_profit_pct = (call_profitable / len(call_profit_loss)) * 100
    call_loss_pct = (call_losing / len(call_profit_loss)) * 100
    
    put_profitable = sum(1 for pl in put_profit_loss if pl > 0)
    put_losing = sum(1 for pl in put_profit_loss if pl <= 0)
    put_profit_pct = (put_profitable / len(put_profit_loss)) * 100
    put_loss_pct = (put_losing / len(put_profit_loss)) * 100
    
    # Plot call option profit/loss distribution
    plt.subplot(2, 2, 3)
    plt.hist(call_profit_loss, bins=50, alpha=0.7, color='blue', density=True)
    plt.axvline(x=0, color='red', linestyle='--', alpha=0.7, label='Break-even (No Profit/Loss)')
    plt.title(f'Call Option \nProfitable: {call_profit_pct:.1f}% | Loss: {call_loss_pct:.1f}%')
    plt.xlabel('Profit/Loss per Contract')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot put option profit/loss distribution
    plt.subplot(2, 2, 4)
    plt.hist(put_profit_loss, bins=50, alpha=0.7, color='green', density=True)
    plt.axvline(x=0, color='red', linestyle='--', alpha=0.7, label='Break-even (No Profit/Loss)')
    plt.title(f'Put Option \nProfitable: {put_profit_pct:.1f}% | Loss: {put_loss_pct:.1f}%')
    plt.xlabel('Profit/Loss per Contract')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def main():
    # Parameters (should match your C++ program)
    S0 = 100.0  # Initial stock price
    K = 100.0   # Strike price
    T = 1.0     # Time to maturity
    
    try:
        # Read price paths
        call_paths = read_price_paths('call_simulated_prices.txt')
        put_paths = read_price_paths('put_simulated_prices.txt')
        
        print(f"Loaded {len(call_paths)} call option price paths")
        print(f"Loaded {len(put_paths)} put option price paths")
        
        # Plot the paths
        plot_price_paths(call_paths, put_paths, S0, K, T)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure to run the C++ program first to generate the price path files.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 