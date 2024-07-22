import openBook from '../images/open-book.png';
import React from 'react';

export default function Header() {
    return (
        <div className="header">
            <img src={openBook} alt="Open Book" className="header--image"/>
            <h2 className="header--title">Book Summarizer</h2>
            <h3 className="header--project">History</h3>
        </div> 
    )
}
