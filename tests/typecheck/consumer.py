# pyright: strict

# Typical use of the public API by a user of the SDK.
# This file is not a test. `./scripts/typecheck-consumers` checks it with pyright and mypy,
# the type checkers that our users run. `assert_type` pins the types that they see.

from __future__ import annotations

from typing import List, Optional
from pathlib import Path
from datetime import datetime
from typing_extensions import assert_type

import httpx

import e_invoice_api
from e_invoice_api import EInvoice, APIResponse, AsyncEInvoice, AsyncAPIResponse, resources
from e_invoice_api.types import (
    WebhookResponse,
    DocumentResponse,
    MeRetrieveResponse,
    StatsRetrieveResponse,
    UblDocumentValidation,
    LookupRetrieveResponse,
    DocumentCreateFromPdfResponse,
    ValidateValidatePeppolIDResponse,
)
from e_invoice_api.pagination import SyncDocumentsNumberPage, AsyncDocumentsNumberPage
from e_invoice_api.types.documents import DocumentAttachment


def sync_usage() -> None:
    client = EInvoice(api_key="My API Key", max_retries=2, timeout=20.0)

    document = client.documents.create(
        document_type="INVOICE",
        invoice_id="INV-1",
        invoice_date="2026-01-31",
        customer_name="Customer BV",
        items=[{"description": "Consulting", "quantity": 2, "unit_price": "100.00"}],
    )
    assert_type(document, DocumentResponse)
    assert_type(document.id, str)
    assert_type(document.created_at, datetime)
    assert_type(document.invoice_total, Optional[str])
    for item in document.items or []:
        assert_type(item.description, Optional[str])

    assert_type(client.documents.retrieve("doc_123"), DocumentResponse)
    assert_type(client.documents.send("doc_123", receiver_peppol_id="0208:0123456789"), DocumentResponse)
    assert_type(client.documents.attachments.list("doc_123"), List[DocumentAttachment])
    assert_type(client.me.retrieve(), MeRetrieveResponse)
    assert_type(client.with_options(timeout=5.0).me.retrieve().name, str)
    assert_type(client.stats.retrieve(aggregation="MONTH"), StatsRetrieveResponse)

    # file uploads accept a path, bytes or a `(filename, contents, media type)` tuple
    from_pdf = client.documents.create_from_pdf(file=Path("invoice.pdf"), vendor_tax_id="BE0123456789")
    assert_type(from_pdf, DocumentCreateFromPdfResponse)
    assert_type(from_pdf.vendor_name, Optional[str])
    assert_type(client.validate.validate_ubl(file=b"<Invoice/>"), UblDocumentValidation)
    assert_type(
        client.documents.ubl.create_from_ubl(file=("invoice.xml", b"<Invoice/>", "application/xml")),
        DocumentResponse,
    )

    validation = client.validate.validate_json(document_type="INVOICE", invoice_id="INV-1")
    assert_type(validation, UblDocumentValidation)
    assert_type(validation.is_valid, bool)
    for issue in validation.issues:
        assert_type(issue.message, str)
    peppol_id = client.validate.validate_peppol_id(peppol_id="0208:0123456789")
    assert_type(peppol_id, ValidateValidatePeppolIDResponse)
    assert_type(peppol_id.supported_document_types, List[str])

    lookup = client.lookup.retrieve(peppol_id="0208:0123456789")
    assert_type(lookup, LookupRetrieveResponse)
    assert_type(lookup.errors, List[str])

    page = client.inbox.list(page=1, page_size=20, sort_order="desc")
    assert_type(page, SyncDocumentsNumberPage[DocumentResponse])
    assert_type(page.items, List[DocumentResponse])
    assert_type(page.has_next_page(), bool)
    assert_type(page.get_next_page(), SyncDocumentsNumberPage[DocumentResponse])
    for inbox_document in page:
        assert_type(inbox_document, DocumentResponse)
    for sent_document in client.outbox.list_received_documents(sender="0208:0123456789", type="INVOICE"):
        assert_type(sent_document, DocumentResponse)

    webhook = client.webhooks.create(events=["document.received"], url="https://example.com/hook")
    assert_type(webhook, WebhookResponse)
    assert_type(webhook.secret, str)
    assert_type(client.webhooks.update(webhook.id, enabled=False), WebhookResponse)
    assert_type(client.webhooks.list(), List[WebhookResponse])

    raw = client.documents.with_raw_response.retrieve("doc_123")
    assert_type(raw, APIResponse[DocumentResponse])
    assert_type(raw.parse(), DocumentResponse)
    assert_type(raw.headers, httpx.Headers)
    assert_type(client.with_raw_response.documents.retrieve("doc_123"), APIResponse[DocumentResponse])
    assert_type(client.with_raw_response.inbox.list(), APIResponse[SyncDocumentsNumberPage[DocumentResponse]])

    with client.documents.with_streaming_response.retrieve("doc_123") as streamed:
        assert_type(streamed.parse(), DocumentResponse)
    with client.with_streaming_response.webhooks.list() as streamed_webhooks:
        assert_type(streamed_webhooks, APIResponse[List[WebhookResponse]])

    try:
        client.documents.retrieve("doc_123")
    except e_invoice_api.APIConnectionError as err:
        assert_type(err.request, httpx.Request)
    except e_invoice_api.RateLimitError as err:
        assert_type(err.response, httpx.Response)
    except e_invoice_api.APIStatusError as err:
        assert_type(err.status_code, int)


async def async_usage() -> None:
    async with AsyncEInvoice(api_key="My API Key") as client:
        document = await client.documents.create(document_type="CREDIT_NOTE", invoice_id="CN-1")
        assert_type(document, DocumentResponse)
        assert_type(document.id, str)

        from_pdf = await client.documents.create_from_pdf(file=Path("invoice.pdf"))
        assert_type(from_pdf, DocumentCreateFromPdfResponse)
        assert_type(await client.lookup.retrieve(peppol_id="0208:0123456789"), LookupRetrieveResponse)
        assert_type(await client.webhooks.list(), List[WebhookResponse])

        page = await client.inbox.list(page_size=20)
        assert_type(page, AsyncDocumentsNumberPage[DocumentResponse])
        assert_type(await page.get_next_page(), AsyncDocumentsNumberPage[DocumentResponse])
        async for inbox_document in client.inbox.list():
            assert_type(inbox_document, DocumentResponse)
        async for sent_document in client.outbox.list_received_documents():
            assert_type(sent_document, DocumentResponse)

        raw = await client.me.with_raw_response.retrieve()
        assert_type(raw, AsyncAPIResponse[MeRetrieveResponse])
        assert_type(await raw.parse(), MeRetrieveResponse)
        assert_type(
            await client.with_raw_response.validate.validate_peppol_id(peppol_id="0208:0123456789"),
            AsyncAPIResponse[ValidateValidatePeppolIDResponse],
        )

        async with client.me.with_streaming_response.retrieve() as streamed:
            assert_type(await streamed.parse(), MeRetrieveResponse)
        async with client.with_streaming_response.documents.retrieve("doc_123") as streamed_document:
            assert_type(streamed_document, AsyncAPIResponse[DocumentResponse])


# Every resource of `client.with_raw_response` and `client.with_streaming_response`.
def client_level_wrappers(client: EInvoice, async_client: AsyncEInvoice) -> None:
    raw = client.with_raw_response
    assert_type(raw.documents, resources.DocumentsResourceWithRawResponse)
    assert_type(raw.inbox, resources.InboxResourceWithRawResponse)
    assert_type(raw.mailbox, resources.MailboxResourceWithRawResponse)
    assert_type(raw.drafts, resources.DraftsResourceWithRawResponse)
    assert_type(raw.outbox, resources.OutboxResourceWithRawResponse)
    assert_type(raw.validate, resources.ValidateResourceWithRawResponse)
    assert_type(raw.lookup, resources.LookupResourceWithRawResponse)
    assert_type(raw.me, resources.MeResourceWithRawResponse)
    assert_type(raw.stats, resources.StatsResourceWithRawResponse)
    assert_type(raw.conversion, resources.ConversionResourceWithRawResponse)
    assert_type(raw.webhooks, resources.WebhooksResourceWithRawResponse)

    streaming = client.with_streaming_response
    assert_type(streaming.documents, resources.DocumentsResourceWithStreamingResponse)
    assert_type(streaming.inbox, resources.InboxResourceWithStreamingResponse)
    assert_type(streaming.mailbox, resources.MailboxResourceWithStreamingResponse)
    assert_type(streaming.drafts, resources.DraftsResourceWithStreamingResponse)
    assert_type(streaming.outbox, resources.OutboxResourceWithStreamingResponse)
    assert_type(streaming.validate, resources.ValidateResourceWithStreamingResponse)
    assert_type(streaming.lookup, resources.LookupResourceWithStreamingResponse)
    assert_type(streaming.me, resources.MeResourceWithStreamingResponse)
    assert_type(streaming.stats, resources.StatsResourceWithStreamingResponse)
    assert_type(streaming.conversion, resources.ConversionResourceWithStreamingResponse)
    assert_type(streaming.webhooks, resources.WebhooksResourceWithStreamingResponse)

    async_raw = async_client.with_raw_response
    assert_type(async_raw.documents, resources.AsyncDocumentsResourceWithRawResponse)
    assert_type(async_raw.inbox, resources.AsyncInboxResourceWithRawResponse)
    assert_type(async_raw.mailbox, resources.AsyncMailboxResourceWithRawResponse)
    assert_type(async_raw.drafts, resources.AsyncDraftsResourceWithRawResponse)
    assert_type(async_raw.outbox, resources.AsyncOutboxResourceWithRawResponse)
    assert_type(async_raw.validate, resources.AsyncValidateResourceWithRawResponse)
    assert_type(async_raw.lookup, resources.AsyncLookupResourceWithRawResponse)
    assert_type(async_raw.me, resources.AsyncMeResourceWithRawResponse)
    assert_type(async_raw.stats, resources.AsyncStatsResourceWithRawResponse)
    assert_type(async_raw.conversion, resources.AsyncConversionResourceWithRawResponse)
    assert_type(async_raw.webhooks, resources.AsyncWebhooksResourceWithRawResponse)

    async_streaming = async_client.with_streaming_response
    assert_type(async_streaming.documents, resources.AsyncDocumentsResourceWithStreamingResponse)
    assert_type(async_streaming.inbox, resources.AsyncInboxResourceWithStreamingResponse)
    assert_type(async_streaming.mailbox, resources.AsyncMailboxResourceWithStreamingResponse)
    assert_type(async_streaming.drafts, resources.AsyncDraftsResourceWithStreamingResponse)
    assert_type(async_streaming.outbox, resources.AsyncOutboxResourceWithStreamingResponse)
    assert_type(async_streaming.validate, resources.AsyncValidateResourceWithStreamingResponse)
    assert_type(async_streaming.lookup, resources.AsyncLookupResourceWithStreamingResponse)
    assert_type(async_streaming.me, resources.AsyncMeResourceWithStreamingResponse)
    assert_type(async_streaming.stats, resources.AsyncStatsResourceWithStreamingResponse)
    assert_type(async_streaming.conversion, resources.AsyncConversionResourceWithStreamingResponse)
    assert_type(async_streaming.webhooks, resources.AsyncWebhooksResourceWithStreamingResponse)
