# Bakery-MDP

**Inventory Optimization Using a Markov Decision Process**

**Overview**

This project models a bakery inventory system as a Markov Decision Process (MDP) using real-world sales data.

The objective is to determine an optimal daily ordering policy that minimizes long-run operational costs by balancing:
- Holding costs
- Shortage costs
- Ordering costs

The model is solved using value iteration.

**Data Source**
- Kaggle: French Bakery Daily Sales
- Transaction-level sales data aggregated to daily demand
- Demand is discretized into finite states for tractability

**Model Description**

**State**
- Discrete demand level (low → high daily sales)

**Action**
- Number of units ordered at the start of the day

**Transition Probabilities**
- Estimated empirically from historical sales data

**Reward (Cost) Function**
- Cost = holding cost+shortage cost+ordering cost

**Solution Method** 

- Construct transition matrix from historical data
- Apply value iteration to compute:
  - Optimal value function
  - Optimal ordering policy
- Compute the steady-state distribution under the optimal policy
- Evaluate long-run average daily cost

**Project Structure**
```bash
bakery-mdp/
│── src/
│   ├── markov.py       
│   ├── analysis.py     
│── notebooks/
│   └── experiments.ipynb
│── data/
│   └── bakery_sales.csv
│── README.md
│── requirements.txt
```
**Results Interpretation**

- The optimal policy prescribes higher orders on high-demand states and conservative ordering otherwise
- The steady-state distribution reflects demand patterns in real data
- The reported average daily cost represents the long-run expected operational cost when following the optimal policy

**Technologies Used**

- Python
- NumPy
- Pandas
- Jupyter Notebooks
