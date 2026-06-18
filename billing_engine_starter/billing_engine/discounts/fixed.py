"""
FixedAmountDiscount — e.g., flat ₹500 off.

CAPPING RULE: if the fixed amount exceeds the subtotal, return subtotal
(so the discounted total never goes below zero).
"""

from billing_engine.money import Money
from billing_engine.discounts.base import Discount, DiscountContext


class FixedAmountDiscount(Discount):
    def __init__(self, amount: Money) -> None:
        # TODO Day 1
        if not isinstance(amount, Money):
            raise TypeError("FixedAmountDiscount amount must be Money")
        if amount.is_negative():
            raise ValueError("FixedAmountDiscount amount cannot be negative")
        self.amount = amount

    def apply(self, subtotal: Money, context: DiscountContext) -> Money:
        # TODO Day 1
        if self.amount.currency != subtotal.currency:
            raise ValueError("discount currency must match subtotal currency")
        return self.amount if self.amount < subtotal else subtotal
    # changes done
