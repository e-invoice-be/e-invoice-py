# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from e_invoice_api import EInvoice, AsyncEInvoice
from e_invoice_api.types import (
    UblDocumentValidation,
    ValidateValidatePeppolIDResponse,
)
from e_invoice_api._utils import parse_date

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestValidate:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_validate_json(self, client: EInvoice) -> None:
        validate = client.validate.validate_json()
        assert_matches_type(UblDocumentValidation, validate, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_validate_json_with_all_params(self, client: EInvoice) -> None:
        validate = client.validate.validate_json(
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
        assert_matches_type(UblDocumentValidation, validate, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_validate_json(self, client: EInvoice) -> None:
        response = client.validate.with_raw_response.validate_json()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validate = response.parse()
        assert_matches_type(UblDocumentValidation, validate, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_validate_json(self, client: EInvoice) -> None:
        with client.validate.with_streaming_response.validate_json() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validate = response.parse()
            assert_matches_type(UblDocumentValidation, validate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_validate_peppol_id(self, client: EInvoice) -> None:
        validate = client.validate.validate_peppol_id(
            peppol_id="peppol_id",
        )
        assert_matches_type(ValidateValidatePeppolIDResponse, validate, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_validate_peppol_id(self, client: EInvoice) -> None:
        response = client.validate.with_raw_response.validate_peppol_id(
            peppol_id="peppol_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validate = response.parse()
        assert_matches_type(ValidateValidatePeppolIDResponse, validate, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_validate_peppol_id(self, client: EInvoice) -> None:
        with client.validate.with_streaming_response.validate_peppol_id(
            peppol_id="peppol_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validate = response.parse()
            assert_matches_type(ValidateValidatePeppolIDResponse, validate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_validate_ubl(self, client: EInvoice) -> None:
        validate = client.validate.validate_ubl(
            file=b"raw file contents",
        )
        assert_matches_type(UblDocumentValidation, validate, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_validate_ubl(self, client: EInvoice) -> None:
        response = client.validate.with_raw_response.validate_ubl(
            file=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validate = response.parse()
        assert_matches_type(UblDocumentValidation, validate, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_validate_ubl(self, client: EInvoice) -> None:
        with client.validate.with_streaming_response.validate_ubl(
            file=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validate = response.parse()
            assert_matches_type(UblDocumentValidation, validate, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncValidate:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_validate_json(self, async_client: AsyncEInvoice) -> None:
        validate = await async_client.validate.validate_json()
        assert_matches_type(UblDocumentValidation, validate, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_validate_json_with_all_params(self, async_client: AsyncEInvoice) -> None:
        validate = await async_client.validate.validate_json(
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
        assert_matches_type(UblDocumentValidation, validate, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_validate_json(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.validate.with_raw_response.validate_json()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validate = await response.parse()
        assert_matches_type(UblDocumentValidation, validate, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_validate_json(self, async_client: AsyncEInvoice) -> None:
        async with async_client.validate.with_streaming_response.validate_json() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validate = await response.parse()
            assert_matches_type(UblDocumentValidation, validate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_validate_peppol_id(self, async_client: AsyncEInvoice) -> None:
        validate = await async_client.validate.validate_peppol_id(
            peppol_id="peppol_id",
        )
        assert_matches_type(ValidateValidatePeppolIDResponse, validate, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_validate_peppol_id(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.validate.with_raw_response.validate_peppol_id(
            peppol_id="peppol_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validate = await response.parse()
        assert_matches_type(ValidateValidatePeppolIDResponse, validate, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_validate_peppol_id(self, async_client: AsyncEInvoice) -> None:
        async with async_client.validate.with_streaming_response.validate_peppol_id(
            peppol_id="peppol_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validate = await response.parse()
            assert_matches_type(ValidateValidatePeppolIDResponse, validate, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_validate_ubl(self, async_client: AsyncEInvoice) -> None:
        validate = await async_client.validate.validate_ubl(
            file=b"raw file contents",
        )
        assert_matches_type(UblDocumentValidation, validate, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_validate_ubl(self, async_client: AsyncEInvoice) -> None:
        response = await async_client.validate.with_raw_response.validate_ubl(
            file=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        validate = await response.parse()
        assert_matches_type(UblDocumentValidation, validate, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_validate_ubl(self, async_client: AsyncEInvoice) -> None:
        async with async_client.validate.with_streaming_response.validate_ubl(
            file=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            validate = await response.parse()
            assert_matches_type(UblDocumentValidation, validate, path=["response"])

        assert cast(Any, response.is_closed) is True
