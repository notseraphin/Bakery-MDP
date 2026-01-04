# src/analysis.py
import matplotlib.pyplot as plt
import numpy as np

def plot_policy(policy):
    plt.figure(figsize=(6,4))
    plt.bar(np.arange(len(policy)), policy, color='skyblue')
    plt.xlabel('Demand state')
    plt.ylabel('Optimal order quantity')
    plt.title('Optimal Policy by Demand State')
    plt.show()

def plot_steady_state(stationary):
    plt.figure(figsize=(6,4))
    plt.bar(np.arange(len(stationary)), stationary, color='salmon')
    plt.xlabel('Demand state')
    plt.ylabel('Steady-state probability')
    plt.title('Steady-State Distribution')
    plt.show()
