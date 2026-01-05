"""Entity definitions for Venezuela tax-benefit system."""

from policyengine_core.entities import build_entity

Person = build_entity(
    key="person",
    plural="persons",
    label="Person",
    doc="A physical person",
    is_person=True,
)

Household = build_entity(
    key="household",
    plural="households",
    label="Household",
    doc="""A household sharing living expenses and potentially benefits.

    In Venezuela, many social programs (Sistema Patria, CLAP) are distributed
    at the household level via the Carnet de la Patria.""",
    roles=[
        dict(
            key="member",
            plural="members",
            label="Member",
            doc="A person in the household",
        ),
        dict(
            key="head",
            plural="heads",
            label="Head of household",
            max=1,
            doc="The primary adult responsible for the household",
        ),
    ],
    containing_entities=["person"],
)

entities = [Person, Household]
