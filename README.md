# PolicyEngine Venezuela

A tax-benefit microsimulation model for Venezuela, built on the PolicyEngine framework.

## Installation

```bash
pip install -e .[dev]
```

## Usage

```python
from policyengine_ve import Simulation

sim = Simulation(
    situation={
        "persons": {
            "adult": {
                "age": {2025: 30},
                "employment_income": {2025: 1000},
                "is_public_sector": {2025: True},
            }
        },
        "households": {
            "household": {
                "members": ["adult"],
            }
        },
    }
)

net_income = sim.calculate("household_net_income", 2025)
print(f"Net income: {net_income[0]} VES")
```

## Modeled Programs

### Taxes
- Personal income tax (8 brackets, 6-34%)
- Payroll taxes (IVSS, BANAVIH, INCES, unemployment)
- VAT/IVA (16% standard, 8% reduced)

### Transfers
- Sistema Patria bonuses (public sector, pensioners)
- Gran Misión Amor Mayor (income-tested social pension)

## Key Features

- **Benefit cliff modeling**: The Gran Misión Amor Mayor pension has an income test
  at the minimum wage threshold, creating an MTR > 100% cliff.
- **Public/private sector divide**: Public sector workers receive comprehensive
  income packages (~$160/month) while private sector minimum wage is ~$3.50/month.

## References

- [PWC Venezuela Tax Summary](https://taxsummaries.pwc.com/venezuela/individual/taxes-on-personal-income)
- [SSA - Venezuela Social Security](https://www.ssa.gov/policy/docs/progdesc/ssptw/2018-2019/americas/venezuela.html)
- [Venezuelanalysis - Bonus System](https://venezuelanalysis.com/news/venezuela-maduro-govt-announces-may-day-bonus-increase-maintains-wage-freeze/)
