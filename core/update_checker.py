# -*- coding: utf-8 -*-
"""
Update Checker Module

Provides automatic update checking functionality for the plugin.
Supports checking latest version from remote server and notifying user.
"""

import json
import os
import re
import threading
from typing import Callable
from typing import Optional
from urllib.error import URLError
from urllib.request import Request
from urllib.request import urlopen

from qgis.core import Qgis
from qgis.core import QgsMessageLog

# Default update check URL (GitHub raw content as example)
# Users should replace this with their actual update server URL
DEFAULT_VERSION_URL = "https://raw.githubusercontent.com/autostyle/autostyle/main/version.json"

# Request timeout in seconds
REQUEST_TIMEOUT = 10

# Log tag
LOG_TAG = "AutoStyle"


def parse_version(version_str: str) -> tuple:
    """
    Parse version string to comparable tuple.

    Supports formats like: 1.0.0, 1.2.3, 1.0.0-beta, 1.0.0.1

    :param version_str: Version string
    :return: Tuple of version numbers
    """
    # Remove leading 'v' if present
    version_str = version_str.lstrip('vV')

    # Extract numeric parts
    match = re.match(r'^(\d+(?:\.\d+)*)', version_str)
    if not match:
        return (0,)

    parts = match.group(1).split('.')
    return tuple(int(p) for p in parts)


def compare_versions(version1: str, version2: str) -> int:
    """
    Compare two version strings.

    :param version1: First version string
    :param version2: Second version string
    :return: 1 if version1 > version2, -1 if version1 < version2, 0 if equal
    """
    v1 = parse_version(version1)
    v2 = parse_version(version2)

    # Pad shorter version with zeros
    max_len = max(len(v1), len(v2))
    v1 = v1 + (0,) * (max_len - len(v1))
    v2 = v2 + (0,) * (max_len - len(v2))

    if v1 > v2:
        return 1
    elif v1 < v2:
        return -1
    else:
        return 0


class UpdateInfo:
    """Update information container."""

    def __init__(
        self,
        has_update: bool = False,
        current_version: str = "",
        latest_version: str = "",
        download_url: str = "",
        changelog: str = "",
        release_date: str = "",
        error: Optional[str] = None,
    ):
        """
        Initialize update info.

        :param has_update: Whether there is a new version available
        :param current_version: Current installed version
        :param latest_version: Latest available version
        :param download_url: URL to download the latest version
        :param changelog: Changelog/release notes
        :param release_date: Release date of latest version
        :param error: Error message if check failed
        """
        self.has_update = has_update
        self.current_version = current_version
        self.latest_version = latest_version
        self.download_url = download_url
        self.changelog = changelog
        self.release_date = release_date
        self.error = error


class UpdateChecker:
    """
    Plugin update checker.

    Checks for updates from a remote server and provides update information.
    Supports both synchronous and asynchronous checking.
    """

    def __init__(
        self,
        plugin_dir: str,
        version_url: str = DEFAULT_VERSION_URL,
    ):
        """
        Initialize the update checker.

        :param plugin_dir: Plugin directory path (to read metadata.txt)
        :param version_url: URL to fetch version information JSON
        """
        self.plugin_dir = plugin_dir
        self.version_url = version_url
        self._current_version = None

    def get_current_version(self) -> str:
        """
        Get current plugin version from metadata.txt.

        :return: Current version string
        """
        if self._current_version is not None:
            return self._current_version

        metadata_path = os.path.join(self.plugin_dir, "metadata.txt")
        version = "0.0.0"

        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("version="):
                        version = line.split("=", 1)[1].strip()
                        break
        except Exception as e:
            QgsMessageLog.logMessage(
                f"Failed to read metadata.txt: {e}",
                LOG_TAG,
                Qgis.Warning,
            )

        self._current_version = version
        return version

    def _fetch_remote_version(self) -> dict:
        """
        Fetch version information from remote server.

        :return: Parsed JSON data or empty dict on error
        :raises: URLError, ValueError on failure
        """
        request = Request(
            self.version_url,
            headers={
                "User-Agent": f"AutoStyle/{self.get_current_version()}",
                "Accept": "application/json",
            },
        )

        with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)

    def check_update(self) -> UpdateInfo:
        """
        Check for updates synchronously.

        :return: UpdateInfo object with check results
        """
        current_version = self.get_current_version()

        try:
            remote_data = self._fetch_remote_version()

            latest_version = remote_data.get("version", "")
            if not latest_version:
                return UpdateInfo(
                    has_update=False,
                    current_version=current_version,
                    error="Invalid version data from server",
                )

            has_update = compare_versions(latest_version, current_version) > 0

            return UpdateInfo(
                has_update=has_update,
                current_version=current_version,
                latest_version=latest_version,
                download_url=remote_data.get("download_url", ""),
                changelog=remote_data.get("changelog", ""),
                release_date=remote_data.get("release_date", ""),
            )

        except URLError as e:
            QgsMessageLog.logMessage(
                f"Network error while checking update: {e}",
                LOG_TAG,
                Qgis.Warning,
            )
            return UpdateInfo(
                has_update=False,
                current_version=current_version,
                error=f"Network error: {e.reason}",
            )

        except json.JSONDecodeError as e:
            QgsMessageLog.logMessage(
                f"Invalid JSON response: {e}",
                LOG_TAG,
                Qgis.Warning,
            )
            return UpdateInfo(
                has_update=False,
                current_version=current_version,
                error="Invalid response format",
            )

        except Exception as e:
            QgsMessageLog.logMessage(
                f"Update check failed: {e}",
                LOG_TAG,
                Qgis.Warning,
            )
            return UpdateInfo(
                has_update=False,
                current_version=current_version,
                error=str(e),
            )

    def check_update_async(self, callback: Callable[[UpdateInfo], None]) -> None:
        """
        Check for updates asynchronously.

        The callback will be called from a background thread.
        Use Qt signals/slots to safely update UI from the callback.

        :param callback: Function to call with UpdateInfo when check completes
        """
        def _check_thread():
            result = self.check_update()
            callback(result)

        thread = threading.Thread(target=_check_thread, daemon=True)
        thread.start()
