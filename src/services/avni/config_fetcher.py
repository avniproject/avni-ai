import logging
import os
from typing import Dict, Any, List, Optional

from ...clients.avni_client import AvniClient

logger = logging.getLogger(__name__)

_DEFAULT_MAX_CONFIG_ITEMS = int(os.getenv("MAX_CONFIG_ITEMS", "100"))

_ALL_ENDPOINTS: Dict[str, str] = {
    "addressLevelTypes": "/addressLevelType",
    "locations": "/locations",
    "catchments": "/catchment",
    "subjectTypes": "/web/subjectType",
    "programs": "/web/program",
    "encounterTypes": "/web/encounterType",
}


class ConfigFetcher:
    def __init__(self):
        self.avni_client = AvniClient()

    async def fetch_complete_config(
        self,
        auth_token: str,
        sections: Optional[List[str]] = None,
        max_items: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Fetch config sections from Avni.

        Args:
            sections: If provided, only fetch these section keys (subset of
                      addressLevelTypes, locations, catchments, subjectTypes,
                      programs, encounterTypes). Default: all sections.
            max_items: Cap each array to this many items. If an array is
                       clipped, a ``_truncated`` sibling key is added with
                       ``{truncated: true, total: N}``.  Default env var
                       MAX_CONFIG_ITEMS (100).
        """
        cap = max_items if max_items is not None else _DEFAULT_MAX_CONFIG_ITEMS

        # Validate / filter requested sections
        if sections:
            unknown = [s for s in sections if s not in _ALL_ENDPOINTS]
            if unknown:
                return {
                    "error": f"Unknown sections: {unknown}. Valid: {list(_ALL_ENDPOINTS)}"
                }
            endpoints = {k: v for k, v in _ALL_ENDPOINTS.items() if k in sections}
        else:
            endpoints = _ALL_ENDPOINTS

        try:
            complete_config: Dict[str, Any] = {}

            for config_key, endpoint in endpoints.items():
                logger.info(f"Fetching {config_key} from {endpoint}")
                result = await self.avni_client.call_avni_server(
                    "GET", endpoint, auth_token
                )

                if result.success:
                    data = result.data or []
                    total = len(data)
                    if cap and total > cap:
                        data = data[:cap]
                        complete_config[f"{config_key}_truncated"] = {
                            "truncated": True,
                            "total": total,
                            "returned": cap,
                        }
                    complete_config[config_key] = data
                    logger.info(
                        "Fetched %d/%d %s (cap=%s)", len(data), total, config_key, cap
                    )
                else:
                    logger.error(f"Failed to fetch {config_key}: {result.error}")
                    return {"error": f"Failed to fetch {config_key}: {result.error}"}

            logger.info("Successfully fetched complete configuration")
            return complete_config

        except Exception as e:
            error_msg = f"Failed to fetch complete configuration: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
