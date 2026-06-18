"""
GSTCalculator — Indian Goods & Services Tax.

The rule:
    - If customer_state == seller_state (or seller_state is "")  =>  intra-state
        -> charge CGST + SGST (split equally, e.g. 9% + 9% = 18%)
    - Else  =>  inter-state
        -> charge IGST (e.g. 18%)

Customers without a state code default to IGST (safe choice).
"""

from decimal import Decimal

from billing_engine.money import Money
from billing_engine.taxes.base import TaxCalculator, TaxContext, TaxBreakdown


class GSTCalculator(TaxCalculator):
    def __init__(self, cgst: Decimal, sgst: Decimal, igst: Decimal) -> None:
        # TODO Day 1
         for name, rate in (("cgst", cgst), ("sgst", sgst), ("igst", igst)):
            if isinstance(rate, float):
                raise TypeError(f"{name} must be Decimal, not float")
            if not isinstance(rate, Decimal):
                raise TypeError(f"{name} must be Decimal")
            if rate < Decimal("0") or rate > Decimal("1"):
                raise ValueError(f"{name} must be between 0 and 1")
         if cgst + sgst != igst:
            raise ValueError("cgst + sgst must equal igst")

         self.cgst = cgst
         self.sgst = sgst
         self.igst = igst

        #   - Validate each rate is Decimal in [0, 1].
        #   - Validate cgst + sgst == igst (sanity check on Indian GST setup).
        #   - Store on self.
        
    def apply(self, taxable: Money, context: TaxContext) -> TaxBreakdown:
        # TODO Day 1
        #   - Decide intra vs inter-state from context.
        #     intra = bool(context.customer_state) and context.customer_state == context.seller_state
        #   - If intra: components = [("CGST X%", taxable*cgst), ("SGST Y%", taxable*sgst)], total = sum
        #   - Else:     components = [("IGST Z%", taxable*igst)],                            total = igst leg
        intra = bool(context.customer_state) and context.customer_state == context.seller_state
        if intra:
            cgst_amount = taxable * self.cgst
            sgst_amount = taxable * self.sgst
            components = [
                (f"CGST {self.cgst * 100}%", cgst_amount),
                (f"SGST {self.sgst * 100}%", sgst_amount),
            ]
            return TaxBreakdown(components=components, total=cgst_amount + sgst_amount)

        igst_amount = taxable * self.igst
        return TaxBreakdown(
            components=[(f"IGST {self.igst * 100}%", igst_amount)],
            total=igst_amount,
        )
    
    # changes done
