# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types import (
    DocumentResponse,
    DocumentDeleteResponse,
)
from e_invoice_api._utils import parse_date

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDocuments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: EInvoice) -> None:
        document = client.documents.create()
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: EInvoice) -> None:
        document = client.documents.create(
            amount_due=0,
            attachments=[
                {
                    "file_name": "file_name",
                    "file_data": "file_data",
                    "file_size": 0,
                    "file_type": "file_type",
                }
            ],
            billing_address="billing_address",
            billing_address_recipient="billing_address_recipient",
            currency="EUR",
            customer_address="customer_address",
            customer_address_recipient="customer_address_recipient",
            customer_email="customer_email",
            customer_id="customer_id",
            customer_name="customer_name",
            customer_tax_id="customer_tax_id",
            direction="INBOUND",
            document_type="INVOICE",
            due_date=parse_date("2019-12-27"),
            invoice_date=parse_date("2019-12-27"),
            invoice_id="invoice_id",
            invoice_total=0,
            items=[
                {
                    "amount": 0,
                    "date": None,
                    "description": "description",
                    "product_code": "product_code",
                    "quantity": 0,
                    "tax": 0,
                    "tax_rate": "tax_rate",
                    "unit": "10",
                    "unit_price": 0,
                }
            ],
            note="note",
            payment_details=[
                {
                    "bank_account_number": "bank_account_number",
                    "iban": "iban",
                    "payment_reference": "payment_reference",
                    "swift": "swift",
                }
            ],
            payment_term="payment_term",
            previous_unpaid_balance=0,
            purchase_order="purchase_order",
            remittance_address="remittance_address",
            remittance_address_recipient="remittance_address_recipient",
            service_address="service_address",
            service_address_recipient="service_address_recipient",
            service_end_date=parse_date("2019-12-27"),
            service_start_date=parse_date("2019-12-27"),
            shipping_address="shipping_address",
            shipping_address_recipient="shipping_address_recipient",
            state="DRAFT",
            subtotal=0,
            tax_details=[
                {
                    "amount": 0,
                    "rate": "rate",
                }
            ],
            total_discount=0,
            total_tax=0,
            vendor_address="vendor_address",
            vendor_address_recipient="vendor_address_recipient",
            vendor_email="vendor_email",
            vendor_name="vendor_name",
            vendor_tax_id="vendor_tax_id",
        )
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: EInvoice) -> None:
        response = client.documents.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: EInvoice) -> None:
        with client.documents.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(DocumentResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: EInvoice) -> None:
        document = client.documents.retrieve(
            "document_id",
        )
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: EInvoice) -> None:
        response = client.documents.with_raw_response.retrieve(
            "document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: EInvoice) -> None:
        with client.documents.with_streaming_response.retrieve(
            "document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(DocumentResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete(self, client: EInvoice) -> None:
        document = client.documents.delete(
            "document_id",
        )
        assert_matches_type(DocumentDeleteResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: EInvoice) -> None:
        response = client.documents.with_raw_response.delete(
            "document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(DocumentDeleteResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: EInvoice) -> None:
        with client.documents.with_streaming_response.delete(
            "document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(DocumentDeleteResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_send(self, client: EInvoice) -> None:
        document = client.documents.send(
            document_id="document_id",
        )
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_send_with_all_params(self, client: EInvoice) -> None:
        document = client.documents.send(
            document_id="document_id",
            email="email",
            receiver_peppol_id="receiver_peppol_id",
            receiver_peppol_scheme="receiver_peppol_scheme",
            sender_peppol_id="sender_peppol_id",
            sender_peppol_scheme="sender_peppol_scheme",
        )
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_send(self, client: EInvoice) -> None:
        response = client.documents.with_raw_response.send(
            document_id="document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_send(self, client: EInvoice) -> None:
        with client.documents.with_streaming_response.send(
            document_id="document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(DocumentResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_send(self, client: EInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.documents.with_raw_response.send(
                document_id="",
            )


class TestAsyncDocuments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncEInvoice) -> None:
        document = await async_client.documents.create()
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEInvoice) -> None:
        document = await async_client.documents.create(
            amount_due=0,
            attachments=[
                {
                    "file_name": "file_name",
                    "file_data": "file_data",
                    "file_size": 0,
                    "file_type": "file_type",
                }
            ],
            billing_address="billing_address",
            billing_address_recipient="billing_address_recipient",
            currency="EUR",
            customer_address="customer_address",
            customer_address_recipient="customer_address_recipient",
            customer_email="customer_email",
            customer_id="customer_id",
            customer_name="customer_name",
            customer_tax_id="customer_tax_id",
            direction="INBOUND",
            document_type="INVOICE",
            due_date=parse_date("2019-12-27"),
            invoice_date=parse_date("2019-12-27"),
            invoice_id="invoice_id",
            invoice_total=0,
            items=[
                {
                    "amount": 0,
                    "date": None,
                    "description": "description",
                    "product_code": "product_code",
                    "quantity": 0,
                    "tax": 0,
                    "tax_rate": "tax_rate",
                    "unit": "10",
                    "unit_price": 0,
                }
            ],
            note="note",
            payment_details=[
                {
                    "bank_account_number": "bank_account_number",
                    "iban": "iban",
                    "payment_reference": "payment_reference",
                    "swift": "swift",
                }
            ],
            payment_term="payment_term",
            previous_unpaid_balance=0,
            purchase_order="purchase_order",
            remittance_address="remittance_address",
            remittance_address_recipient="remittance_address_recipient",
            service_address="service_address",
            service_address_recipient="service_address_recipient",
            service_end_date=parse_date("2019-12-27"),
            service_start_date=parse_date("2019-12-27"),
            shipping_address="shipping_address",
            shipping_address_recipient="shipping_address_recipient",
            state="DRAFT",
            subtotal=0,
            tax_details=[
                {
                    "amount": 0,
                    "rate": "rate",
                }
            ],
            total_discount=0,
            total_tax=0,
            vendor_address="vendor_address",
            vendor_address_recipient="vendor_address_recipient",
            vendor_email="vendor_email",
            vendor_name="vendor_name",
            vendor_tax_id="vendor_tax_id",
        )
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.documents.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEInvoice) -> None:
        async with async_client.documents.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(DocumentResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEInvoice) -> None:
        document = await async_client.documents.retrieve(
            "document_id",
        )
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.documents.with_raw_response.retrieve(
            "document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEInvoice) -> None:
        async with async_client.documents.with_streaming_response.retrieve(
            "document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(DocumentResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.documents.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncEInvoice) -> None:
        document = await async_client.documents.delete(
            "document_id",
        )
        assert_matches_type(DocumentDeleteResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.documents.with_raw_response.delete(
            "document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(DocumentDeleteResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncEInvoice) -> None:
        async with async_client.documents.with_streaming_response.delete(
            "document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(DocumentDeleteResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.documents.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_send(self, async_client: AsyncEInvoice) -> None:
        document = await async_client.documents.send(
            document_id="document_id",
        )
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_send_with_all_params(self, async_client: AsyncEInvoice) -> None:
        document = await async_client.documents.send(
            document_id="document_id",
            email="email",
            receiver_peppol_id="receiver_peppol_id",
            receiver_peppol_scheme="receiver_peppol_scheme",
            sender_peppol_id="sender_peppol_id",
            sender_peppol_scheme="sender_peppol_scheme",
        )
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_send(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.documents.with_raw_response.send(
            document_id="document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(DocumentResponse, document, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_send(self, async_client: AsyncEInvoice) -> None:
        async with async_client.documents.with_streaming_response.send(
            document_id="document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(DocumentResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_send(self, async_client: AsyncEInvoice) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.documents.with_raw_response.send(
                document_id="",
            )
