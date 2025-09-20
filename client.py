import jwt
import os
import httpx
import asyncio

def generate_jwt():
    private_key = os.environ.get("PRIVATE_KEY")
    if not private_key:
        raise ValueError("PRIVATE_KEY environment variable not set")
    payload = {
        "user": "example_user",
        "scope": "mcp_auth"
    }
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token

class MCPClient:
    def __init__(self, token_data):
        self.token_data = token_data
        self.headers = {
            "access_token": f"Bearer {token_data['access_token']}"
        }
        self.base_url = token_data["instance_url"]

    async def __aenter__(self):
        self.client = httpx.AsyncClient(headers=self.headers)
        return self.client

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.aclose()

def create_authenticated_mcp_client(token_data):
    return MCPClient(token_data)

# Example usage:
if __name__ == "__main__":
    token_data = {
        "access_token": generate_jwt(),
        "instance_url": "https://example-mcp-server.com",
        "token_type": "Bearer"
    }
    mcp_client = create_authenticated_mcp_client(token_data)
    async def main():
        async with mcp_client as client:
            resp = await client.get(f"{token_data['instance_url']}/api/test")
            print(resp.json())
    asyncio.run(main())