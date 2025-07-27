import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

def cumulative_standard_normal(x):
    """Replicate the C++ cumulativeStandardNormal function"""
    # This is a simplified version - you might want to use the exact implementation from your C++ code
    return norm.cdf(x)

def black_scholes_call(S, K, T, r, sigma):
    """Calculate Black-Scholes call option price using the same logic as option_pricer.cpp"""
    d1 = (np.log(S/K) + (r + ((sigma * sigma) / 2)) * T) / (sigma * np.sqrt(T))
    d2 = d1 - (sigma * np.sqrt(T))
    
    call_price = S * cumulative_standard_normal(d1) - K * np.exp(-r * T) * cumulative_standard_normal(d2)
    return call_price

def black_scholes_put(S, K, T, r, sigma):
    """Calculate Black-Scholes put option price using the same logic as option_pricer.cpp"""
    d1 = (np.log(S/K) + (r + ((sigma * sigma) / 2)) * T) / (sigma * np.sqrt(T))
    d2 = d1 - (sigma * np.sqrt(T))
    
    put_price = K * np.exp(-r * T) * cumulative_standard_normal(-d2) - S * cumulative_standard_normal(-d1)
    return put_price

def plot_black_scholes_profit_loss():
    """Plot Black-Scholes profit/loss curves for different time to expiry"""
    
    # Parameters
    K = 100.0  # Strike price
    r = 0.05   # Risk-free rate
    sigma = 0.2  # Volatility
    
    # Time to expiry values
    T_values = [0.2, 0.4, 0.6, 0.8, 1.0]
    
    # Stock price range
    S_range = np.linspace(80, 120, 200)
    
    plt.figure(figsize=(15, 6))
    
    # Plot Call Option Profit/Loss
    plt.subplot(1, 2, 1)
    colors = ['red', 'orange', 'yellow', 'green', 'blue']
    
    for i, T in enumerate(T_values):
        call_prices = [black_scholes_call(S, K, T, r, sigma) for S in S_range]
        call_profit_loss = [call_price - black_scholes_call(K, K, T, r, sigma) for call_price in call_prices]
        
        plt.plot(S_range, call_profit_loss, color=colors[i], linewidth=2, 
                label=f'T = {T} years')
    
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.7, label='Break-even')
    plt.axvline(x=K, color='black', linestyle=':', alpha=0.7, label=f'Strike Price: {K}')
    plt.title('Call Option Profit/Loss vs Stock Price\n(At Different Time to Expiry)')
    plt.xlabel('Stock Price')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot Put Option Profit/Loss
    plt.subplot(1, 2, 2)
    
    for i, T in enumerate(T_values):
        put_prices = [black_scholes_put(S, K, T, r, sigma) for S in S_range]
        put_profit_loss = [put_price - black_scholes_put(K, K, T, r, sigma) for put_price in put_prices]
        
        plt.plot(S_range, put_profit_loss, color=colors[i], linewidth=2, 
                label=f'T = {T} years')
    
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.7, label='Break-even')
    plt.axvline(x=K, color='black', linestyle=':', alpha=0.7, label=f'Strike Price: {K}')
    plt.title('Put Option Profit/Loss vs Stock Price\n(At Different Time to Expiry)')
    plt.xlabel('Stock Price')
    plt.ylabel('Profit/Loss')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_greeks_vs_time():
    """Plot option Greeks vs time to expiry"""
    
    # Parameters
    S = 100.0  # Current stock price
    K = 100.0  # Strike price
    r = 0.05   # Risk-free rate
    sigma = 0.2  # Volatility
    
    # Time to expiry range
    T_range = np.linspace(0.1, 1.0, 100)
    
    plt.figure(figsize=(15, 10))
    
    # Calculate Greeks
    deltas_call = []
    deltas_put = []
    gammas = []
    thetas_call = []
    thetas_put = []
    vegas = []
    
    for T in T_range:
        d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma*np.sqrt(T)
        
        # Delta
        delta_call = norm.cdf(d1)
        delta_put = delta_call - 1
        deltas_call.append(delta_call)
        deltas_put.append(delta_put)
        
        # Gamma (same for call and put)
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        gammas.append(gamma)
        
        # Theta
        theta_call = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - 
                     r * K * np.exp(-r*T) * norm.cdf(d2))
        theta_put = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + 
                    r * K * np.exp(-r*T) * norm.cdf(-d2))
        thetas_call.append(theta_call)
        thetas_put.append(theta_put)
        
        # Vega (same for call and put)
        vega = S * np.sqrt(T) * norm.pdf(d1)
        vegas.append(vega)
    
    # Plot Delta
    plt.subplot(2, 2, 1)
    plt.plot(T_range, deltas_call, 'b-', linewidth=2, label='Call Delta')
    plt.plot(T_range, deltas_put, 'r-', linewidth=2, label='Put Delta')
    plt.title('Delta vs Time to Expiry')
    plt.xlabel('Time to Expiry (years)')
    plt.ylabel('Delta')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot Gamma
    plt.subplot(2, 2, 2)
    plt.plot(T_range, gammas, 'g-', linewidth=2, label='Gamma')
    plt.title('Gamma vs Time to Expiry')
    plt.xlabel('Time to Expiry (years)')
    plt.ylabel('Gamma')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot Theta
    plt.subplot(2, 2, 3)
    plt.plot(T_range, thetas_call, 'b-', linewidth=2, label='Call Theta')
    plt.plot(T_range, thetas_put, 'r-', linewidth=2, label='Put Theta')
    plt.title('Theta vs Time to Expiry')
    plt.xlabel('Time to Expiry (years)')
    plt.ylabel('Theta')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot Vega
    plt.subplot(2, 2, 4)
    plt.plot(T_range, vegas, 'purple', linewidth=2, label='Vega')
    plt.title('Vega vs Time to Expiry')
    plt.xlabel('Time to Expiry (years)')
    plt.ylabel('Vega')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Plotting Black-Scholes profit/loss curves...")
    plot_black_scholes_profit_loss()
    
    print("Plotting option Greeks vs time to expiry...")
    plot_greeks_vs_time() 