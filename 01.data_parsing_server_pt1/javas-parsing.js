const fs = require('fs'); // File System module
const csv = require('csv-parser'); // CSV parser

// Paths to your files
const jsonFile = '/Users/kaitsvetkov/System_Integration/System_Integration/02.Text-based_Data_Formats/me.json';
const csvFile = '/Users/kaitsvetkov/System_Integration/System_Integration/02.Text-based_Data_Formats/me.csv';
const txtFile = '/Users/kaitsvetkov/System_Integration/System_Integration/02.Text-based_Data_Formats/me.txt';

// Function to read JSON
const readJSON = (filepath) => {
    return JSON.parse(fs.readFileSync(filepath, 'utf8'));
};

// Function to read CSV (async because CSV parsing is event-based)
const readCSV = async (filepath) => {
    return new Promise((resolve, reject) => {
        const results = [];
        fs.createReadStream(filepath)
            .pipe(csv())
            .on('data', (data) => results.push(data))
            .on('end', () => resolve(results))
            .on('error', reject);
    });
};

// Function to read TXT
const readTXT = (filepath) => {
    return fs.readFileSync(filepath, 'utf8').replace(/\n/g, ' '); // Convert newlines to spaces
};

// Read all files and print each content on a new line
(async () => {
    const jsonContent = readJSON(jsonFile);
    const csvContent = await readCSV(csvFile);
    const txtContent = readTXT(txtFile);

    console.log(`JSON: ${JSON.stringify(jsonContent)}`);
    console.log(`CSV: ${JSON.stringify(csvContent)}`);
    console.log(`TXT: "${txtContent}"`);
})();