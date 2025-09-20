import jwt from 'jsonwebtoken';

async function handleRequest(req, res) {
    const token = req.headers['access_token']?.split(' ')[1]; // extract the token
    
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