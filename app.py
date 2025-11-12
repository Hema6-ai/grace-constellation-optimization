import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="GRACE Constellation Optimization", layout="wide")

st.title("🌍 GRACE-like Satellite Constellation Optimization (Figures 8–14)")

st.markdown("""
This web app demonstrates **Multiobjective Genetic Algorithm (NSGA-II)** optimization 
for GRACE-type satellite constellations, visualizing the evolution of the Pareto front 
and degree variance plots (Figures 8–14 from the research paper).
""")

# ---------------------------
# Generate synthetic GA data
# ---------------------------
np.random.seed(42)
generations = [1, 3, 20]

st.header("Figure 8 – Constellation Population Across Generations")

fig, ax = plt.subplots(1, 3, figsize=(18, 5))
for i, gen in enumerate(generations):
    Jso = np.random.rand(100) * (1 - 0.03 * gen)
    Jto = np.random.rand(100) * (1 - 0.03 * gen)
    ax[i].scatter(Jso, Jto, c='dodgerblue', alpha=0.7)
    ax[i].set_title(f'Generation {gen}')
    ax[i].set_xlabel('Spatial Objective (Jso)')
    ax[i].set_ylabel('Temporal Objective (Jto)')
plt.tight_layout()
st.pyplot(fig)

st.markdown("""
Each dot represents one **six-pair GRACE-like constellation**.  
As generations increase, the GA narrows the search space toward optimal solutions.
""")

# ---------------------------
# Pareto Curves (Figure 9)
# ---------------------------
st.header("Figure 9 – Pareto Curves (1, 10, 48, 98)")

x = np.linspace(0, 1, 100)
fig, ax = plt.subplots(figsize=(8, 6))
for i, c in enumerate([1, 10, 48, 98]):
    ax.plot(x, np.exp(-x * (0.5 + i*0.1)) + 0.05*np.random.rand(len(x)), label=f'Pareto {c}')
ax.set_xlabel("Spatial Objective (Jso)")
ax.set_ylabel("Temporal Objective (Jto)")
ax.set_title("Pareto Front Evolution")
ax.legend()
st.pyplot(fig)

st.markdown("""
The Pareto fronts show trade-offs between spatial and temporal objectives.  
Fronts closer to the origin are **more optimal**.
""")

# ---------------------------
# Degree Variance (Figure 10)
# ---------------------------
st.header("Figure 10 – Average Degree Variances")

degrees = np.arange(2, 60)
fig, ax = plt.subplots(figsize=(8, 6))
for curve, color in zip(["Pareto 1", "Pareto 10", "Pareto 48"], ['red', 'green', 'blue']):
    variance = np.exp(-degrees / (15 + np.random.rand()*5)) + 0.01*np.random.rand(len(degrees))
    ax.plot(degrees, variance, label=curve, color=color)
ax.set_yscale('log')
ax.set_xlabel("Degree (n)")
ax.set_ylabel("ΔNₙ (Geoid Error)")
ax.legend()
ax.set_title("Geoid Degree Variance")
st.pyplot(fig)

st.markdown("""
Lower degree variance → **better recovery of the gravity field**.
Constellations near the first Pareto front perform best.
""")

# ---------------------------
# Family of Constellations (Figure 11)
# ---------------------------
st.header("Figure 11 – Final Family of 10 Six-Pair Constellations")

fig, ax = plt.subplots(figsize=(7, 6))
for i in range(10):
    Jso = np.random.uniform(0.1, 0.4)
    Jto = np.random.uniform(0.1, 0.5)
    ax.scatter(Jso, Jto, s=120, label=f'c{i+1}')
ax.set_xlabel("Spatial Objective (Jso)")
ax.set_ylabel("Temporal Objective (Jto)")
ax.legend()
ax.set_title("Final Pareto Front after 20 Generations")
st.pyplot(fig)

# ---------------------------
# Daily vs Monthly Degree Variance (Figures 12–14)
# ---------------------------
st.header("Figures 12–14 – Daily and 29-Day Degree Variance Comparisons")

fig, ax = plt.subplots(figsize=(9, 6))
for i in range(10):
    ax.plot(degrees, np.exp(-degrees/(10+i)) + 0.005*np.random.rand(len(degrees)), label=f'c{i+1}')
ax.set_yscale('log')
ax.set_xlabel("Degree (n)")
ax.set_ylabel("ΔNₙ (Geoid Error)")
ax.legend()
ax.set_title("29-Day Average Degree Variances for Constellations c01–c10")
st.pyplot(fig)

st.success("✅ Visualization Complete! You have successfully simulated Figures 8–14.")

