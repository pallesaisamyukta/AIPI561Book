import React from 'react';

function SummaryDisplay({ summaries }) {
  return (
    <div className="summary-display">
      <h2>Things you need to know before reading this book</h2>
      {summaries.map((summary, index) => (
        <div key={index}>
          <h3>Book {index + 1}</h3>
          <p>{summary}</p>
          <button onClick={() => navigator.clipboard.writeText(summary)}>Copy</button>
          <button
            onClick={() => {
              const element = document.createElement('a');
              const file = new Blob([summary], { type: 'text/plain' });
              element.href = URL.createObjectURL(file);
              element.download = `summary_book_${index + 1}.txt`;
              document.body.appendChild(element); // Required for this to work in FireFox
              element.click();
            }}
          >
            Download
          </button>
        </div>
      ))}
    </div>
  );
}

export default SummaryDisplay;
