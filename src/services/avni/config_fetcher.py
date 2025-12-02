import logging
from typing import Dict, Any

from ...clients.avni_client import AvniClient

logger = logging.getLogger(__name__)


class ConfigFetcher:
    def __init__(self):
        self.avni_client = AvniClient()

    async def fetch_complete_config(self, auth_token: str) -> Dict[str, Any]:
        try:
            complete_config = {}

            endpoints = {
                "addressLevelTypes": "/addressLevelType",
                "locations": "/locations",
                "catchments": "/catchment",
                "subjectTypes": "/web/subjectType",
                "programs": "/web/program",
                "encounterTypes": "/web/encounterType",
            }

            for config_key, endpoint in endpoints.items():
                logger.info(f"Fetching {config_key} from {endpoint}")
                result = await self.avni_client.call_avni_server(
                    "GET", endpoint, auth_token
                )

                if result.success:
                    complete_config[config_key] = result.data or []
                    logger.info(
                        f"Successfully fetched {len(complete_config[config_key])} {config_key}"
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
