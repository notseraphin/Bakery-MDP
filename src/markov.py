# src/markov.py
import pandas as pd
import numpy as np

class BakeryMDP:
    def __init__(self, csv_path, num_states=10, max_order=5, holding_cost=1, shortage_cost=50, order_cost=2, gamma=0.95):
        """
        Data-driven Markov Decision Process for bakery inventory optimization.
        """
        #  Load and standardize CSV
        self.df = pd.read_csv(csv_path)
        self.df.columns = [c.strip().lower() for c in self.df.columns]  # lowercase columns
        if 'date' not in self.df.columns or 'quantity' not in self.df.columns:
            raise ValueError("CSV must contain 'date' and 'quantity' columns (case-insensitive)")

        self.num_states = num_states
        self.max_order = max_order
        self.states = np.arange(num_states)
        self.actions = np.arange(max_order + 1)
        self.holding_cost = holding_cost
        self.shortage_cost = shortage_cost
        self.order_cost = order_cost
        self.gamma = gamma

        # Compute daily total sales 
        daily_sales = self.df.groupby('date')['quantity'].sum()
        self.daily_sales = daily_sales.values
        self.max_sales = daily_sales.max()

        # Discretize into states 
        self.state_bins = np.linspace(0, self.max_sales, num_states + 1)
        self.sales_states = np.digitize(self.daily_sales, self.state_bins, right=True) - 1
        self.sales_states = np.clip(self.sales_states, 0, num_states - 1)

        # Build transition matrix from data 
        self.P = self.build_transition_matrix()

    def build_transition_matrix(self):
        counts = np.zeros((self.num_states, self.num_states))
        for t in range(len(self.sales_states) - 1):
            s = self.sales_states[t]
            s_next = self.sales_states[t + 1]
            counts[s, s_next] += 1
        # Normalize rows to probabilities
        P = counts / counts.sum(axis=1, keepdims=True)
        P[np.isnan(P)] = 0  # handle rows with no outgoing transitions
        return P

    def reward(self, s, a):
        """
        Negative expected cost = order cost + holding + shortage
        """
        new_inventory = min(s + a, self.num_states - 1)
        # Expected shortage and holding
        expected_shortage = sum(max(next_s - new_inventory, 0) * p for next_s, p in enumerate(self.P[s]))
        expected_holding = sum(min(next_s, new_inventory) * p for next_s, p in enumerate(self.P[s]))
        cost = self.order_cost * a + self.holding_cost * expected_holding + self.shortage_cost * expected_shortage
        return -cost

    def value_iteration(self, tol=1e-5, max_iter=1000):
        V = np.zeros(self.num_states)
        policy = np.zeros(self.num_states, dtype=int)

        for _ in range(max_iter):
            V_new = np.zeros_like(V)
            for s in self.states:
                action_values = []
                for a in self.actions:
                    r = self.reward(s, a)
                    action_value = r + self.gamma * np.dot(self.P[s], V)
                    action_values.append(action_value)
                best_a = np.argmax(action_values)
                V_new[s] = action_values[best_a]
                policy[s] = best_a
            if np.max(np.abs(V_new - V)) < tol:
                break
            V = V_new
        return V, policy
