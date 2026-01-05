"""
Net Income and MTR Analysis for Venezuela
==========================================

This script generates net income and marginal tax rate (MTR) graphs
for various household types in Venezuela, highlighting the benefit cliff
in the Gran Mision Amor Mayor pension program.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from policyengine_ve import Simulation

# Constants
VES_TO_USD = 1 / 36  # Approximate exchange rate
MIN_WAGE_ANNUAL = 1_560  # VES (130/month * 12)


def calculate_net_income_and_mtr(
    earnings_range,
    age=35,
    is_public_sector=False,
    has_carnet_patria=True,
    is_retired=False,
    was_public_sector_retiree=False,
    num_children=0,
):
    """Calculate net income and MTR across an earnings range."""
    net_incomes = []
    mtrs = []

    for i, earnings in enumerate(earnings_range):
        # Build situation
        persons = {
            "adult": {
                "age": {2025: int(age)},
                "employment_income": {2025: float(earnings)},
                "is_public_sector": {2025: bool(is_public_sector)},
                "has_carnet_patria": {2025: bool(has_carnet_patria)},
                "is_retired": {2025: bool(is_retired)},
                "is_employed": {2025: bool(not is_retired and earnings > 0)},
                "was_public_sector_retiree": {2025: bool(was_public_sector_retiree)},
            }
        }
        members = ["adult"]

        # Add children if specified
        for c in range(num_children):
            child_id = f"child_{c}"
            persons[child_id] = {
                "age": {2025: 5 + c * 3},
                "employment_income": {2025: 0},
            }
            members.append(child_id)

        situation = {
            "persons": persons,
            "households": {"household": {"members": members}},
        }

        sim = Simulation(situation=situation)
        net_income = sim.calculate("household_net_income", 2025)[0]
        net_incomes.append(net_income)

        # Calculate MTR using finite difference
        if i > 0:
            delta_earnings = earnings_range[i] - earnings_range[i - 1]
            delta_net = net_incomes[i] - net_incomes[i - 1]
            mtr = 1 - (delta_net / delta_earnings) if delta_earnings > 0 else 0
            mtrs.append(mtr)
        else:
            mtrs.append(0)

    return np.array(net_incomes), np.array(mtrs)


def create_household_comparison_chart():
    """Create comparison chart for different household types."""
    # Fine-grained earnings range to capture cliff
    earnings_range = np.concatenate(
        [
            np.linspace(0, MIN_WAGE_ANNUAL * 0.9, 20),
            np.linspace(MIN_WAGE_ANNUAL * 0.9, MIN_WAGE_ANNUAL * 1.1, 50),
            np.linspace(MIN_WAGE_ANNUAL * 1.1, 10_000, 30),
        ]
    )

    # Household scenarios
    scenarios = [
        {
            "name": "Elderly (65+), with Carnet",
            "params": {"age": 65, "has_carnet_patria": True},
            "color": "red",
        },
        {
            "name": "Elderly (65+), no Carnet",
            "params": {"age": 65, "has_carnet_patria": False},
            "color": "orange",
        },
        {
            "name": "Working Age (35)",
            "params": {"age": 35, "has_carnet_patria": True},
            "color": "blue",
        },
        {
            "name": "Public Sector Worker",
            "params": {
                "age": 35,
                "is_public_sector": True,
                "has_carnet_patria": True,
            },
            "color": "green",
        },
    ]

    # Create subplots
    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=("Net Income vs Earnings", "Marginal Tax Rate"),
        vertical_spacing=0.12,
    )

    for scenario in scenarios:
        net_income, mtr = calculate_net_income_and_mtr(
            earnings_range, **scenario["params"]
        )

        # Net income plot
        fig.add_trace(
            go.Scatter(
                x=earnings_range,
                y=net_income,
                mode="lines",
                name=scenario["name"],
                line=dict(color=scenario["color"]),
                legendgroup=scenario["name"],
            ),
            row=1,
            col=1,
        )

        # MTR plot
        fig.add_trace(
            go.Scatter(
                x=earnings_range,
                y=mtr * 100,  # Convert to percentage
                mode="lines",
                name=scenario["name"],
                line=dict(color=scenario["color"]),
                legendgroup=scenario["name"],
                showlegend=False,
            ),
            row=2,
            col=1,
        )

    # Add cliff annotation
    fig.add_vline(
        x=MIN_WAGE_ANNUAL,
        line_dash="dash",
        line_color="gray",
        annotation_text="Minimum Wage<br>(Cliff Threshold)",
        row=1,
        col=1,
    )
    fig.add_vline(
        x=MIN_WAGE_ANNUAL,
        line_dash="dash",
        line_color="gray",
        row=2,
        col=1,
    )

    # Update layout
    fig.update_layout(
        title="Venezuela: Net Income and MTR by Household Type (2025)",
        height=800,
        showlegend=True,
        legend=dict(x=0.02, y=0.98),
    )
    fig.update_xaxes(title_text="Annual Earnings (VES)", row=2, col=1)
    fig.update_yaxes(title_text="Net Income (VES)", row=1, col=1)
    fig.update_yaxes(title_text="MTR (%)", row=2, col=1)

    return fig


def create_cliff_detail_chart():
    """Create detailed chart showing the Amor Mayor cliff."""
    # Very fine-grained around the cliff
    earnings_range = np.linspace(
        MIN_WAGE_ANNUAL * 0.8, MIN_WAGE_ANNUAL * 1.2, 200
    )

    net_income, mtr = calculate_net_income_and_mtr(
        earnings_range, age=65, has_carnet_patria=True
    )

    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=(
            "Net Income Around Cliff Threshold",
            "Marginal Tax Rate (Note: Infinite at Threshold)",
        ),
        vertical_spacing=0.12,
    )

    # Net income
    fig.add_trace(
        go.Scatter(
            x=earnings_range,
            y=net_income,
            mode="lines",
            name="Net Income",
            line=dict(color="red", width=2),
        ),
        row=1,
        col=1,
    )

    # 45-degree line (no taxes/benefits)
    fig.add_trace(
        go.Scatter(
            x=earnings_range,
            y=earnings_range,
            mode="lines",
            name="45° Line (No Tax/Benefits)",
            line=dict(color="gray", dash="dot"),
        ),
        row=1,
        col=1,
    )

    # MTR - clip extreme values for visualization
    mtr_clipped = np.clip(mtr * 100, -100, 500)
    fig.add_trace(
        go.Scatter(
            x=earnings_range,
            y=mtr_clipped,
            mode="lines",
            name="MTR",
            line=dict(color="darkred", width=2),
        ),
        row=2,
        col=1,
    )

    # Add threshold line
    fig.add_vline(
        x=MIN_WAGE_ANNUAL,
        line_dash="dash",
        line_color="black",
        annotation_text=f"Threshold: {MIN_WAGE_ANNUAL} VES<br>(~${MIN_WAGE_ANNUAL * VES_TO_USD:.0f} USD)",
    )

    # Add annotation for the cliff
    fig.add_annotation(
        x=MIN_WAGE_ANNUAL,
        y=net_income[len(net_income) // 2],
        text="CLIFF: Earning $1 more<br>loses entire pension!",
        showarrow=True,
        arrowhead=2,
        ax=50,
        ay=-50,
        row=1,
        col=1,
    )

    fig.update_layout(
        title="Gran Misión Amor Mayor: The Benefit Cliff",
        height=700,
    )
    fig.update_xaxes(title_text="Annual Earnings (VES)")
    fig.update_yaxes(title_text="Net Income (VES)", row=1, col=1)
    fig.update_yaxes(title_text="MTR (%)", row=2, col=1)

    return fig


if __name__ == "__main__":
    print("Generating Venezuela net income and MTR charts...")

    # Generate charts
    comparison_fig = create_household_comparison_chart()
    cliff_fig = create_cliff_detail_chart()

    # Save as HTML
    comparison_fig.write_html("notebooks/household_comparison.html")
    cliff_fig.write_html("notebooks/cliff_detail.html")

    print("Charts saved to notebooks/")
    print("- household_comparison.html")
    print("- cliff_detail.html")

    # Also show
    comparison_fig.show()
    cliff_fig.show()
