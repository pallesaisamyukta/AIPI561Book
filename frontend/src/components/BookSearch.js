import React, { useState } from 'react';
import PropTypes from 'prop-types';
import BookData from './BookData'; // Ensure you import BookData correctly

const BookSearch = ({ onBookSelect, summaries }) => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = () => {
        if (!BookData || !BookData.data || !BookData.data.books) {
            console.error('BookData is not available or has an incorrect structure.');
            setResults([]);
            return;
        }

        const booksArray = BookData.data.books;
        const filteredBooks = booksArray.filter(book => 
            book.name.toLowerCase().includes(query.toLowerCase())
        );

        if (filteredBooks.length > 0) {
            const foundBook = filteredBooks[0];
            const precedingBooks = booksArray.filter(book => 
                parseInt(book.id) < parseInt(foundBook.id)
            );
            setResults(precedingBooks);

            // Pass each preceding book to the parent component
            if (onBookSelect) {
                precedingBooks.forEach(book => {
                    onBookSelect(book); // Pass each preceding book one by one
                });
            }
        } else {
            setResults([]);
        }
    };

    return (
        <div>
            <div className="search-container">
                <input 
                    type="text" 
                    value={query} 
                    onChange={(e) => setQuery(e.target.value)} 
                    placeholder="Search for a book" 
                />
                <button onClick={handleSearch}>Search</button>
            </div>
            {results.length > 0 && (
                <h2 className="results-heading">Preceding Books in the Series</h2>
            )}
            <div className="results-container">
                {results.map(book => (
                    <div key={book.id} className="book-card">
                        <div className="book-info">
                            <div className="book-details">
                                <h3>{book.name}</h3>
                                <p><strong>Author:</strong> {book.author}</p>
                                <p><strong>Publisher:</strong> {book.publisher}</p>
                                <p><strong>Release Date:</strong> {book.release_date}</p>
                                <p><strong>Rating:</strong> {book.rating}</p>
                                {/* Display summary if available */}
                                {summaries[book.id] && (
                                    <div>
                                        <h4>Summary:</h4>
                                        <p>{summaries[book.id]}</p>
                                    </div>
                                )}
                            </div>
                            <img src={book.url} alt={book.name} className="book-image" />
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

BookSearch.propTypes = {
    onBookSelect: PropTypes.func.isRequired,
    summaries: PropTypes.object.isRequired,
};

export default BookSearch;
