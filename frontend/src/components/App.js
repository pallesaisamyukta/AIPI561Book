import React, { useState, useEffect } from 'react';
import Header from './Header';
import BookSearch from './BookSearch';
import LoadingIndicator from './LoadingIndicator';
import './App.css';

function App() {
  const [loading, setLoading] = useState(false);
  const [summaries, setSummaries] = useState({}); // State to store summaries

  const handleBookSelection = async (book) => {
    const pdfPath = `/home/ritik/Samyukta/local-project/src/books/${book.name}.pdf`;
    console.log('PDF Path:', pdfPath);  // Print the pdf_path
    setLoading(true);
    
    try {
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pdf_path: pdfPath })
      };

      console.log("Inside try");
      // Call your backend API to get summaries of preceding books
      const response = await fetch('http://localhost:5050/summarize', requestOptions);
      console.log("Called backend API");

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Received summaries:', data.summary);  // Print the summaries
      
      // Update state with summaries for the current book
      setSummaries(prevSummaries => ({
        ...prevSummaries,
        [book.id]: data.summary
      }));

    } catch (error) {
      console.error('Error fetching summary:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <Header />
      <BookSearch onBookSelect={handleBookSelection} summaries={summaries} />
      {loading && <LoadingIndicator />}
      {/* Display other components using summaries and history as needed */}
    </div>
  );
}

export default App;
