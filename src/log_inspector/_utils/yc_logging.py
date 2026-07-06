"""Yandex Cloud Logging REST API client."""

import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

logger = logging.getLogger(__name__)

# Max page size allowed by Yandex Cloud Logging API
MAX_PAGE_SIZE = 1000

# Yandex Cloud Logging API base URL
API_BASE = 'https://logging.api.cloud.yandex.net/logging/v1'


class YcLoggingError(Exception):
    """Base exception for YC Logging API errors."""


class AuthError(YcLoggingError):
    """Authentication-related errors."""


class IamTokenAuth:
    """Provides an IAM token from the YC_IAM_TOKEN environment variable.

    Caches the token and handles refresh on expiry.
    """

    def __init__(self) -> None:
        self._token: str | None = None
        self._expiry: datetime | None = None

    def get_token(self) -> str:
        """Return a valid IAM token, reading from env var if needed."""
        if self._token and self._expiry and datetime.now(timezone.utc) < self._expiry:
            return self._token

        token = os.environ.get('YC_IAM_TOKEN')
        if not token:
            raise AuthError(
                'YC_IAM_TOKEN environment variable is not set. ' 'Obtain a token via YC CLI: yc iam create-token'
            )

        self._token = token
        # IAM tokens are valid for 12h, refresh after 11h
        self._expiry = datetime.now(timezone.utc) + timedelta(hours=11)
        return self._token

    def invalidate(self) -> None:
        """Force token refresh on next call."""
        self._token = None
        self._expiry = None


class YcLoggingClient:
    """Client for Yandex Cloud Logging REST API.

    Uses IamTokenAuth for authentication via the YC_IAM_TOKEN env var.
    """

    def __init__(self, folder_id: str | None = None, auth: IamTokenAuth | None = None) -> None:
        self._folder_id = folder_id or os.environ.get('YC_FOLDER_ID', '')
        self._auth = auth or IamTokenAuth()
        self._http = httpx.Client(timeout=30.0)

    # ── Internal HTTP ───────────────────────────────────────────────

    def _request(self, method: str, path: str, **kwargs: Any) -> dict:
        """Make an authenticated request to the YC Logging API."""
        token = self._auth.get_token()
        url = f'{API_BASE}/{path.lstrip("/")}'

        headers = kwargs.pop('headers', {})
        headers['Authorization'] = f'Bearer {token}'
        headers['Content-Type'] = 'application/json'

        resp = self._http.request(method, url, headers=headers, **kwargs)

        if resp.status_code == 401:
            # Token expired, force refresh and retry once
            self._auth.invalidate()
            token = self._auth.get_token()
            headers['Authorization'] = f'Bearer {token}'
            resp = self._http.request(method, url, headers=headers, **kwargs)

        resp.raise_for_status()
        return resp.json()

    # ── API Methods ─────────────────────────────────────────────────

    def list_log_groups(self) -> list[dict]:
        """List all available log groups in the folder."""
        path = f'logGroups?folderId={self._folder_id}'
        data = self._request('GET', path)
        return data.get('groups', [])

    def read_logs(
        self,
        group_id: str,
        *,
        level: str = 'ERROR',
        since: timedelta | None = None,
        until: datetime | None = None,
        filter_str: str | None = None,
        page_size: int = 100,
        page_token: str | None = None,
    ) -> dict:
        """Read log entries from a log group.

        Args:
            group_id: Log group ID.
            level: Minimum log level (ERROR, WARN, INFO, DEBUG, TRACE).
            since: Time range start (relative to now).
            until: Time range end (absolute).
            filter_str: Additional YC Logging filter string.
            page_size: Results per page (max 1000).
            page_token: Pagination token for next page.

        Returns:
            API response dict with 'entries' and optional 'nextPageToken'.
        """
        until_time = until or datetime.now(timezone.utc)
        since_time = (until_time - since) if since else (until_time - timedelta(days=1))

        filters = [f'level={level}']
        if filter_str:
            filters.append(f'({filter_str})')
        full_filter = ' AND '.join(filters)

        body: dict[str, Any] = {
            'pageSize': min(page_size, MAX_PAGE_SIZE),
            'filter': full_filter,
            'sinceTime': since_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'untilTime': until_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        }
        if page_token:
            body['pageToken'] = page_token

        return self._request('POST', f'logGroups/{group_id}:read', json=body)

    def read_all_logs(
        self,
        group_id: str,
        *,
        level: str = 'ERROR',
        since: timedelta | None = None,
        until: datetime | None = None,
        filter_str: str | None = None,
        max_entries: int = 5000,
    ) -> list[dict]:
        """Read all log entries across paginated responses.

        Args:
            Same as read_logs().
            max_entries: Maximum entries to collect across all pages.

        Returns:
            Combined list of log entries.
        """
        entries: list[dict] = []
        page_token: str | None = None

        while len(entries) < max_entries:
            remaining = max_entries - len(entries)
            page_size = min(MAX_PAGE_SIZE, remaining)

            data = self.read_logs(
                group_id,
                level=level,
                since=since,
                until=until,
                filter_str=filter_str,
                page_size=page_size,
                page_token=page_token,
            )

            page_entries = data.get('entries', [])
            entries.extend(page_entries)

            next_token = data.get('nextPageToken')
            if not next_token or not page_entries:
                break
            page_token = next_token

        return entries

    def get_logs_by_request_id(
        self,
        group_id: str,
        request_id: str,
        *,
        since: timedelta | None = None,
        max_entries: int = 500,
    ) -> list[dict]:
        """Get all log entries for a specific request_id."""
        return self.read_all_logs(
            group_id,
            level='TRACE',
            since=since or timedelta(days=1),
            filter_str=f'json_payload.request_id="{request_id}"',
            max_entries=max_entries,
        )

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http.close()
