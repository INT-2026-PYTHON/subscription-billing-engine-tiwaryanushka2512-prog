"""
TieredPricing — different price per unit depending on the tier the quantity falls into.

This is the "cumulative" / "stacked" tier model, NOT the "volume" model:
    Tiers: [(0, 1000, ₹2.00), (1000, 5000, ₹1.50), (5000, None, ₹1.00)]
    Quantity = 6000:
        First 1000 units  @ ₹2.00 = ₹2000
        Next  4000 units  @ ₹1.50 = ₹6000
        Last  1000 units  @ ₹1.00 = ₹1000
        ------------------------------------
        Total                     = ₹9000

A tier with `to_units = None` is the open-ended top tier.

Tier boundaries are HALF-OPEN on the right: a tier (from, to, price)
covers units strictly less than `to` (i.e. [from, to)).
"""

from dataclasses import dataclass
from typing import Optional

from billing_engine.money import Money
from billing_engine.pricing.base import PricingStrategy


@dataclass(frozen=True)
class Tier:
    from_units: int
    to_units: Optional[int]   # None means "unlimited" / open-ended
    unit_price: Money


class TieredPricing(PricingStrategy):
    """Charges across multiple price tiers based on cumulative quantity."""

    def __init__(self, tiers: list[Tier]) -> None:
        # TODO Day 1
        if not tiers:
            raise ValueError("tiers cannot be empty")

        currency = tiers[0].unit_price.currency
        for i, tier in enumerate(tiers):
            if tier.unit_price.currency != currency:
                raise ValueError("all tiers must use the same currency")
            if tier.unit_price.is_negative():
                raise ValueError("tier unit_price cannot be negative")
            if tier.from_units < 0:
                raise ValueError("tier from_units cannot be negative")
            if tier.to_units is not None and tier.to_units <= tier.from_units:
                raise ValueError("tier to_units must be greater than from_units")
            if i < len(tiers) - 1:
                if tier.to_units is None:
                    raise ValueError("only the last tier can be open-ended")
                if tiers[i + 1].from_units != tier.to_units:
                    raise ValueError("tiers must be contiguous")
            elif tier.to_units is not None:
                raise ValueError("top tier must be open-ended")

        self.tiers = tiers

    def calculate(self, quantity: int) -> Money:
        # TODO Day 1
        if quantity < 0:
            raise ValueError("quantity cannot be negative")

        total = Money.zero(self.tiers[0].unit_price.currency)
        for tier in self.tiers:
            if quantity <= tier.from_units:
                units = 0
            elif tier.to_units is None:
                units = quantity - tier.from_units
            else:
                units = min(quantity, tier.to_units) - tier.from_units
            total = total + (tier.unit_price * units)
        return total
    
    # changes done
