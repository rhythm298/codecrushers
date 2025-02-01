const crypto = require('crypto');
const { promisify } = require('util');
const generateKeyPair = promisify(crypto.generateKeyPair);

class SecurityManager {
    constructor() {
        this.algorithm = 'aes-256-cbc';
        this.iv = crypto.randomBytes(16);
    }

    async generateRSAKeys() {
        return generateKeyPair('rsa', {
            modulusLength: 4096,
            publicKeyEncoding: { type: 'spki', format: 'pem' },
            privateKeyEncoding: { type: 'pkcs8', format: 'pem' }
        });
    }

    encryptData(data, key) {
        const cipher = crypto.createCipheriv(this.algorithm, key, this.iv);
        let encrypted = cipher.update(data, 'utf8', 'hex');
        encrypted += cipher.final('hex');
        return {
            iv: this.iv.toString('hex'),
            encryptedData: encrypted
        };
    }

    decryptData(encrypted, key) {
        const decipher = crypto.createDecipheriv(
            this.algorithm, 
            key, 
            Buffer.from(encrypted.iv, 'hex')
        );
        let decrypted = decipher.update(encrypted.encryptedData, 'hex', 'utf8');
        decrypted += decipher.final('utf8');
        return decrypted;
    }
}

module.exports = SecurityManager;
