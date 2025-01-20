function encryptData(data) {
    // Simple base64 encoding for demonstration (not secure)
    return btoa(data);
}

function decryptData(data) {
    return atob(data);
}

// Example usage
const sensitiveData = "User 's personal information";
const encryptedData = encryptData(sensitiveData);
console.log("Encrypted Data:", encryptedData);
console.log("Decrypted Data:", decryptData(encryptedData));
