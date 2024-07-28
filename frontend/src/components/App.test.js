// frontend/src/components/App.test.js

import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Book Summarizer header', () => {
  render(<App />);
  const headerElement = screen.getByText(/Book Summarizer/i);
  expect(headerElement).toBeInTheDocument();
});
