# MCPAuth

This repository contains authentication and client utilities for MCP (Multi-Cloud Platform) integration.

## Files

### client.py

A Python module for generating JWTs and creating an authenticated MCP client.

**Features:**
- Generates JWT tokens using RS256 algorithm.
- Uses environment variable `PRIVATE_KEY` for signing.
- Provides an async context manager to create authenticated HTTP headers.
- Example usage included for quick setup.

**Usage Example:**
```python
token_data = {
    "access_token": generate_jwt(),
    "instance_url": "https://example-mcp-server.com",
    "token_type": "Bearer"
}
mcp_client = create_authenticated_mcp_client(token_data)
```

### server.js

A Node.js server handler for validating JWTs in incoming requests.

**Features:**
- Extracts and verifies JWT from `access_token` header.
- Uses environment variable `PUBLIC_KEY` for verification.
- Responds with appropriate status codes for missing or invalid tokens.
- Prints a message to console on successful decoding.

**Usage Example:**
```javascript
import jwt from 'jsonwebtoken';

async function handleRequest(req, res) {
    const token = req.headers['access_token']?.split(' ')[1];
    if (!token) {
        res.status(400).send('Missing authentication token');
        return;
    }
    try {
        const public_key =  process.env.PUBLIC_KEY;
        const decoded_token = jwt.verify(token, public_key, { algorithm: ['RS256'] });
        console.log("Token decoded successfully")
    }
    catch (err){
        res.status(400).send(`Token invalid or we get connection error: ${err}`);
    }
}
```

## Environment Variables

- `PRIVATE_KEY`: Used in `client.py` for JWT signing.
- `PUBLIC_KEY`: Used in `server.js` for JWT verification.

## License

MIT (or your chosen license)