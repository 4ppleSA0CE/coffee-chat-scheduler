import { useState } from 'react';

/**
 * BookingForm component - form for collecting attendee information
 */
export default function BookingForm({ selectedSlot, onSubmit, isSubmitting }) {
  const [formData, setFormData] = useState({
    attendee_name: '',
    attendee_email: '',
    notes: ''
  });
  const [errors, setErrors] = useState({});

  // Email validation regex
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  // Validate form
  const validate = () => {
    const newErrors = {};

    if (!formData.attendee_name.trim()) {
      newErrors.attendee_name = 'Name is required';
    }

    if (!formData.attendee_email.trim()) {
      newErrors.attendee_email = 'Email is required';
    } else if (!emailRegex.test(formData.attendee_email)) {
      newErrors.attendee_email = 'Please enter a valid email address';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle input change
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!selectedSlot) {
      return;
    }

    if (validate()) {
      onSubmit({
        ...formData,
        start_time: selectedSlot.start,
        end_time: selectedSlot.end
      });
    }
  };

  // Don't render if no slot is selected
  if (!selectedSlot) {
    return null;
  }

  return (
    <div className="mb-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Booking Details</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Name field */}
        <div>
          <label htmlFor="attendee_name" className="block text-sm font-medium text-gray-700 mb-1">
            Your Name <span className="text-red-500">*</span>
          </label>
          <input
            id="attendee_name"
            name="attendee_name"
            type="text"
            value={formData.attendee_name}
            onChange={handleChange}
            className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
              errors.attendee_name ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="Enter your name"
            disabled={isSubmitting}
          />
          {errors.attendee_name && (
            <p className="mt-1 text-sm text-red-600">{errors.attendee_name}</p>
          )}
        </div>

        {/* Email field */}
        <div>
          <label htmlFor="attendee_email" className="block text-sm font-medium text-gray-700 mb-1">
            Your Email <span className="text-red-500">*</span>
          </label>
          <input
            id="attendee_email"
            name="attendee_email"
            type="email"
            value={formData.attendee_email}
            onChange={handleChange}
            className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
              errors.attendee_email ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="your.email@example.com"
            disabled={isSubmitting}
          />
          {errors.attendee_email && (
            <p className="mt-1 text-sm text-red-600">{errors.attendee_email}</p>
          )}
        </div>

        {/* Notes field */}
        <div>
          <label htmlFor="notes" className="block text-sm font-medium text-gray-700 mb-1">
            Notes (Optional)
          </label>
          <textarea
            id="notes"
            name="notes"
            value={formData.notes}
            onChange={handleChange}
            rows={3}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="Any additional information or reason for the meeting..."
            disabled={isSubmitting}
          />
        </div>

        {/* Submit button */}
        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-blue-500 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isSubmitting ? 'Submitting...' : 'Confirm Booking'}
        </button>
      </form>
    </div>
  );
}

