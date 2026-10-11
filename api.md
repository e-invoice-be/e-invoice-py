# Documents

Types:

```python
from e_invoice_api.types import (
    Allowance,
    Charge,
    CurrencyCode,
    DocumentAttachmentCreate,
    DocumentCreate,
    DocumentDirection,
    DocumentResponse,
    DocumentTimeline,
    DocumentType,
    PaymentDetailCreate,
    UnitOfMeasureCode,
    DocumentDeleteResponse,
    DocumentCreateFromPdfResponse,
)
```

Methods:

- <code title="post /api/documents/">client.documents.<a href="./src/e_invoice_api/resources/documents/documents.py">create</a>(\*\*<a href="src/e_invoice_api/types/document_create_params.py">params</a>) -> <a href="./src/e_invoice_api/types/document_response.py">DocumentResponse</a></code>
- <code title="get /api/documents/{document_id}">client.documents.<a href="./src/e_invoice_api/resources/documents/documents.py">retrieve</a>(document_id) -> <a href="./src/e_invoice_api/types/document_response.py">DocumentResponse</a></code>
- <code title="delete /api/documents/{document_id}">client.documents.<a href="./src/e_invoice_api/resources/documents/documents.py">delete</a>(document_id) -> <a href="./src/e_invoice_api/types/document_delete_response.py">DocumentDeleteResponse</a></code>
- <code title="post /api/documents/pdf">client.documents.<a href="./src/e_invoice_api/resources/documents/documents.py">create_from_pdf</a>(\*\*<a href="src/e_invoice_api/types/document_create_from_pdf_params.py">params</a>) -> <a href="./src/e_invoice_api/types/document_create_from_pdf_response.py">DocumentCreateFromPdfResponse</a></code>
- <code title="get /api/documents/{document_id}/timeline">client.documents.<a href="./src/e_invoice_api/resources/documents/documents.py">retrieve_timeline</a>(document_id) -> <a href="./src/e_invoice_api/types/document_timeline.py">DocumentTimeline</a></code>
- <code title="post /api/documents/{document_id}/send">client.documents.<a href="./src/e_invoice_api/resources/documents/documents.py">send</a>(document_id, \*\*<a href="src/e_invoice_api/types/document_send_params.py">params</a>) -> <a href="./src/e_invoice_api/types/document_response.py">DocumentResponse</a></code>
- <code title="post /api/documents/{document_id}/validate">client.documents.<a href="./src/e_invoice_api/resources/documents/documents.py">validate</a>(document_id) -> <a href="./src/e_invoice_api/types/ubl_document_validation.py">UblDocumentValidation</a></code>

## Attachments

Types:

```python
from e_invoice_api.types.documents import (
    DocumentAttachment,
    AttachmentListResponse,
    AttachmentDeleteResponse,
)
```

Methods:

- <code title="get /api/documents/{document_id}/attachments/{attachment_id}">client.documents.attachments.<a href="./src/e_invoice_api/resources/documents/attachments.py">retrieve</a>(attachment_id, \*, document_id) -> <a href="./src/e_invoice_api/types/documents/document_attachment.py">DocumentAttachment</a></code>
- <code title="get /api/documents/{document_id}/attachments">client.documents.attachments.<a href="./src/e_invoice_api/resources/documents/attachments.py">list</a>(document_id) -> <a href="./src/e_invoice_api/types/documents/attachment_list_response.py">AttachmentListResponse</a></code>
- <code title="delete /api/documents/{document_id}/attachments/{attachment_id}">client.documents.attachments.<a href="./src/e_invoice_api/resources/documents/attachments.py">delete</a>(attachment_id, \*, document_id) -> <a href="./src/e_invoice_api/types/documents/attachment_delete_response.py">AttachmentDeleteResponse</a></code>
- <code title="post /api/documents/{document_id}/attachments">client.documents.attachments.<a href="./src/e_invoice_api/resources/documents/attachments.py">add</a>(document_id, \*\*<a href="src/e_invoice_api/types/documents/attachment_add_params.py">params</a>) -> <a href="./src/e_invoice_api/types/documents/document_attachment.py">DocumentAttachment</a></code>

## Ubl

Types:

```python
from e_invoice_api.types.documents import UblGetResponse
```

Methods:

- <code title="post /api/documents/ubl">client.documents.ubl.<a href="./src/e_invoice_api/resources/documents/ubl.py">create_from_ubl</a>(\*\*<a href="src/e_invoice_api/types/documents/ubl_create_from_ubl_params.py">params</a>) -> <a href="./src/e_invoice_api/types/document_response.py">DocumentResponse</a></code>
- <code title="get /api/documents/{document_id}/ubl">client.documents.ubl.<a href="./src/e_invoice_api/resources/documents/ubl.py">get</a>(document_id) -> <a href="./src/e_invoice_api/types/documents/ubl_get_response.py">UblGetResponse</a></code>

# Inbox

Types:

```python
from e_invoice_api.types import DocumentState, PaginatedDocumentResponse
```

Methods:

- <code title="get /api/inbox/">client.inbox.<a href="./src/e_invoice_api/resources/inbox.py">list</a>(\*\*<a href="src/e_invoice_api/types/inbox_list_params.py">params</a>) -> <a href="./src/e_invoice_api/types/document_response.py">SyncDocumentsNumberPage[DocumentResponse]</a></code>
- <code title="get /api/inbox/credit-notes">client.inbox.<a href="./src/e_invoice_api/resources/inbox.py">list_credit_notes</a>(\*\*<a href="src/e_invoice_api/types/inbox_list_credit_notes_params.py">params</a>) -> <a href="./src/e_invoice_api/types/document_response.py">SyncDocumentsNumberPage[DocumentResponse]</a></code>
- <code title="get /api/inbox/invoices">client.inbox.<a href="./src/e_invoice_api/resources/inbox.py">list_invoices</a>(\*\*<a href="src/e_invoice_api/types/inbox_list_invoices_params.py">params</a>) -> <a href="./src/e_invoice_api/types/document_response.py">SyncDocumentsNumberPage[DocumentResponse]</a></code>

# Mailbox

Types:

```python
from e_invoice_api.types import InboundEmail
```

Methods:

- <code title="get /api/mailbox/{inbound_email_id}">client.mailbox.<a href="./src/e_invoice_api/resources/mailbox.py">retrieve</a>(inbound_email_id) -> <a href="./src/e_invoice_api/types/inbound_email.py">InboundEmail</a></code>
- <code title="get /api/mailbox/">client.mailbox.<a href="./src/e_invoice_api/resources/mailbox.py">list</a>(\*\*<a href="src/e_invoice_api/types/mailbox_list_params.py">params</a>) -> <a href="./src/e_invoice_api/types/inbound_email.py">SyncDocumentsNumberPage[InboundEmail]</a></code>
- <code title="get /api/mailbox/{inbound_email_id}/attachments/{filename}">client.mailbox.<a href="./src/e_invoice_api/resources/mailbox.py">download_attachment</a>(filename, \*, inbound_email_id) -> BinaryAPIResponse</code>
- <code title="post /api/mailbox/{inbound_email_id}/reprocess">client.mailbox.<a href="./src/e_invoice_api/resources/mailbox.py">reprocess</a>(inbound_email_id) -> <a href="./src/e_invoice_api/types/inbound_email.py">InboundEmail</a></code>

# Drafts

Methods:

- <code title="get /api/drafts/">client.drafts.<a href="./src/e_invoice_api/resources/drafts.py">list</a>(\*\*<a href="src/e_invoice_api/types/draft_list_params.py">params</a>) -> <a href="./src/e_invoice_api/types/document_response.py">SyncDocumentsNumberPage[DocumentResponse]</a></code>

# Outbox

Methods:

- <code title="get /api/outbox/drafts">client.outbox.<a href="./src/e_invoice_api/resources/outbox.py">list_draft_documents</a>(\*\*<a href="src/e_invoice_api/types/outbox_list_draft_documents_params.py">params</a>) -> <a href="./src/e_invoice_api/types/document_response.py">SyncDocumentsNumberPage[DocumentResponse]</a></code>
- <code title="get /api/outbox/">client.outbox.<a href="./src/e_invoice_api/resources/outbox.py">list_received_documents</a>(\*\*<a href="src/e_invoice_api/types/outbox_list_received_documents_params.py">params</a>) -> <a href="./src/e_invoice_api/types/document_response.py">SyncDocumentsNumberPage[DocumentResponse]</a></code>

# Validate

Types:

```python
from e_invoice_api.types import UblDocumentValidation, ValidateValidatePeppolIDResponse
```

Methods:

- <code title="post /api/validate/json">client.validate.<a href="./src/e_invoice_api/resources/validate.py">validate_json</a>(\*\*<a href="src/e_invoice_api/types/validate_validate_json_params.py">params</a>) -> <a href="./src/e_invoice_api/types/ubl_document_validation.py">UblDocumentValidation</a></code>
- <code title="get /api/validate/peppol-id">client.validate.<a href="./src/e_invoice_api/resources/validate.py">validate_peppol_id</a>(\*\*<a href="src/e_invoice_api/types/validate_validate_peppol_id_params.py">params</a>) -> <a href="./src/e_invoice_api/types/validate_validate_peppol_id_response.py">ValidateValidatePeppolIDResponse</a></code>
- <code title="post /api/validate/ubl">client.validate.<a href="./src/e_invoice_api/resources/validate.py">validate_ubl</a>(\*\*<a href="src/e_invoice_api/types/validate_validate_ubl_params.py">params</a>) -> <a href="./src/e_invoice_api/types/ubl_document_validation.py">UblDocumentValidation</a></code>

# Lookup

Types:

```python
from e_invoice_api.types import (
    Certificate,
    LookupRetrieveResponse,
    LookupRetrieveParticipantsResponse,
)
```

Methods:

- <code title="get /api/lookup">client.lookup.<a href="./src/e_invoice_api/resources/lookup.py">retrieve</a>(\*\*<a href="src/e_invoice_api/types/lookup_retrieve_params.py">params</a>) -> <a href="./src/e_invoice_api/types/lookup_retrieve_response.py">LookupRetrieveResponse</a></code>
- <code title="get /api/lookup/participants">client.lookup.<a href="./src/e_invoice_api/resources/lookup.py">retrieve_participants</a>(\*\*<a href="src/e_invoice_api/types/lookup_retrieve_participants_params.py">params</a>) -> <a href="./src/e_invoice_api/types/lookup_retrieve_participants_response.py">LookupRetrieveParticipantsResponse</a></code>

# Me

Types:

```python
from e_invoice_api.types import MeRetrieveResponse
```

Methods:

- <code title="get /api/me/">client.me.<a href="./src/e_invoice_api/resources/me.py">retrieve</a>() -> <a href="./src/e_invoice_api/types/me_retrieve_response.py">MeRetrieveResponse</a></code>

# Stats

Types:

```python
from e_invoice_api.types import StatsRetrieveResponse
```

Methods:

- <code title="get /api/stats">client.stats.<a href="./src/e_invoice_api/resources/stats.py">retrieve</a>(\*\*<a href="src/e_invoice_api/types/stats_retrieve_params.py">params</a>) -> <a href="./src/e_invoice_api/types/stats_retrieve_response.py">StatsRetrieveResponse</a></code>

# Conversion

Types:

```python
from e_invoice_api.types import ConversionPdfTask
```

Methods:

- <code title="post /api/conversion/pdf">client.conversion.<a href="./src/e_invoice_api/resources/conversion.py">create_pdf</a>(\*\*<a href="src/e_invoice_api/types/conversion_create_pdf_params.py">params</a>) -> <a href="./src/e_invoice_api/types/conversion_pdf_task.py">ConversionPdfTask</a></code>
- <code title="get /api/conversion/pdf/{task_id}">client.conversion.<a href="./src/e_invoice_api/resources/conversion.py">retrieve_pdf</a>(task_id) -> <a href="./src/e_invoice_api/types/conversion_pdf_task.py">ConversionPdfTask</a></code>
- <code title="get /api/conversion/pdf/{task_id}/result">client.conversion.<a href="./src/e_invoice_api/resources/conversion.py">retrieve_pdf_result</a>(task_id) -> <a href="./src/e_invoice_api/types/document_create_from_pdf_response.py">DocumentCreateFromPdfResponse</a></code>

# Webhooks

Types:

```python
from e_invoice_api.types import (
    WebhookResponse,
    WebhookListResponse,
    WebhookDeleteResponse,
    WebhookRetrieveHistoryResponse,
    WebhookTestResponse,
)
```

Methods:

- <code title="post /api/webhooks/">client.webhooks.<a href="./src/e_invoice_api/resources/webhooks.py">create</a>(\*\*<a href="src/e_invoice_api/types/webhook_create_params.py">params</a>) -> <a href="./src/e_invoice_api/types/webhook_response.py">WebhookResponse</a></code>
- <code title="get /api/webhooks/{webhook_id}">client.webhooks.<a href="./src/e_invoice_api/resources/webhooks.py">retrieve</a>(webhook_id) -> <a href="./src/e_invoice_api/types/webhook_response.py">WebhookResponse</a></code>
- <code title="put /api/webhooks/{webhook_id}">client.webhooks.<a href="./src/e_invoice_api/resources/webhooks.py">update</a>(webhook_id, \*\*<a href="src/e_invoice_api/types/webhook_update_params.py">params</a>) -> <a href="./src/e_invoice_api/types/webhook_response.py">WebhookResponse</a></code>
- <code title="get /api/webhooks/">client.webhooks.<a href="./src/e_invoice_api/resources/webhooks.py">list</a>() -> <a href="./src/e_invoice_api/types/webhook_list_response.py">WebhookListResponse</a></code>
- <code title="delete /api/webhooks/{webhook_id}">client.webhooks.<a href="./src/e_invoice_api/resources/webhooks.py">delete</a>(webhook_id) -> <a href="./src/e_invoice_api/types/webhook_delete_response.py">WebhookDeleteResponse</a></code>
- <code title="get /api/webhooks/{webhook_id}/history">client.webhooks.<a href="./src/e_invoice_api/resources/webhooks.py">retrieve_history</a>(webhook_id) -> <a href="./src/e_invoice_api/types/webhook_retrieve_history_response.py">WebhookRetrieveHistoryResponse</a></code>
- <code title="post /api/webhooks/{webhook_id}/test">client.webhooks.<a href="./src/e_invoice_api/resources/webhooks.py">test</a>(webhook_id, \*\*<a href="src/e_invoice_api/types/webhook_test_params.py">params</a>) -> <a href="./src/e_invoice_api/types/webhook_test_response.py">WebhookTestResponse</a></code>
