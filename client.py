# client.py
import os
import time
import uuid
import jwt  # PyJWT
from contextlib import asynccontextmanager
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient

def generate_jwt(subject: str, audience: str, issuer: str, lifetime_seconds: int = 300) -> str:
    """
    Generate an RS256-signed JWT using a PEM private key from env.
    """
    private_key_pem = os.environ.get("PRIVATE_KEY_PEM")
    if not private_key_pem:
        raise RuntimeError("PRIVATE_KEY_PEM not set in environment")

    now = int(time.time())
    payload = {
        "sub": subject,
        "iss": issuer,
        "aud": audience,
        "iat": now,
        "exp": now + lifetime_seconds,
        "jti": str(uuid.uuid4())
    }
    token = jwt.encode(payload, private_key_pem, algorithm="RS256")
    # PyJWT might return a str or bytes depending on version; ensure str
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token

@asynccontextmanager
async def _create_transport_with_auth(instance_url: str, token: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "x-instance-url": instance_url,
        "x-token-type": "Bearer"
    }
    async with streamablehttp_client(instance_url, headers=headers) as transport:
        yield transport

def create_authenticated_mcp_client(token: str, instance_url: str) -> MCPClient:
    """
    Return an MCPClient that uses an asynccontextmanager to attach headers.
    MCPClient should accept a callable that yields a transport context manager.
    """
    # Provide a zero-arg callable MCPClient can call when opening connections
    return MCPClient(lambda: _create_transport_with_auth(instance_url, token))

# Example usage
if __name__ == "__main__":
    token = generate_jwt("user@example.com", "https://example-mcp-server.com", "your-client-id")
    client = create_authenticated_mcp_client(token, "https://example-mcp-server.com")
