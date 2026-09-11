const fs = require('fs')
const path = require('path');

const filePath_API = path.resolve(__dirname, 'json/postman/Faktura.uz_API.json');
const filePath_ENV = path.resolve(__dirname, 'json/postman/Faktura.uz_ENV.json');

console.log(filePath_API);
console.log(filePath_ENV);

fs.readFileSync(filePath_API, 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading API file:', err);
        return;
    }   
    console.log(data);
});

fs.readFileSync(filePath_ENV, 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading ENV file:', err);
        return;
    }
    console.log(data);
});


fs.writeFileSync(filePath_API, JSON.stringify({ message: "This is a test message for API file." }, null, 2), 'utf8', (err) => {