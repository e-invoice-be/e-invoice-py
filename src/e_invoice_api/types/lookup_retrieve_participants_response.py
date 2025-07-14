# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = [
    "LookupRetrieveParticipantsResponse",
    "Participant",
    "ParticipantDocumentType",
    "ParticipantEntity",
    "ParticipantEntityIdentifier",
]


class ParticipantDocumentType(BaseModel):
    scheme: str
    """Document type scheme"""

    value: str
    """Document type value"""


class ParticipantEntityIdentifier(BaseModel):
    scheme: str
    """Identifier scheme"""

    value: str
    """Identifier value"""


class ParticipantEntity(BaseModel):
    additional_info: Optional[str] = None
    """Additional information"""

    country_code: Optional[str] = None
    """Country code"""

    geo_info: Optional[str] = None
    """Geographic information"""

    identifiers: Optional[List[ParticipantEntityIdentifier]] = None
    """List of business identifiers"""

    name: Optional[str] = None
    """Business entity name"""

    registration_date: Optional[str] = None
    """Registration date"""

    website: Optional[str] = None
    """Website URL"""


class Participant(BaseModel):
    peppol_id: str
    """Peppol ID of the participant"""

    peppol_scheme: str
    """Peppol scheme of the participant"""

    document_types: Optional[List[ParticipantDocumentType]] = None
    """List of supported document types"""

    entities: Optional[List[ParticipantEntity]] = None
    """List of business entities"""


class LookupRetrieveParticipantsResponse(BaseModel):
    query_terms: str
    """Query terms used for search"""

    search_date: str
    """Search date of the result"""

    total_count: int
    """Total number of results"""

    used_count: int
    """Number of results returned by the API"""

    participants: Optional[List[Participant]] = None
    """List of participants"""
