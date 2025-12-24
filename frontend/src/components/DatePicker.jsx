/**
 * DatePicker component - allows user to select a date for booking
 * Minimum date is tomorrow (24-hour lead time requirement)
 */
export default function DatePicker({ selectedDate, onDateChange }) {
  // Calculate minimum date (tomorrow)
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  const minDate = tomorrow.toISOString().split('T')[0];

  return (
    <div className="mb-6">
      <label htmlFor="date-picker" className="block text-sm font-medium text-gray-700 mb-2">
        Select a Date
      </label>
      <input
        id="date-picker"
        type="date"
        value={selectedDate || ''}
        onChange={(e) => onDateChange(e.target.value)}
        min={minDate}
        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg"
      />
      <p className="mt-1 text-sm text-gray-500">
        Bookings must be made at least 24 hours in advance
      </p>
    </div>
  );
}

