import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';
import { server as mswServer, rest } from 'msw/node';

// Setup mock server and handlers
const mockServer = mswServer(
  rest.post('http://localhost:5050/summarize', (req, res, ctx) => {
    return res(ctx.json({ summary: 'Mocked summary text' }));
  })
);

// Setup and teardown server for tests
beforeAll(() => mockServer.listen());
afterEach(() => mockServer.resetHandlers());
afterAll(() => mockServer.close());

test('renders App and fetches book summary', async () => {
  render(<App />);
  
  // Mock book selection
  fireEvent.click(screen.getByText(/select book/i)); // Make sure there's a button or element to select a book

  // Verify loading indicator is shown
  expect(screen.getByText(/loading.../i)).toBeInTheDocument(); // Adjust the text to match your actual loading indicator

  // Wait for the summary to be displayed
  await waitFor(() => {
    expect(screen.getByText('Mocked summary text')).toBeInTheDocument();
  });

  // Optionally, verify if the API call was made
  // You might need additional checks or verifications depending on the implementation
});

test('handles API error gracefully', async () => {
  mockServer.use(
    rest.post('http://localhost:5050/summarize', (req, res, ctx) => {
      return res(ctx.status(500)); // Simulate an error
    })
  );

  render(<App />);
  
  // Mock book selection
  fireEvent.click(screen.getByText(/select book/i)); // Make sure there's a button or element to select a book
  
  // Verify loading indicator is shown
  expect(screen.getByText(/loading.../i)).toBeInTheDocument(); // Adjust the text to match your actual loading indicator

  // Wait for the loading to finish and check if an error message is displayed
  await waitFor(() => {
    expect(screen.queryByText('Mocked summary text')).not.toBeInTheDocument();
    expect(screen.getByText(/error fetching summary/i)).toBeInTheDocument(); // Adjust this to match your actual error handling
  });
});
