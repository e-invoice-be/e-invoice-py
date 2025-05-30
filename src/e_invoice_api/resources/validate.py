# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Mapping, Iterable, Optional, cast
from datetime import date

import httpx

from ..types import (
    CurrencyCode,
    DocumentType,
    DocumentState,
    DocumentDirection,
    validate_validate_ubl_params,
    validate_validate_json_params,
    validate_validate_peppol_id_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven, FileTypes
from .._utils import extract_files, maybe_transform, deepcopy_minimal, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.currency_code import CurrencyCode
from ..types.document_type import DocumentType
from ..types.document_state import DocumentState
from ..types.document_direction import DocumentDirection
from ..types.ubl_document_validation import UblDocumentValidation
from ..types.payment_detail_create_param import PaymentDetailCreateParam
from ..types.document_attachment_create_param import DocumentAttachmentCreateParam
from ..types.validate_validate_peppol_id_response import ValidateValidatePeppolIDResponse

__all__ = ["ValidateResource", "AsyncValidateResource"]


class ValidateResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ValidateResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return ValidateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ValidateResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return ValidateResourceWithStreamingResponse(self)

    def validate_json(
        self,
        *,
        amount_due: Union[float, str, None] | NotGiven = NOT_GIVEN,
        attachments: Optional[Iterable[DocumentAttachmentCreateParam]] | NotGiven = NOT_GIVEN,
        billing_address: Optional[str] | NotGiven = NOT_GIVEN,
        billing_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        currency: CurrencyCode | NotGiven = NOT_GIVEN,
        customer_address: Optional[str] | NotGiven = NOT_GIVEN,
        customer_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        customer_email: Optional[str] | NotGiven = NOT_GIVEN,
        customer_id: Optional[str] | NotGiven = NOT_GIVEN,
        customer_name: Optional[str] | NotGiven = NOT_GIVEN,
        customer_tax_id: Optional[str] | NotGiven = NOT_GIVEN,
        direction: DocumentDirection | NotGiven = NOT_GIVEN,
        document_type: DocumentType | NotGiven = NOT_GIVEN,
        due_date: Union[str, date, None] | NotGiven = NOT_GIVEN,
        invoice_date: Union[str, date, None] | NotGiven = NOT_GIVEN,
        invoice_id: Optional[str] | NotGiven = NOT_GIVEN,
        invoice_total: Union[float, str, None] | NotGiven = NOT_GIVEN,
        items: Optional[Iterable[validate_validate_json_params.Item]] | NotGiven = NOT_GIVEN,
        note: Optional[str] | NotGiven = NOT_GIVEN,
        payment_details: Optional[Iterable[PaymentDetailCreateParam]] | NotGiven = NOT_GIVEN,
        payment_term: Optional[str] | NotGiven = NOT_GIVEN,
        previous_unpaid_balance: Union[float, str, None] | NotGiven = NOT_GIVEN,
        purchase_order: Optional[str] | NotGiven = NOT_GIVEN,
        remittance_address: Optional[str] | NotGiven = NOT_GIVEN,
        remittance_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        service_address: Optional[str] | NotGiven = NOT_GIVEN,
        service_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        service_end_date: Union[str, date, None] | NotGiven = NOT_GIVEN,
        service_start_date: Union[str, date, None] | NotGiven = NOT_GIVEN,
        shipping_address: Optional[str] | NotGiven = NOT_GIVEN,
        shipping_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        state: DocumentState | NotGiven = NOT_GIVEN,
        subtotal: Union[float, str, None] | NotGiven = NOT_GIVEN,
        tax_details: Optional[Iterable[validate_validate_json_params.TaxDetail]] | NotGiven = NOT_GIVEN,
        total_discount: Union[float, str, None] | NotGiven = NOT_GIVEN,
        total_tax: Union[float, str, None] | NotGiven = NOT_GIVEN,
        vendor_address: Optional[str] | NotGiven = NOT_GIVEN,
        vendor_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        vendor_email: Optional[str] | NotGiven = NOT_GIVEN,
        vendor_name: Optional[str] | NotGiven = NOT_GIVEN,
        vendor_tax_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UblDocumentValidation:
        """
        Validate if the JSON document can be converted to a valid UBL document

        Args:
          currency: Currency of the invoice

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/validate/json",
            body=maybe_transform(
                {
                    "amount_due": amount_due,
                    "attachments": attachments,
                    "billing_address": billing_address,
                    "billing_address_recipient": billing_address_recipient,
                    "currency": currency,
                    "customer_address": customer_address,
                    "customer_address_recipient": customer_address_recipient,
                    "customer_email": customer_email,
                    "customer_id": customer_id,
                    "customer_name": customer_name,
                    "customer_tax_id": customer_tax_id,
                    "direction": direction,
                    "document_type": document_type,
                    "due_date": due_date,
                    "invoice_date": invoice_date,
                    "invoice_id": invoice_id,
                    "invoice_total": invoice_total,
                    "items": items,
                    "note": note,
                    "payment_details": payment_details,
                    "payment_term": payment_term,
                    "previous_unpaid_balance": previous_unpaid_balance,
                    "purchase_order": purchase_order,
                    "remittance_address": remittance_address,
                    "remittance_address_recipient": remittance_address_recipient,
                    "service_address": service_address,
                    "service_address_recipient": service_address_recipient,
                    "service_end_date": service_end_date,
                    "service_start_date": service_start_date,
                    "shipping_address": shipping_address,
                    "shipping_address_recipient": shipping_address_recipient,
                    "state": state,
                    "subtotal": subtotal,
                    "tax_details": tax_details,
                    "total_discount": total_discount,
                    "total_tax": total_tax,
                    "vendor_address": vendor_address,
                    "vendor_address_recipient": vendor_address_recipient,
                    "vendor_email": vendor_email,
                    "vendor_name": vendor_name,
                    "vendor_tax_id": vendor_tax_id,
                },
                validate_validate_json_params.ValidateValidateJsonParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UblDocumentValidation,
        )

    def validate_peppol_id(
        self,
        *,
        peppol_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ValidateValidatePeppolIDResponse:
        """
        Validate if a Peppol ID exists in the Peppol network and retrieve supported
        document types. The peppol_id must be in the form of `<scheme>:<id>`. The scheme
        is a 4-digit code representing the identifier scheme, and the id is the actual
        identifier value. For example, for a Belgian company it is `0208:0123456789`
        (where 0208 is the scheme for Belgian enterprises, followed by the 10 digits of
        the official BTW / KBO number).

        Args:
          peppol_id: Peppol ID in the format `<scheme>:<id>`. Example: `0208:1018265814` for a
              Belgian company.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/validate/peppol-id",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"peppol_id": peppol_id}, validate_validate_peppol_id_params.ValidateValidatePeppolIDParams
                ),
            ),
            cast_to=ValidateValidatePeppolIDResponse,
        )

    def validate_ubl(
        self,
        *,
        file: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UblDocumentValidation:
        """
        Validate the correctness of a UBL document

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal({"file": file})
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/api/validate/ubl",
            body=maybe_transform(body, validate_validate_ubl_params.ValidateValidateUblParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UblDocumentValidation,
        )


class AsyncValidateResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncValidateResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#accessing-raw-response-data-eg-headers
        """
        return AsyncValidateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncValidateResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/e-invoice-be/e-invoice-py#with_streaming_response
        """
        return AsyncValidateResourceWithStreamingResponse(self)

    async def validate_json(
        self,
        *,
        amount_due: Union[float, str, None] | NotGiven = NOT_GIVEN,
        attachments: Optional[Iterable[DocumentAttachmentCreateParam]] | NotGiven = NOT_GIVEN,
        billing_address: Optional[str] | NotGiven = NOT_GIVEN,
        billing_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        currency: CurrencyCode | NotGiven = NOT_GIVEN,
        customer_address: Optional[str] | NotGiven = NOT_GIVEN,
        customer_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        customer_email: Optional[str] | NotGiven = NOT_GIVEN,
        customer_id: Optional[str] | NotGiven = NOT_GIVEN,
        customer_name: Optional[str] | NotGiven = NOT_GIVEN,
        customer_tax_id: Optional[str] | NotGiven = NOT_GIVEN,
        direction: DocumentDirection | NotGiven = NOT_GIVEN,
        document_type: DocumentType | NotGiven = NOT_GIVEN,
        due_date: Union[str, date, None] | NotGiven = NOT_GIVEN,
        invoice_date: Union[str, date, None] | NotGiven = NOT_GIVEN,
        invoice_id: Optional[str] | NotGiven = NOT_GIVEN,
        invoice_total: Union[float, str, None] | NotGiven = NOT_GIVEN,
        items: Optional[Iterable[validate_validate_json_params.Item]] | NotGiven = NOT_GIVEN,
        note: Optional[str] | NotGiven = NOT_GIVEN,
        payment_details: Optional[Iterable[PaymentDetailCreateParam]] | NotGiven = NOT_GIVEN,
        payment_term: Optional[str] | NotGiven = NOT_GIVEN,
        previous_unpaid_balance: Union[float, str, None] | NotGiven = NOT_GIVEN,
        purchase_order: Optional[str] | NotGiven = NOT_GIVEN,
        remittance_address: Optional[str] | NotGiven = NOT_GIVEN,
        remittance_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        service_address: Optional[str] | NotGiven = NOT_GIVEN,
        service_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        service_end_date: Union[str, date, None] | NotGiven = NOT_GIVEN,
        service_start_date: Union[str, date, None] | NotGiven = NOT_GIVEN,
        shipping_address: Optional[str] | NotGiven = NOT_GIVEN,
        shipping_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        state: DocumentState | NotGiven = NOT_GIVEN,
        subtotal: Union[float, str, None] | NotGiven = NOT_GIVEN,
        tax_details: Optional[Iterable[validate_validate_json_params.TaxDetail]] | NotGiven = NOT_GIVEN,
        total_discount: Union[float, str, None] | NotGiven = NOT_GIVEN,
        total_tax: Union[float, str, None] | NotGiven = NOT_GIVEN,
        vendor_address: Optional[str] | NotGiven = NOT_GIVEN,
        vendor_address_recipient: Optional[str] | NotGiven = NOT_GIVEN,
        vendor_email: Optional[str] | NotGiven = NOT_GIVEN,
        vendor_name: Optional[str] | NotGiven = NOT_GIVEN,
        vendor_tax_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UblDocumentValidation:
        """
        Validate if the JSON document can be converted to a valid UBL document

        Args:
          currency: Currency of the invoice

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/validate/json",
            body=await async_maybe_transform(
                {
                    "amount_due": amount_due,
                    "attachments": attachments,
                    "billing_address": billing_address,
                    "billing_address_recipient": billing_address_recipient,
                    "currency": currency,
                    "customer_address": customer_address,
                    "customer_address_recipient": customer_address_recipient,
                    "customer_email": customer_email,
                    "customer_id": customer_id,
                    "customer_name": customer_name,
                    "customer_tax_id": customer_tax_id,
                    "direction": direction,
                    "document_type": document_type,
                    "due_date": due_date,
                    "invoice_date": invoice_date,
                    "invoice_id": invoice_id,
                    "invoice_total": invoice_total,
                    "items": items,
                    "note": note,
                    "payment_details": payment_details,
                    "payment_term": payment_term,
                    "previous_unpaid_balance": previous_unpaid_balance,
                    "purchase_order": purchase_order,
                    "remittance_address": remittance_address,
                    "remittance_address_recipient": remittance_address_recipient,
                    "service_address": service_address,
                    "service_address_recipient": service_address_recipient,
                    "service_end_date": service_end_date,
                    "service_start_date": service_start_date,
                    "shipping_address": shipping_address,
                    "shipping_address_recipient": shipping_address_recipient,
                    "state": state,
                    "subtotal": subtotal,
                    "tax_details": tax_details,
                    "total_discount": total_discount,
                    "total_tax": total_tax,
                    "vendor_address": vendor_address,
                    "vendor_address_recipient": vendor_address_recipient,
                    "vendor_email": vendor_email,
                    "vendor_name": vendor_name,
                    "vendor_tax_id": vendor_tax_id,
                },
                validate_validate_json_params.ValidateValidateJsonParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UblDocumentValidation,
        )

    async def validate_peppol_id(
        self,
        *,
        peppol_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ValidateValidatePeppolIDResponse:
        """
        Validate if a Peppol ID exists in the Peppol network and retrieve supported
        document types. The peppol_id must be in the form of `<scheme>:<id>`. The scheme
        is a 4-digit code representing the identifier scheme, and the id is the actual
        identifier value. For example, for a Belgian company it is `0208:0123456789`
        (where 0208 is the scheme for Belgian enterprises, followed by the 10 digits of
        the official BTW / KBO number).

        Args:
          peppol_id: Peppol ID in the format `<scheme>:<id>`. Example: `0208:1018265814` for a
              Belgian company.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/validate/peppol-id",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"peppol_id": peppol_id}, validate_validate_peppol_id_params.ValidateValidatePeppolIDParams
                ),
            ),
            cast_to=ValidateValidatePeppolIDResponse,
        )

    async def validate_ubl(
        self,
        *,
        file: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UblDocumentValidation:
        """
        Validate the correctness of a UBL document

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal({"file": file})
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/api/validate/ubl",
            body=await async_maybe_transform(body, validate_validate_ubl_params.ValidateValidateUblParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UblDocumentValidation,
        )


class ValidateResourceWithRawResponse:
    def __init__(self, validate: ValidateResource) -> None:
        self._validate = validate

        self.validate_json = to_raw_response_wrapper(
            validate.validate_json,
        )
        self.validate_peppol_id = to_raw_response_wrapper(
            validate.validate_peppol_id,
        )
        self.validate_ubl = to_raw_response_wrapper(
            validate.validate_ubl,
        )


class AsyncValidateResourceWithRawResponse:
    def __init__(self, validate: AsyncValidateResource) -> None:
        self._validate = validate

        self.validate_json = async_to_raw_response_wrapper(
            validate.validate_json,
        )
        self.validate_peppol_id = async_to_raw_response_wrapper(
            validate.validate_peppol_id,
        )
        self.validate_ubl = async_to_raw_response_wrapper(
            validate.validate_ubl,
        )


class ValidateResourceWithStreamingResponse:
    def __init__(self, validate: ValidateResource) -> None:
        self._validate = validate

        self.validate_json = to_streamed_response_wrapper(
            validate.validate_json,
        )
        self.validate_peppol_id = to_streamed_response_wrapper(
            validate.validate_peppol_id,
        )
        self.validate_ubl = to_streamed_response_wrapper(
            validate.validate_ubl,
        )


class AsyncValidateResourceWithStreamingResponse:
    def __init__(self, validate: AsyncValidateResource) -> None:
        self._validate = validate

        self.validate_json = async_to_streamed_response_wrapper(
            validate.validate_json,
        )
        self.validate_peppol_id = async_to_streamed_response_wrapper(
            validate.validate_peppol_id,
        )
        self.validate_ubl = async_to_streamed_response_wrapper(
            validate.validate_ubl,
        )
