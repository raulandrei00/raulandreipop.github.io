const { google } = require('googleapis');

const sheets = google.sheets('v4');

// Replace with your Google API credentials and spreadsheet details
const SPREADSHEET_ID = '1e1S-HuM-6Dy0nxopEc7be8SIsMK-GedcoqHmfu1pyLQ';
const RANGE = 'Form responses 1!C2:E40'; // Adjust the range to match your sheet structure

// Authenticate using a service account or OAuth2
async function authenticate() {
    const auth = new google.auth.GoogleAuth({
        keyFile: 'path/to/your/service-account-key.json', // Replace with your service account key file
        scopes: ['https://www.googleapis.com/auth/spreadsheets.readonly'],
    });
    return auth.getClient();
}

// Fetch data from the spreadsheet
async function fetchTeams() {
    const authClient = await authenticate();
    const response = await sheets.spreadsheets.values.get({
        auth: authClient,
        spreadsheetId: SPREADSHEET_ID,
        range: RANGE,
    });

    const rows = response.data.values;
    if (!rows || rows.length === 0) {
        console.log('No data found.');
        return [];
    }

    // Extract Team Name, Member 1 Name, and Member 2 Name
    const teams = rows.slice(1).map(row => ({
        teamName: row[0],
        member1: row[1],
        member2: row[2],
    }));

    console.log(teams);
    return teams;
}

// Run the script
fetchTeams().catch(console.error);