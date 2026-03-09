# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .certificate import Certificate

__all__ = [
    "LookupRetrieveResponse",
    "BusinessCard",
    "BusinessCardEntity",
    "DNSInfo",
    "DNSInfoDNSRecord",
    "QueryMetadata",
    "ServiceMetadata",
    "ServiceMetadataEndpoint",
    "ServiceMetadataEndpointDocumentType",
    "ServiceMetadataEndpointProcess",
    "ServiceMetadataEndpointProcessEndpoint",
    "ServiceMetadataEndpointProcessProcessID",
]


class BusinessCardEntity(BaseModel):
    """Business entity information in the Peppol network."""

    additional_information: Optional[List[str]] = FieldInfo(alias="additionalInformation", default=None)
    """Additional information about the business entity"""

    country_code: Optional[str] = FieldInfo(alias="countryCode", default=None)
    """ISO 3166-1 alpha-2 country code of the business entity"""

    name: Optional[str] = None
    """Name of the business entity"""

    registration_date: Optional[str] = FieldInfo(alias="registrationDate", default=None)
    """ISO 8601 date of when the entity was registered in Peppol"""


class BusinessCard(BaseModel):
    """Business card information for the Peppol participant"""

    entities: List[BusinessCardEntity]
    """List of business entities associated with the Peppol ID"""

    query_time_ms: float = FieldInfo(alias="queryTimeMs")
    """Time taken to query the business card in milliseconds"""

    status: str
    """Status of the business card lookup: 'success', 'error', or 'pending'"""

    error: Optional[str] = None
    """Error message if business card lookup failed"""


class DNSInfoDNSRecord(BaseModel):
    """DNS record information for a Peppol participant."""

    ip: str
    """IP address found in the DNS record"""


class DNSInfo(BaseModel):
    """Information about the DNS lookup performed"""

    dns_records: List[DNSInfoDNSRecord] = FieldInfo(alias="dnsRecords")
    """List of DNS records found for the Peppol participant"""

    sml_hostname: str = FieldInfo(alias="smlHostname")
    """Hostname of the SML used for the query"""

    status: str
    """Status of the DNS lookup: 'success', 'error', or 'pending'"""

    error: Optional[str] = None
    """Error message if the DNS lookup failed"""

    lookup_method: Optional[str] = FieldInfo(alias="lookupMethod", default=None)
    """DNS lookup method used: 'naptr' (new spec) or 'busdox' (legacy)"""

    smp_hostname: Optional[str] = FieldInfo(alias="smpHostname", default=None)
    """Hostname of the SMP (Service Metadata Publisher) discovered via DNS"""


class QueryMetadata(BaseModel):
    """Metadata about the query that was performed"""

    identifier_scheme: str = FieldInfo(alias="identifierScheme")
    """Scheme of the identifier, typically 'iso6523-actorid-upis'"""

    identifier_value: str = FieldInfo(alias="identifierValue")
    """The actual Peppol ID value being queried"""

    sml_domain: str = FieldInfo(alias="smlDomain")
    """Domain of the SML (Service Metadata Locator) used for the lookup"""

    timestamp: str
    """ISO 8601 timestamp of when the query was executed"""

    version: str
    """Version of the API used for the lookup"""


class ServiceMetadataEndpointDocumentType(BaseModel):
    """Document type supported by a Peppol participant."""

    scheme: str
    """Scheme of the document type identifier"""

    value: str
    """Value of the document type identifier"""


class ServiceMetadataEndpointProcessEndpoint(BaseModel):
    """Endpoint information for a specific Peppol process."""

    address: str
    """URL or address of the endpoint"""

    transport_profile: str = FieldInfo(alias="transportProfile")
    """Transport profile used by this endpoint"""

    certificate: Optional[Certificate] = None
    """Certificate information for a Peppol endpoint."""

    service_activation_date: Optional[str] = FieldInfo(alias="serviceActivationDate", default=None)
    """ISO 8601 date when the service was activated"""

    service_description: Optional[str] = FieldInfo(alias="serviceDescription", default=None)
    """Human-readable description of the service"""

    service_expiration_date: Optional[str] = FieldInfo(alias="serviceExpirationDate", default=None)
    """ISO 8601 date when the service will expire"""

    technical_contact_url: Optional[str] = FieldInfo(alias="technicalContactUrl", default=None)
    """URL for technical contact information"""

    technical_information_url: Optional[str] = FieldInfo(alias="technicalInformationUrl", default=None)
    """URL for technical documentation"""


class ServiceMetadataEndpointProcessProcessID(BaseModel):
    """Identifier of the process"""

    scheme: str
    """Scheme of the process identifier"""

    value: str
    """Value of the process identifier"""


class ServiceMetadataEndpointProcess(BaseModel):
    """Process information in the Peppol network."""

    endpoints: List[ServiceMetadataEndpointProcessEndpoint]
    """List of endpoints supporting this process"""

    process_id: ServiceMetadataEndpointProcessProcessID = FieldInfo(alias="processId")
    """Identifier of the process"""


class ServiceMetadataEndpoint(BaseModel):
    """Information about a Peppol participant's endpoint."""

    document_types: List[ServiceMetadataEndpointDocumentType] = FieldInfo(alias="documentTypes")
    """List of document types supported by this endpoint"""

    status: str
    """Status of the endpoint lookup: 'success', 'error', or 'pending'"""

    url: str
    """URL of the endpoint"""

    error: Optional[str] = None
    """Error message if endpoint lookup failed"""

    processes: Optional[List[ServiceMetadataEndpointProcess]] = None
    """List of processes supported by this endpoint"""


class ServiceMetadata(BaseModel):
    """Service metadata information for the Peppol participant"""

    endpoints: List[ServiceMetadataEndpoint]
    """List of endpoints found for the Peppol participant"""

    query_time_ms: float = FieldInfo(alias="queryTimeMs")
    """Time taken to query the service metadata in milliseconds"""

    status: str
    """Status of the service metadata lookup: 'success', 'error', or 'pending'"""

    error: Optional[str] = None
    """Error message if service metadata lookup failed"""


class LookupRetrieveResponse(BaseModel):
    """Response from a Peppol ID lookup operation.

    This model represents the complete result of validating and looking up a Peppol ID
    in the Peppol network, including DNS information, service metadata, business card
    details, and certificate information.

    Example:
        A successful lookup for a Peppol ID "0192:991825827" would return DNS information,
        service metadata with supported document types and processes, business card information
        with organization details, and certificate data.
    """

    business_card: BusinessCard = FieldInfo(alias="businessCard")
    """Business card information for the Peppol participant"""

    certificates: List[Certificate]
    """List of certificates found for the Peppol participant"""

    dns_info: DNSInfo = FieldInfo(alias="dnsInfo")
    """Information about the DNS lookup performed"""

    errors: List[str]
    """List of error messages if any errors occurred during the lookup"""

    execution_time_ms: float = FieldInfo(alias="executionTimeMs")
    """Total execution time of the lookup operation in milliseconds"""

    query_metadata: QueryMetadata = FieldInfo(alias="queryMetadata")
    """Metadata about the query that was performed"""

    service_metadata: ServiceMetadata = FieldInfo(alias="serviceMetadata")
    """Service metadata information for the Peppol participant"""

    status: str
    """Overall status of the lookup: 'success' or 'error'"""
