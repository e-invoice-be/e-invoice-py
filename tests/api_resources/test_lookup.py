from __future__ import annotations

import os

import httpx
import pytest
from respx import MockRouter

from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types import Certificate, LookupRetrieveResponse, LookupRetrieveParticipantsResponse
from e_invoice_api.resources.lookup import (
    LookupResourceWithRawResponse,
    AsyncLookupResourceWithRawResponse,
    LookupResourceWithStreamingResponse,
    AsyncLookupResourceWithStreamingResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")

PEPPOL_ID = "0208:1018265814"

LOOKUP_PAYLOAD = {
    "businessCard": {
        "entities": [
            {
                "additionalInformation": ["Main office"],
                "countryCode": "BE",
                "name": "Acme BV",
                "registrationDate": "2024-03-01",
            }
        ],
        "queryTimeMs": 12.5,
        "status": "success",
    },
    "certificates": [{"status": "success", "details": {"subject": "CN=PBE000001"}}],
    "dnsInfo": {
        "dnsRecords": [{"ip": "192.0.2.10"}],
        "smlHostname": "edelivery.tech.ec.europa.eu",
        "status": "success",
        "lookupMethod": "naptr",
        "smpHostname": "smp.example.com",
    },
    "errors": [],
    "executionTimeMs": 87.25,
    "queryMetadata": {
        "identifierScheme": "iso6523-actorid-upis",
        "identifierValue": PEPPOL_ID,
        "smlDomain": "edelivery.tech.ec.europa.eu",
        "timestamp": "2026-02-01T09:00:00Z",
        "version": "1.0",
    },
    "serviceMetadata": {
        "endpoints": [
            {
                "documentTypes": [{"scheme": "busdox-docid-qns", "value": "urn:invoice"}],
                "status": "success",
                "url": "https://smp.example.com/doc",
                "processes": [
                    {
                        "endpoints": [
                            {
                                "address": "https://ap.example.com/as4",
                                "transportProfile": "peppol-transport-as4-v2_0",
                                "certificate": {"status": "success"},
                                "serviceDescription": "AS4 access point",
                            }
                        ],
                        "processId": {"scheme": "cenbii-procid-ubl", "value": "urn:billing:01"},
                    }
                ],
            }
        ],
        "queryTimeMs": 30.0,
        "status": "success",
    },
    "status": "success",
}

PARTICIPANTS_PAYLOAD = {
    "query_terms": "acme",
    "search_date": "2026-02-01",
    "total_count": 42,
    "used_count": 1,
    "participants": [
        {
            "peppol_id": "1018265814",
            "peppol_scheme": "0208",
            "document_types": [{"scheme": "busdox-docid-qns", "value": "urn:invoice"}],
            "entities": [
                {
                    "name": "Acme BV",
                    "country_code": "BE",
                    "identifiers": [{"scheme": "VAT", "value": "BE1018265814"}],
                    "website": "https://acme.example",
                }
            ],
        }
    ],
}


def _assert_lookup(lookup: LookupRetrieveResponse) -> None:
    assert isinstance(lookup, LookupRetrieveResponse)
    assert lookup.status == "success"
    assert lookup.errors == []
    assert lookup.execution_time_ms == 87.25
    assert lookup.business_card.query_time_ms == 12.5
    entity = lookup.business_card.entities[0]
    assert (entity.name, entity.country_code, entity.registration_date) == ("Acme BV", "BE", "2024-03-01")
    assert entity.additional_information == ["Main office"]
    assert isinstance(lookup.certificates[0], Certificate)
    assert lookup.certificates[0].details == {"subject": "CN=PBE000001"}
    assert [r.ip for r in lookup.dns_info.dns_records] == ["192.0.2.10"]
    assert lookup.dns_info.lookup_method == "naptr"
    assert lookup.dns_info.smp_hostname == "smp.example.com"
    assert lookup.query_metadata.identifier_value == PEPPOL_ID
    endpoint = lookup.service_metadata.endpoints[0]
    assert endpoint.document_types[0].value == "urn:invoice"
    assert endpoint.processes is not None
    process = endpoint.processes[0]
    assert process.process_id.value == "urn:billing:01"
    assert process.endpoints[0].transport_profile == "peppol-transport-as4-v2_0"
    assert process.endpoints[0].certificate is not None
    assert process.endpoints[0].certificate.status == "success"


def _assert_participants(result: LookupRetrieveParticipantsResponse) -> None:
    assert isinstance(result, LookupRetrieveParticipantsResponse)
    assert (result.query_terms, result.search_date, result.total_count, result.used_count) == (
        "acme",
        "2026-02-01",
        42,
        1,
    )
    assert result.participants is not None
    participant = result.participants[0]
    assert (participant.peppol_scheme, participant.peppol_id) == ("0208", "1018265814")
    assert participant.document_types is not None
    assert participant.document_types[0].scheme == "busdox-docid-qns"
    assert participant.entities is not None
    assert participant.entities[0].identifiers is not None
    assert participant.entities[0].identifiers[0].value == "BE1018265814"


class TestLookup:
    def test_resource_exposes_wrapper_properties(self, client: EInvoice) -> None:
        raw = client.lookup.with_raw_response
        streaming = client.lookup.with_streaming_response

        assert isinstance(raw, LookupResourceWithRawResponse)
        assert isinstance(streaming, LookupResourceWithStreamingResponse)
        assert client.lookup.with_raw_response is raw
        assert client.lookup.with_streaming_response is streaming

    @pytest.mark.respx(base_url=base_url)
    def test_retrieve_sends_peppol_id(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/lookup").mock(return_value=httpx.Response(200, json=LOOKUP_PAYLOAD))

        lookup = client.lookup.retrieve(peppol_id=PEPPOL_ID)

        assert route.call_count == 1
        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == "/api/lookup"
        assert dict(request.url.params) == {"peppol_id": PEPPOL_ID}
        _assert_lookup(lookup)

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/lookup").mock(
            return_value=httpx.Response(200, json=LOOKUP_PAYLOAD, headers={"x-request-id": "req_lookup"})
        )

        response = client.lookup.with_raw_response.retrieve(peppol_id=PEPPOL_ID)

        assert response.is_closed is True
        assert response.headers["x-request-id"] == "req_lookup"
        assert response.http_request.url.params["peppol_id"] == PEPPOL_ID
        _assert_lookup(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/lookup").mock(return_value=httpx.Response(200, json=LOOKUP_PAYLOAD))

        with client.lookup.with_streaming_response.retrieve(peppol_id=PEPPOL_ID) as response:
            assert not response.is_closed
            _assert_lookup(response.parse())

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    def test_retrieve_participants_sends_query_and_country(self, respx_mock: MockRouter, client: EInvoice) -> None:
        route = respx_mock.get("/api/lookup/participants").mock(
            return_value=httpx.Response(200, json=PARTICIPANTS_PAYLOAD)
        )

        result = client.lookup.retrieve_participants(query="acme", country_code="BE")

        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == "/api/lookup/participants"
        assert dict(request.url.params) == {"query": "acme", "country_code": "BE"}
        _assert_participants(result)

    @pytest.mark.respx(base_url=base_url)
    def test_retrieve_participants_omits_country_and_defaults_participants(
        self, respx_mock: MockRouter, client: EInvoice
    ) -> None:
        route = respx_mock.get("/api/lookup/participants").mock(
            return_value=httpx.Response(
                200, json={"query_terms": "nobody", "search_date": "2026-02-01", "total_count": 0, "used_count": 0}
            )
        )

        result = client.lookup.retrieve_participants(query="nobody")

        assert dict(route.calls.last.request.url.params) == {"query": "nobody"}
        assert result.total_count == 0
        assert result.participants is None

    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_retrieve_participants(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/lookup/participants").mock(return_value=httpx.Response(200, json=PARTICIPANTS_PAYLOAD))

        response = client.lookup.with_raw_response.retrieve_participants(query="acme")

        assert response.is_closed is True
        assert response.status_code == 200
        assert dict(response.http_request.url.params) == {"query": "acme"}
        _assert_participants(response.parse())

    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_retrieve_participants(self, respx_mock: MockRouter, client: EInvoice) -> None:
        respx_mock.get("/api/lookup/participants").mock(return_value=httpx.Response(200, json=PARTICIPANTS_PAYLOAD))

        with client.lookup.with_streaming_response.retrieve_participants(query="acme", country_code="BE") as response:
            assert not response.is_closed
            _assert_participants(response.parse())

        assert response.is_closed is True


class TestAsyncLookup:
    def test_resource_exposes_wrapper_properties(self, async_client: AsyncEInvoice) -> None:
        raw = async_client.lookup.with_raw_response
        streaming = async_client.lookup.with_streaming_response

        assert isinstance(raw, AsyncLookupResourceWithRawResponse)
        assert isinstance(streaming, AsyncLookupResourceWithStreamingResponse)
        assert async_client.lookup.with_raw_response is raw
        assert async_client.lookup.with_streaming_response is streaming

    @pytest.mark.respx(base_url=base_url)
    async def test_retrieve_sends_peppol_id(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        route = respx_mock.get("/api/lookup").mock(return_value=httpx.Response(200, json=LOOKUP_PAYLOAD))

        lookup = await async_client.lookup.retrieve(peppol_id=PEPPOL_ID)

        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == "/api/lookup"
        assert dict(request.url.params) == {"peppol_id": PEPPOL_ID}
        _assert_lookup(lookup)

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/lookup").mock(return_value=httpx.Response(200, json=LOOKUP_PAYLOAD))

        response = await async_client.lookup.with_raw_response.retrieve(peppol_id=PEPPOL_ID)

        assert response.is_closed is True
        assert response.http_request.url.params["peppol_id"] == PEPPOL_ID
        _assert_lookup(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve(self, respx_mock: MockRouter, async_client: AsyncEInvoice) -> None:
        respx_mock.get("/api/lookup").mock(return_value=httpx.Response(200, json=LOOKUP_PAYLOAD))

        async with async_client.lookup.with_streaming_response.retrieve(peppol_id=PEPPOL_ID) as response:
            assert not response.is_closed
            _assert_lookup(await response.parse())

        assert response.is_closed is True

    @pytest.mark.respx(base_url=base_url)
    async def test_retrieve_participants_sends_query_and_country(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        route = respx_mock.get("/api/lookup/participants").mock(
            return_value=httpx.Response(200, json=PARTICIPANTS_PAYLOAD)
        )

        result = await async_client.lookup.retrieve_participants(query="acme", country_code="BE")

        request = route.calls.last.request
        assert request.method == "GET"
        assert request.url.path == "/api/lookup/participants"
        assert dict(request.url.params) == {"query": "acme", "country_code": "BE"}
        _assert_participants(result)

    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_retrieve_participants(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        respx_mock.get("/api/lookup/participants").mock(return_value=httpx.Response(200, json=PARTICIPANTS_PAYLOAD))

        response = await async_client.lookup.with_raw_response.retrieve_participants(query="acme")

        assert response.is_closed is True
        assert dict(response.http_request.url.params) == {"query": "acme"}
        _assert_participants(await response.parse())

    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_retrieve_participants(
        self, respx_mock: MockRouter, async_client: AsyncEInvoice
    ) -> None:
        respx_mock.get("/api/lookup/participants").mock(return_value=httpx.Response(200, json=PARTICIPANTS_PAYLOAD))

        async with async_client.lookup.with_streaming_response.retrieve_participants(query="acme") as response:
            assert not response.is_closed
            _assert_participants(await response.parse())

        assert response.is_closed is True
