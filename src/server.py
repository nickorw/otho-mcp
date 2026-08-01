from fastmcp import FastMCP

from src.core.config import settings

mcp = FastMCP(
    "otho-mcp",
    instructions="OWL Ontology Validation & Analysis Server",
)

from src.tools.validators import validators_mcp  # noqa: E402
from src.tools.composite import composite_mcp  # noqa: E402
from src.tools.utilities import utilities_mcp  # noqa: E402

mcp.mount(validators_mcp)
mcp.mount(composite_mcp)
mcp.mount(utilities_mcp)


@mcp.custom_route("/health", methods=["GET"])
async def health(request):
    from starlette.responses import JSONResponse
    return JSONResponse({"status": "ok"})


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host=settings.server_host, port=settings.server_port)
