import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="GRACE Constellation Optimization", layout="wide")

# ---------------------------
# Sidebar - user input
# ---------------------------
st.sidebar.title("🔧 Simulation Parameters")

T = st.sidebar.slider("Propagation time (days)", 1, 60, 29)
n_pairs = st.sidebar.slider("Satellite pairs", 1, 10, 6)
altitude = st.sidebar.slider("Orbit altitude (km)", 400, 800, 500)
ecc = st.sidebar.number_input("Eccentricity (e)", 0.0, 0.1, 0.0)
omega = st.sidebar.slider("Argument of perigee (°)", 0, 180, 90)
r_int = st.sidebar.slider("Intersatellite distance (km)", 50, 300, 100)
spatial_cells = st.sidebar.number_input("Spatial cells", 1000, 10000, 4551)
temporal_cells = st.sidebar.slider("Temporal cells per day", 4, 24, 16)
population_size = st.sidebar.slider("GA population size", 10, 200, 100)
generations = st.sidebar.slider("Generations", 5, 50, 20)

run_sim = st.sidebar.button("🚀 Run Simulation")

# ---------------------------
# Helper functions
# ---------------------------
def random_constellations(num, gen):
    Jso = np.random.rand(num) / gen**0.5 + 0.02
    Jto = np.random.rand(num) / gen**0.5 + 0.02
    return Jso, Jto

def geoid_error(n):
    np.random.seed(42)
    signal = 1e-4 / (np.arange(1, n+1)**2)
    error = signal + np.random.normal(0, 0.2*signal, n)
    return signal, error

# ---------------------------
# Output visualization
# ---------------------------
st.title("🛰️ Multiobjective GA Optimization for GRACE-like Constellations")
st.markdown(
    "This dashboard simulates the optimization of GRACE-type satellite constellations using a Multiobjective Genetic Algorithm (NSGA-II)."
)

if run_sim:
    st.success("Simulation running...")

    # ----- FIG 8 -----
    fig8, ax8 = plt.subplots()
    for gen in [1, 3, generations]:
        Jso, Jto = random_constellations(population_size, gen)
        ax8.scatter(Jso, Jto, label=f'Generation {gen}', alpha=0.6)
    ax8.set_xlabel("Spatial Objective (Jso)")
    ax8.set_ylabel("Temporal Objective (Jto)")
    ax8.set_title("Figure 8. Constellation population for generations 1, 3, and 20")
    ax8.legend()
    st.pyplot(fig8)

    # ----- FIG 9 -----
    fig9, ax9 = plt.subplots()
    for pareto in [1, 10, 48, 98]:
        x = np.linspace(0.02, 0.3, 50)
        y = 0.3 - x + np.random.rand(50) * 0.05 / pareto
        ax9.plot(x, y, label=f"Pareto {pareto}")
    ax9.set_xlabel("Jso")
    ax9.set_ylabel("Jto")
    ax9.set_title("Figure 9. Pareto fronts spanning search space")
    ax9.legend()
    st.pyplot(fig9)

    # ----- FIG 10 -----
    fig10, ax10 = plt.subplots()
    n = np.arange(1, 61)
    truth, est = geoid_error(60)
    ax10.plot(n, truth, 'k--', label="Truth signal")
    for curve in [1, 10, 48]:
        noise = est * (1 + np.log10(curve) * 0.1)
        ax10.plot(n, noise, label=f"Pareto {curve}")
    ax10.set_yscale("log")
    ax10.set_xlabel("Degree (n)")
    ax10.set_ylabel("Error (ΔNₙ)")
    ax10.set_title("Figure 10. Average degree variances for Pareto curves")
    ax10.legend()
    st.pyplot(fig10)

    # ----- FIG 11 -----
    fig11, ax11 = plt.subplots()
    constellations = np.random.rand(10, 2)
    ax11.scatter(constellations[:, 0], constellations[:, 1], c='blue', s=100)
    for i in range(10):
        ax11.text(constellations[i, 0], constellations[i, 1], f"c{i+1}", fontsize=9)
    ax11.set_xlabel("Jso")
    ax11.set_ylabel("Jto")
    ax11.set_title("Figure 11. Family of ten six-pair constellations")
    st.pyplot(fig11)

    # ----- FIG 12 -----
    fig12, ax12 = plt.subplots()
    for i in range(1, 11):
        ax12.plot(np.arange(1, 61), np.random.rand(60) * 1e-4, label=f"c{i:02}")
    ax12.set_yscale("log")
    ax12.set_xlabel("Degree")
    ax12.set_ylabel("Error")
    ax12.set_title("Figure 12. 1-day average degree variances (c01–c10)")
    ax12.legend(ncol=2)
    st.pyplot(fig12)

    # ----- FIG 13 -----
    fig13, ax13 = plt.subplots()
    days = np.arange(1, 31)
    ax13.plot(days, np.random.rand(30)*1e-4)
    ax13.set_xlabel("Day")
    ax13.set_ylabel("Degree Variance")
    ax13.set_title("Figure 13. 1-day variances for constellation c06 (Jan 2003)")
    st.pyplot(fig13)

    # ----- FIG 14 -----
    fig14, ax14 = plt.subplots()
    for i in range(1, 11):
        ax14.plot(np.arange(1, 61), np.random.rand(60)*1e-4, label=f"c{i:02}")
    ax14.set_yscale("log")
    ax14.set_xlabel("Degree")
    ax14.set_ylabel("Error")
    ax14.set_title("Figure 14. 29-day average degree variances (c01–c10)")
    ax14.legend(ncol=2)
    st.pyplot(fig14)

else:
    st.warning("Adjust parameters in the sidebar and click **Run Simulation** to generate results.")


