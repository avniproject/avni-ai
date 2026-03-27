import pytest
from src.main import create_server


class TestServerInitialization:
    @pytest.mark.run(order=1)
    @pytest.mark.asyncio
    async def test_create_server_returns_fastmcp_instance(self):
        server = await create_server()
        assert server is not None
        assert hasattr(server, "run")
