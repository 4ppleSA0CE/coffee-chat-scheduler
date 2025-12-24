import { useState, useEffect } from 'react';
import Layout from './components/Layout';
import DatePicker from './components/DatePicker';
import TimeSlotList from './components/TimeSlotList';
import BookingForm from './components/BookingForm';
import { fetchAvailability, createBooking } from './services/api';

function App() {
  // State management
  const [selectedDate, setSelectedDate] = useState('');
  const [availableSlots, setAvailableSlots] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(null);

  // Fetch availability when date changes
  useEffect(() => {
    if (!selectedDate) {
      setAvailableSlots([]);
      setSelectedSlot(null);
      setError('');
      return;
    }

    const loadAvailability = async () => {
      setLoading(true);
      setError('');
      setSelectedSlot(null); // Reset selected slot when date changes
      
      try {
        const response = await fetchAvailability(selectedDate);
        setAvailableSlots(response.available_slots || []);
      } catch (err) {
        setError(err.message || 'Failed to load available slots');
        setAvailableSlots([]);
      } finally {
        setLoading(false);
      }
    };

    loadAvailability();
  }, [selectedDate]);

  // Handle date selection
  const handleDateChange = (date) => {
    setSelectedDate(date);
    setSuccess(null); // Clear success message when date changes
  };

  // Handle slot selection
  const handleSlotSelect = (slot) => {
    setSelectedSlot(slot);
    setError(''); // Clear any previous errors
    setSuccess(null); // Clear success message
  };

  // Handle form submission
  const handleBookingSubmit = async (bookingData) => {
    setSubmitting(true);
    setError('');

    try {
      const booking = await createBooking(bookingData);
      setSuccess({
        id: booking.id,
        attendee_name: booking.attendee_name,
        start_time: booking.start_time,
        end_time: booking.end_time
      });
      
      // Reset form state
      setSelectedSlot(null);
      setAvailableSlots([]);
      setSelectedDate('');
    } catch (err) {
      setError(err.message || 'Failed to create booking. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  // Handle booking another slot
  const handleBookAnother = () => {
    setSuccess(null);
    setSelectedDate('');
    setSelectedSlot(null);
    setAvailableSlots([]);
    setError('');
  };

  // Format time for display
  const formatTime = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true 
    });
  };

  // Format date for display (can accept ISO datetime string or YYYY-MM-DD date string)
  const formatDate = (dateString) => {
    if (!dateString) return '';
    // Handle both ISO datetime strings and YYYY-MM-DD format
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      weekday: 'long',
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  return (
    <Layout>
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-semibold text-gray-900 mb-2">
            Book a Coffee Chat
          </h2>
          <p className="text-gray-600">
            Select a date and time slot to schedule your coffee chat.
          </p>
        </div>

        {/* Success message */}
        {success && (
          <div className="mb-6 bg-green-50 border border-green-200 rounded-lg p-6">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <svg className="h-6 w-6 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="ml-3 flex-1">
                <h3 className="text-lg font-medium text-green-800 mb-2">
                  Booking Confirmed!
                </h3>
                <p className="text-green-700 mb-4">
                  Your coffee chat with <strong>{success.attendee_name}</strong> has been scheduled for:
                </p>
                <p className="text-green-800 font-medium mb-4">
                  {formatDate(success.start_time)} from {formatTime(success.start_time)} to {formatTime(success.end_time)}
                </p>
                <p className="text-sm text-green-600 mb-4">
                  A calendar invitation has been sent to your email.
                </p>
                <button
                  onClick={handleBookAnother}
                  className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
                >
                  Book Another Slot
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Error message (general) */}
        {error && !loading && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {/* Booking flow (only show if not in success state) */}
        {!success && (
          <>
            {/* Date Picker */}
            <DatePicker 
              selectedDate={selectedDate} 
              onDateChange={handleDateChange} 
            />

            {/* Time Slot List */}
            {selectedDate && (
              <TimeSlotList
                slots={availableSlots}
                selectedSlot={selectedSlot}
                onSlotSelect={handleSlotSelect}
                loading={loading}
                error={error}
              />
            )}

            {/* Booking Form */}
            {selectedSlot && (
              <BookingForm
                selectedSlot={selectedSlot}
                onSubmit={handleBookingSubmit}
                isSubmitting={submitting}
              />
            )}
          </>
        )}
      </div>
    </Layout>
  );
}

export default App;
