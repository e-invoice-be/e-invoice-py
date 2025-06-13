# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Generic, TypeVar, Optional
from typing_extensions import override

from ._base_client import BasePage, PageInfo, BaseSyncPage, BaseAsyncPage

__all__ = ["SyncDocumentsNumberPage", "AsyncDocumentsNumberPage"]

_T = TypeVar("_T")


class SyncDocumentsNumberPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    items: List[_T]
    page: Optional[int] = None
    page_size: Optional[int] = None
    total: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        current_page = self.page
        if current_page is None:
            current_page = 1

        total_pages = self.total
        if total_pages is not None and current_page >= total_pages:
            return None

        return PageInfo(params={"page": current_page + 1})


class AsyncDocumentsNumberPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    items: List[_T]
    page: Optional[int] = None
    page_size: Optional[int] = None
    total: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        current_page = self.page
        if current_page is None:
            current_page = 1

        total_pages = self.total
        if total_pages is not None and current_page >= total_pages:
            return None

        return PageInfo(params={"page": current_page + 1})
