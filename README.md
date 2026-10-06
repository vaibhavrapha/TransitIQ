## 🌐 Live Prototype

Try TransitIQ here:

https://transitiq-smart-bus.streamlit.app/
# TransitIQ — Smart Bus Decision Assistant

## Theme
**Theme 2 — Public Transportation**

## Problem
Passengers often do not know which bus is the best option because arrival time alone is not enough.
A bus may arrive first but be overcrowded, delayed, or unreliable.

## Solution
TransitIQ compares available buses using:
- Waiting time
- Delay
- Crowd level
- Reliability

It then recommends the best bus using a simple transparent decision score.

## Why this is suitable for AutoAgent 3D
The event asks teams to:
1. Clearly address the given problem.
2. Provide a working solution.
3. Demonstrate a meaningful outcome.

This prototype demonstrates all three using simulated data.

## Important honesty note
This is a **prototype using simulated transport data**.
Do not claim that it uses live government GPS or real bus APIs unless you later add such a source.

## Run the prototype

### 1. Install Python
Python 3.10+ recommended.

### 2. Open terminal in this folder

### 3. Install packages
```bash
pip install -r requirements.txt
```

### 4. Start the app
```bash
streamlit run app.py
```

A browser window should open automatically.

## Decision Logic
Lower score is better:

```text
Decision Score =
Waiting Time
+ Delay
+ Crowd Penalty
+ Reliability Penalty
```

Crowd penalties:
- Low = 0
- Medium = 5
- High = 10

Reliability penalty:
```text
(100 - Reliability) × 0.1
```

## Demo Flow
1. Select From and To.
2. Observe the recommended bus.
3. Explain why it was selected.
4. Turn ON "Simulate traffic incident".
5. Show that the recommendation can change automatically.
6. Explain that the system turns transport data into a passenger decision.

## One-line pitch
**"Most systems tell passengers where the bus is. TransitIQ tells passengers which bus they should take."**
