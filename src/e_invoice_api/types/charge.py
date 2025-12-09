# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Charge"]


class Charge(BaseModel):
    """A charge is an additional fee for example for late payment, late delivery, etc."""

    amount: Optional[str] = None
    """The charge amount, without VAT. Must be rounded to maximum 2 decimals"""

    base_amount: Optional[str] = None
    """
    The base amount that may be used, in conjunction with the charge percentage, to
    calculate the charge amount. Must be rounded to maximum 2 decimals
    """

    multiplier_factor: Optional[str] = None
    """
    The percentage that may be used, in conjunction with the charge base amount, to
    calculate the charge amount. To state 20%, use value 20
    """

    reason: Optional[str] = None
    """The reason for the charge"""

    reason_code: Optional[
        Literal[
            "AA",
            "AAA",
            "AAC",
            "AAD",
            "AAE",
            "AAF",
            "AAH",
            "AAI",
            "AAS",
            "AAT",
            "AAV",
            "AAY",
            "AAZ",
            "ABA",
            "ABB",
            "ABC",
            "ABD",
            "ABF",
            "ABK",
            "ABL",
            "ABN",
            "ABR",
            "ABS",
            "ABT",
            "ABU",
            "ACF",
            "ACG",
            "ACH",
            "ACI",
            "ACJ",
            "ACK",
            "ACL",
            "ACM",
            "ACS",
            "ADC",
            "ADE",
            "ADJ",
            "ADK",
            "ADL",
            "ADM",
            "ADN",
            "ADO",
            "ADP",
            "ADQ",
            "ADR",
            "ADT",
            "ADW",
            "ADY",
            "ADZ",
            "AEA",
            "AEB",
            "AEC",
            "AED",
            "AEF",
            "AEH",
            "AEI",
            "AEJ",
            "AEK",
            "AEL",
            "AEM",
            "AEN",
            "AEO",
            "AEP",
            "AES",
            "AET",
            "AEU",
            "AEV",
            "AEW",
            "AEX",
            "AEY",
            "AEZ",
            "AJ",
            "AU",
            "CA",
            "CAB",
            "CAD",
            "CAE",
            "CAF",
            "CAI",
            "CAJ",
            "CAK",
            "CAL",
            "CAM",
            "CAN",
            "CAO",
            "CAP",
            "CAQ",
            "CAR",
            "CAS",
            "CAT",
            "CAU",
            "CAV",
            "CAW",
            "CAX",
            "CAY",
            "CAZ",
            "CD",
            "CG",
            "CS",
            "CT",
            "DAB",
            "DAC",
            "DAD",
            "DAF",
            "DAG",
            "DAH",
            "DAI",
            "DAJ",
            "DAK",
            "DAL",
            "DAM",
            "DAN",
            "DAO",
            "DAP",
            "DAQ",
            "DL",
            "EG",
            "EP",
            "ER",
            "FAA",
            "FAB",
            "FAC",
            "FC",
            "FH",
            "FI",
            "GAA",
            "HAA",
            "HD",
            "HH",
            "IAA",
            "IAB",
            "ID",
            "IF",
            "IR",
            "IS",
            "KO",
            "L1",
            "LA",
            "LAA",
            "LAB",
            "LF",
            "MAE",
            "MI",
            "ML",
            "NAA",
            "OA",
            "PA",
            "PAA",
            "PC",
            "PL",
            "PRV",
            "RAB",
            "RAC",
            "RAD",
            "RAF",
            "RE",
            "RF",
            "RH",
            "RV",
            "SA",
            "SAA",
            "SAD",
            "SAE",
            "SAI",
            "SG",
            "SH",
            "SM",
            "SU",
            "TAB",
            "TAC",
            "TT",
            "TV",
            "V1",
            "V2",
            "WH",
            "XAA",
            "YY",
            "ZZZ",
        ]
    ] = None
    """Charge reason codes for invoice charges and fees"""

    tax_code: Optional[Literal["AE", "E", "S", "Z", "G", "O", "K", "L", "M", "B"]] = None
    """Duty or tax or fee category codes (Subset of UNCL5305)

    Agency: UN/CEFACT Version: D.16B Subset: OpenPEPPOL
    """

    tax_rate: Optional[str] = None
    """The VAT rate, represented as percentage that applies to the charge"""
