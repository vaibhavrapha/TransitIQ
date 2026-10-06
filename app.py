
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="TransitIQ - Smart Bus Advisor",
    page_icon="🚌",
    layout="wide"
)

# -----------------------------
# Sample prototype data
# -----------------------------
ROUTES = {
    ("College", "Railway Station"): [
        {"bus": "Bus 101", "eta": 5, "delay": 8, "crowd": "High", "travel_time": 24, "reliability": 72},
        {"bus": "Bus 205", "eta": 8, "delay": 0, "crowd": "Low", "travel_time": 22, "reliability": 92},
        {"bus": "Bus 310", "eta": 12, "delay": 2, "crowd": "Medium", "travel_time": 20, "reliability": 84},
    ],
    ("College", "City Center"): [
        {"bus": "Bus 115", "eta": 4, "delay": 4, "crowd": "High", "travel_time": 18, "reliability": 76},
        {"bus": "Bus 220", "eta": 7, "delay": 1, "crowd": "Low", "travel_time": 17, "reliability": 94},
        {"bus": "Bus 405", "eta": 10, "delay": 0, "crowd": "Medium", "travel_time": 15, "reliability": 88},
    ],
    ("Hostel", "Railway Station"): [
        {"bus": "Bus 150", "eta": 6, "delay": 5, "crowd": "Medium", "travel_time": 26, "reliability": 80},
        {"bus": "Bus 260", "eta": 9, "delay": 0, "crowd": "Low", "travel_time": 23, "reliability": 95},
        {"bus": "Bus 390", "eta": 3, "delay": 10, "crowd": "High", "travel_time": 28, "reliability": 68},
    ],
    ("City Center", "Hospital"): [
        {"bus": "Bus 178", "eta": 5, "delay": 2, "crowd": "Medium", "travel_time": 16, "reliability": 86},
        {"bus": "Bus 280", "eta": 8, "delay": 0, "crowd": "Low", "travel_time": 14, "reliability": 96},
        {"bus": "Bus 333", "eta": 4, "delay": 6, "crowd": "High", "travel_time": 15, "reliability": 74},
    ],
}

CROWD_PENALTY = {"Low": 0, "Medium": 5, "High": 10}

def score_bus(bus):
    # Lower score = better option
    reliability_penalty = (100 - bus["reliability"]) * 0.1
    return (
        bus["eta"]
        + bus["delay"]
        + CROWD_PENALTY[bus["crowd"]]
        + reliability_penalty
    )

def crowd_icon(level):
    return {"Low": "🟢 Low", "Medium": "🟡 Medium", "High": "🔴 High"}[level]

st.title("🚌 TransitIQ")
st.subheader("Smart Bus Decision Assistant")
st.caption("Prototype using simulated transport data — designed for AutoAgent 3D.")

with st.sidebar:
    st.header("Trip Setup")
    origins = sorted(set(k[0] for k in ROUTES.keys()))
    origin = st.selectbox("From", origins)

    destinations = sorted(k[1] for k in ROUTES.keys() if k[0] == origin)
    destination = st.selectbox("To", destinations)

    simulate_incident = st.checkbox("Simulate traffic incident")
    st.markdown("---")
    st.info(
        "This prototype does not use live government transport data. "
        "It demonstrates the decision logic using simulated data."
    )

route_key = (origin, destination)
buses = [b.copy() for b in ROUTES[route_key]]

# Optional disruption demonstration
if simulate_incident:
    # Delay the currently most reliable bus to demonstrate re-ranking
    target = max(buses, key=lambda x: x["reliability"])
    target["delay"] += 12
    target["reliability"] = max(50, target["reliability"] - 18)

for b in buses:
    b["score"] = round(score_bus(b), 1)
    b["total_trip"] = b["eta"] + b["travel_time"] + b["delay"]

best = min(buses, key=lambda x: x["score"])

st.markdown("### Passenger Question")
st.write(f"**Which bus should I take from {origin} to {destination} right now?**")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Recommended Bus", best["bus"])
col2.metric("Arrives In", f'{best["eta"]} min')
col3.metric("Crowd", best["crowd"])
col4.metric("Reliability", f'{best["reliability"]}%')

st.success(
    f"⭐ Recommended: **{best['bus']}** — best overall balance of waiting time, "
    f"delay, crowd level and reliability."
)

table = pd.DataFrame([
    {
        "Bus": b["bus"],
        "Arrival": f'{b["eta"]} min',
        "Crowd": crowd_icon(b["crowd"]),
        "Delay": f'+{b["delay"]} min' if b["delay"] else "On time",
        "Travel Time": f'{b["travel_time"]} min',
        "Reliability": f'{b["reliability"]}%',
        "Decision Score": b["score"],
        "Recommendation": "⭐ BEST" if b["bus"] == best["bus"] else "Alternative"
    }
    for b in sorted(buses, key=lambda x: x["score"])
])

st.markdown("### Available Buses")
st.dataframe(table, use_container_width=True, hide_index=True)

st.markdown("### Why this bus?")
reason1, reason2, reason3, reason4 = st.columns(4)
reason1.write(f"⏱️ **Wait:** {best['eta']} min")
reason2.write(f"👥 **Crowd:** {best['crowd']}")
reason3.write(f"🚦 **Delay:** {best['delay']} min")
reason4.write(f"✅ **Reliability:** {best['reliability']}%")

st.markdown("### How the recommendation works")
st.code(
    "Decision Score = Waiting Time + Delay + Crowd Penalty + Reliability Penalty\n"
    "Crowd Penalty: Low = 0, Medium = 5, High = 10\n"
    "Reliability Penalty = (100 - Reliability) × 0.1\n"
    "Lower score = Better bus",
    language="text"
)

score_df = pd.DataFrame(
    {
        "Bus": [b["bus"] for b in buses],
        "Decision Score": [b["score"] for b in buses]
    }
).set_index("Bus")

st.bar_chart(score_df)

st.markdown("### Demonstration Outcome")
fastest_arrival = min(buses, key=lambda x: x["eta"])
saved = fastest_arrival["total_trip"] - best["total_trip"]

if fastest_arrival["bus"] != best["bus"] and saved > 0:
    st.write(
        f"If a passenger simply chooses the first arriving bus (**{fastest_arrival['bus']}**), "
        f"the total estimated trip is **{fastest_arrival['total_trip']} min**. "
        f"TransitIQ recommends **{best['bus']}**, with **{best['total_trip']} min**, "
        f"saving about **{saved} min** in this simulated scenario."
    )
else:
    st.write(
        f"In this simulated scenario, **{best['bus']}** is also the strongest option by total trip time. "
        "TransitIQ still checks crowd, delay and reliability before recommending it."
    )

if simulate_incident:
    st.warning(
        "Traffic incident simulation is ON. The system has increased delay on one bus "
        "and automatically recalculated the recommendation."
    )

st.markdown("---")
st.caption(
    "TransitIQ converts transport information into a simple passenger decision. "
    "All values shown are simulated for prototype demonstration."
)
