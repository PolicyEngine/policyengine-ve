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
    num_school_children=0,
    has_infant=False,
    spouse_age=None,  # If set, adds a non-earning spouse
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
                "is_male": {2025: True},
                "has_child_under_2": {2025: bool(has_infant)},
            }
        }
        members = ["adult"]

        # Add spouse if specified
        if spouse_age is not None:
            persons["spouse"] = {
                "age": {2025: int(spouse_age)},
                "employment_income": {2025: 0},
                "is_male": {2025: False},
                "has_carnet_patria": {2025: bool(has_carnet_patria)},
                "has_child_under_2": {2025: bool(has_infant)},
            }
            members.append("spouse")

        # Add school-age children
        for c in range(num_school_children):
            child_id = f"child_{c}"
            persons[child_id] = {
                "age": {2025: 8 + c * 3},  # Ages 8, 11, 14...
                "employment_income": {2025: 0},
                "is_in_school": {2025: True},
                "has_carnet_patria": {2025: bool(has_carnet_patria)},
            }
            members.append(child_id)

        # Add infant if specified
        if has_infant:
            persons["infant"] = {
                "age": {2025: 1},
                "employment_income": {2025: 0},
            }
            members.append("infant")

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
    # Earnings range capturing cliff and full income tax schedule
    # Tax brackets go up to 6000 TU = 258,000 VES, so extend to 300,000
    earnings_range = np.concatenate(
        [
            np.linspace(0, MIN_WAGE_ANNUAL * 0.9, 20),
            np.linspace(MIN_WAGE_ANNUAL * 0.9, MIN_WAGE_ANNUAL * 1.1, 50),
            np.linspace(MIN_WAGE_ANNUAL * 1.1, 300_000, 200),
        ]
    )

    # Household scenarios - showing cliffs and child benefits
    scenarios = [
        {
            "name": "Single Elderly (65+)",
            "params": {"age": 65, "has_carnet_patria": True},
            "color": "red",
        },
        {
            "name": "Elderly Couple (both 65+) - SAME CLIFF!",
            "params": {"age": 65, "spouse_age": 65, "has_carnet_patria": True},
            "color": "darkred",
        },
        {
            "name": "Single Working Age",
            "params": {"age": 35, "has_carnet_patria": True},
            "color": "blue",
        },
        {
            "name": "Family + 2 School Children",
            "params": {
                "age": 35,
                "spouse_age": 33,
                "num_school_children": 2,
                "has_carnet_patria": True,
            },
            "color": "green",
        },
        {
            "name": "Family + Infant (lactancia)",
            "params": {
                "age": 30,
                "spouse_age": 28,
                "has_infant": True,
                "has_carnet_patria": True,
            },
            "color": "purple",
        },
    ]

    # Create subplots
    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=("Net Income vs Earnings", "Marginal Tax Rate"),
        vertical_spacing=0.18,
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

        # MTR plot (capped at 1.0)
        mtr_capped = np.clip(mtr, None, 1.0)
        fig.add_trace(
            go.Scatter(
                x=earnings_range,
                y=mtr_capped,
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

    # Update layout with USD axis on top of first subplot only
    max_earnings = earnings_range.max()

    # Create USD tick values aligned with VES
    ves_ticks = np.linspace(0, max_earnings, 7)
    usd_ticks = ves_ticks * VES_TO_USD

    fig.update_layout(
        title="Venezuela: Net Income and MTR by Household Type (2025)",
        height=800,
        showlegend=True,
        legend=dict(x=0.02, y=0.98),
    )

    # VES axis labels on both charts
    fig.update_xaxes(title_text="Annual Earnings (VES)", row=1, col=1)
    fig.update_xaxes(title_text="Annual Earnings (VES)", row=2, col=1)
    fig.update_yaxes(title_text="Net Income (VES)", row=1, col=1)
    fig.update_yaxes(title_text="MTR", tickformat=".0%", row=2, col=1)

    # Add USD axis at the very top
    fig.add_trace(
        go.Scatter(x=[None], y=[None], xaxis="x2", showlegend=False),
    )
    fig.update_layout(
        xaxis2=dict(
            title="Annual Earnings (USD)",
            side="top",
            range=[0, max_earnings],
            tickvals=ves_ticks,
            ticktext=[f"${v:,.0f}" for v in usd_ticks],
            anchor="free",
            overlaying="x",
            position=1.0,
        ),
    )

    return fig


def create_cliff_detail_chart():
    """Create detailed chart showing the Amor Mayor cliff."""
    # Full range with fine granularity around cliff
    earnings_range = np.concatenate(
        [
            np.linspace(0, MIN_WAGE_ANNUAL * 0.9, 50),
            np.linspace(MIN_WAGE_ANNUAL * 0.9, MIN_WAGE_ANNUAL * 1.1, 100),
            np.linspace(MIN_WAGE_ANNUAL * 1.1, 300_000, 150),
        ]
    )

    net_income, mtr = calculate_net_income_and_mtr(
        earnings_range, age=65, has_carnet_patria=True
    )

    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=(
            "Net Income Around Cliff Threshold",
            "Marginal Tax Rate (Capped at 100%)",
        ),
        vertical_spacing=0.18,
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


    # MTR - capped at 1.0
    mtr_capped = np.clip(mtr, None, 1.0)
    fig.add_trace(
        go.Scatter(
            x=earnings_range,
            y=mtr_capped,
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

    max_earnings = earnings_range.max()

    # Create USD tick values aligned with VES
    ves_ticks = np.linspace(0, max_earnings, 7)
    usd_ticks = ves_ticks * VES_TO_USD

    fig.update_layout(
        title="Gran Misión Amor Mayor: The Benefit Cliff",
        height=700,
    )

    # VES axis labels on both charts
    fig.update_xaxes(title_text="Annual Earnings (VES)", row=1, col=1)
    fig.update_xaxes(title_text="Annual Earnings (VES)", row=2, col=1)
    fig.update_yaxes(title_text="Net Income (VES)", row=1, col=1)
    fig.update_yaxes(title_text="MTR", tickformat=".0%", row=2, col=1)

    # Add USD axis at the very top
    fig.add_trace(
        go.Scatter(x=[None], y=[None], xaxis="x2", showlegend=False),
    )
    fig.update_layout(
        xaxis2=dict(
            title="Annual Earnings (USD)",
            side="top",
            range=[0, max_earnings],
            tickvals=ves_ticks,
            ticktext=[f"${v:,.0f}" for v in usd_ticks],
            anchor="free",
            overlaying="x",
            position=1.0,
        ),
    )

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
