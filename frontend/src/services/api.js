/**
 * API client for communicating with the backend
 */
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Fetch available time slots for a specific date
 * @param {string} date - Date in YYYY-MM-DD format
 * @returns {Promise<Object>} Response with available slots
 */
export async function fetchAvailability(date) {
  const response = await fetch(`${API_URL}/api/availability?date=${date}`);
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(error.detail || `Failed to fetch availability: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Create a new booking
 * @param {Object} bookingData - Booking data
 * @param {string} bookingData.attendee_name - Name of the attendee
 * @param {string} bookingData.attendee_email - Email of the attendee
 * @param {string} bookingData.start_time - Start time in ISO 8601 format
 * @param {string} bookingData.end_time - End time in ISO 8601 format
 * @param {string} [bookingData.notes] - Optional notes/reason for meeting
 * @returns {Promise<Object>} Created booking object
 */
export async function createBooking(bookingData) {
  const response = await fetch(`${API_URL}/api/bookings`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(bookingData),
  });
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(error.detail || 'Failed to create booking');
  }
  
  return response.json();
}

