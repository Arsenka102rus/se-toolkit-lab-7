"""LMS API client for communicating with the backend."""

import httpx
from config import settings


class LMSClient:
    """Client for the LMS backend API.
    
    Uses Bearer token authentication and handles common errors.
    """

    def __init__(self):
        self.base_url = settings.lms_api_base_url
        self.api_key = settings.lms_api_key
        self.timeout = 10.0  # seconds

    def _get_headers(self) -> dict:
        """Return headers with Bearer token authentication."""
        return {"Authorization": f"Bearer {self.api_key}"}

    def get_items(self) -> list[dict] | None:
        """Fetch all items (labs and tasks) from the backend."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/items/",
                    headers=self._get_headers()
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise BackendError(f"HTTP {e.response.status_code}: {e.response.text[:100]}")
        except httpx.ConnectError as e:
            raise BackendError(f"connection refused ({self.base_url}). Check that the services are running.")
        except httpx.TimeoutException:
            raise BackendError(f"timeout connecting to {self.base_url}")
        except Exception as e:
            raise BackendError(f"unexpected error: {str(e)}")

    def get_learners(self) -> list[dict] | None:
        """Fetch all learners from the backend."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/learners/",
                    headers=self._get_headers()
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise BackendError(f"HTTP {e.response.status_code}: {e.response.text[:100]}")
        except httpx.ConnectError as e:
            raise BackendError(f"connection refused ({self.base_url}). Check that the services are running.")
        except httpx.TimeoutException:
            raise BackendError(f"timeout connecting to {self.base_url}")
        except Exception as e:
            raise BackendError(f"unexpected error: {str(e)}")

    def get_scores(self, lab: str) -> list[dict] | None:
        """Fetch score distribution for a lab."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/analytics/scores",
                    headers=self._get_headers(),
                    params={"lab": lab}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise BackendError(f"HTTP {e.response.status_code}: {e.response.text[:100]}")
        except httpx.ConnectError as e:
            raise BackendError(f"connection refused ({self.base_url}). Check that the services are running.")
        except httpx.TimeoutException:
            raise BackendError(f"timeout connecting to {self.base_url}")
        except Exception as e:
            raise BackendError(f"unexpected error: {str(e)}")

    def get_pass_rates(self, lab: str) -> list[dict] | None:
        """Fetch per-task pass rates for a specific lab."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/analytics/pass-rates",
                    headers=self._get_headers(),
                    params={"lab": lab}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 422:
                raise BackendError(f"invalid lab identifier: {lab}")
            raise BackendError(f"HTTP {e.response.status_code}: {e.response.text[:100]}")
        except httpx.ConnectError as e:
            raise BackendError(f"connection refused ({self.base_url}). Check that the services are running.")
        except httpx.TimeoutException:
            raise BackendError(f"timeout connecting to {self.base_url}")
        except Exception as e:
            raise BackendError(f"unexpected error: {str(e)}")

    def get_timeline(self, lab: str) -> list[dict] | None:
        """Fetch submissions timeline for a lab."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/analytics/timeline",
                    headers=self._get_headers(),
                    params={"lab": lab}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise BackendError(f"HTTP {e.response.status_code}: {e.response.text[:100]}")
        except httpx.ConnectError as e:
            raise BackendError(f"connection refused ({self.base_url}). Check that the services are running.")
        except httpx.TimeoutException:
            raise BackendError(f"timeout connecting to {self.base_url}")
        except Exception as e:
            raise BackendError(f"unexpected error: {str(e)}")

    def get_groups(self, lab: str) -> list[dict] | None:
        """Fetch per-group performance for a lab."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/analytics/groups",
                    headers=self._get_headers(),
                    params={"lab": lab}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise BackendError(f"HTTP {e.response.status_code}: {e.response.text[:100]}")
        except httpx.ConnectError as e:
            raise BackendError(f"connection refused ({self.base_url}). Check that the services are running.")
        except httpx.TimeoutException:
            raise BackendError(f"timeout connecting to {self.base_url}")
        except Exception as e:
            raise BackendError(f"unexpected error: {str(e)}")

    def get_top_learners(self, lab: str, limit: int = 5) -> list[dict] | None:
        """Fetch top learners for a lab."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/analytics/top-learners",
                    headers=self._get_headers(),
                    params={"lab": lab, "limit": limit}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise BackendError(f"HTTP {e.response.status_code}: {e.response.text[:100]}")
        except httpx.ConnectError as e:
            raise BackendError(f"connection refused ({self.base_url}). Check that the services are running.")
        except httpx.TimeoutException:
            raise BackendError(f"timeout connecting to {self.base_url}")
        except Exception as e:
            raise BackendError(f"unexpected error: {str(e)}")

    def get_completion_rate(self, lab: str) -> dict | None:
        """Fetch completion rate for a lab."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.base_url}/analytics/completion-rate",
                    headers=self._get_headers(),
                    params={"lab": lab}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise BackendError(f"HTTP {e.response.status_code}: {e.response.text[:100]}")
        except httpx.ConnectError as e:
            raise BackendError(f"connection refused ({self.base_url}). Check that the services are running.")
        except httpx.TimeoutException:
            raise BackendError(f"timeout connecting to {self.base_url}")
        except Exception as e:
            raise BackendError(f"unexpected error: {str(e)}")

    def trigger_sync(self) -> dict | None:
        """Trigger ETL sync."""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    f"{self.base_url}/pipeline/sync",
                    headers=self._get_headers(),
                    json={}
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise BackendError(f"HTTP {e.response.status_code}: {e.response.text[:100]}")
        except httpx.ConnectError as e:
            raise BackendError(f"connection refused ({self.base_url}). Check that the services are running.")
        except httpx.TimeoutException:
            raise BackendError(f"timeout connecting to {self.base_url}")
        except Exception as e:
            raise BackendError(f"unexpected error: {str(e)}")


class BackendError(Exception):
    """Error communicating with the LMS backend."""
    pass


# Global client instance
lms_client = LMSClient()
