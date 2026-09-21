# Mini Haladir

A small logistics decisioning demo inspired by Haladir's workflow.

The system combines data from multiple operational systems, creates a unified view of an order, makes a recommendation, and lets an operator approve the action.

## Architecture

```text
WMS + TMS + OMS
        |
        v
Unified Order State
        |
        v
Decision Engine
        |
        v
Operator Recommendation
        |
        v
Approved Action
        |
        v
Write Back to Operational Systems
```

## Systems

### WMS
Provides warehouse information:

- inventory availability
- picker availability
- dock availability
- current dock

### TMS
Provides transportation information:

- truck ID
- truck departure time

### OMS
Provides order information:

- order ID
- priority
- order status

## Decision Logic

For a high-priority order with a truck leaving in less than 30 minutes:

- if inventory is unavailable, wait
- if no picker is available, wait
- if no dock is available, move to another dock
- otherwise, ship now

## Human-in-the-loop

The system does not immediately execute recommendations.

An operator sees the recommendation and must approve it before the system writes changes back to the operational systems.

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the simulated operational systems:

```bash
uvicorn systems_api:app --port 8765
```

In another terminal, start the operator interface:

```bash
streamlit run app.py
```

Then open the Streamlit URL shown in the terminal.
