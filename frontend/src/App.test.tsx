import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';
import axios from 'axios';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

test('renders flashcard app and handles initial data loading', async () => {
  mockedAxios.get.mockImplementation((url) => {
    if (url === 'http://localhost:8000/stats') {
      return Promise.resolve({ data: { total_words: 10, correct_percentage: 75, trend: 'increasing' } });
    }
    if (url === 'http://localhost:8000/next-card') {
      // Simulate no cards being due for review
      return Promise.reject({ response: { status: 404 } });
    }
    return Promise.reject(new Error('Not found'));
  });

  render(<App />);

  // Check that the main title is rendered
  expect(screen.getByText(/Flashcard App/i)).toBeInTheDocument();

  // Check that the stats are displayed correctly after fetching
  expect(await screen.findByText(/Total Words: 10/i)).toBeInTheDocument();
  expect(await screen.findByText(/Correct Percentage: 75%/i)).toBeInTheDocument();

  // Check that the flashcard component shows the "no cards" message
  expect(await screen.findByText(/No cards to review./i)).toBeInTheDocument();
});
