import React from 'react';

function History({ history }) {
  return (
    <div className="history">
      <h2>History</h2>
      <ul>
        {history.map((item, index) => (
          <li key={index}>
            <strong>Book:</strong> {item.book.title}
            <br />
            <strong>Summaries:</strong> {item.summaries.map((summary, i) => (
              <p key={i}>{summary}</p>
            ))}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default History;
