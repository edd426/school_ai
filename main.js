// Function to fetch CSV data from the server
async function fetchCSV() {
    try {
      const response = await fetch('http://localhost:5000/get-csv'); // Make sure the URL matches your server's URL and route
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      // Read the response as text
      const csvText = await response.text();
  
      // Log the raw CSV data
      console.log('CSV Data:', csvText);
  
      // Parse the CSV data (simple parsing example)
      const parsedData = parseCSV(csvText);
      console.log('Parsed Data:', parsedData);
  
    } catch (error) {
      console.error('Error fetching CSV:', error);
    }
  }
  // Helper function to parse CSV text into a JavaScript array
function parseCSV(csvText) {
    const rows = csvText.split('\n'); // Split CSV text into rows
    return rows.map(row => row.split(',')); // Split each row into columns
}