import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

const BookSummary = ({ book, onBookSelect }) => {
    const [loading, setLoading] = useState(false);
    const [summary, setSummary] = useState('');

    useEffect(() => {
        const fetchSummary = async () => {
            setLoading(true);
            try {
                const pdfPath = `/home/ritik/Samyukta/local-project/src/books/${book.name}.pdf`;
                const requestOptions = {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ pdf_path: pdfPath })
                };

                const response = await fetch('http://localhost:5050/summarize', requestOptions);

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json();
                setSummary(data.summary);
            } catch (error) {
                console.error('Error fetching summary:', error);
            } finally {
                setLoading(false);
            }
        };

        if (onBookSelect) {
            onBookSelect(book);
        }

        fetchSummary();
    }, [book, onBookSelect]);

    return (
        <div className="book-card">
            <div className="book-info">
                <div className="book-details">
                    <h3>{book.name}</h3>
                    <p><strong>Author:</strong> {book.author}</p>
                    <p><strong>Publisher:</strong> {book.publisher}</p>
                    <p><strong>Release Date:</strong> {book.release_date}</p>
                    <p><strong>Rating:</strong> {book.rating}</p>
                    {loading && <p>Loading summary...</p>}
                    {summary && (
                        <div>
                            <h4>Summary:</h4>
                            <p>{summary}</p>
                        </div>
                    )}
                </div>
                <img src={book.url} alt={book.name} className="book-image" />
            </div>
        </div>
    );
};

BookSummary.propTypes = {
    book: PropTypes.object.isRequired,
    onBookSelect: PropTypes.func,
};

export default BookSummary;
