/**
 * TimeSlotList component - displays available time slots and allows selection
 */
export default function TimeSlotList({ slots, selectedSlot, onSlotSelect, loading, error }) {
  // Format ISO datetime string to user-friendly time format
  const formatTime = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true 
    });
  };

  // Loading state
  if (loading) {
    return (
      <div className="mb-6">
        <h3 className="text-lg font-medium text-gray-900 mb-3">Available Time Slots</h3>
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          <span className="ml-3 text-gray-600">Loading available slots...</span>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="mb-6">
        <h3 className="text-lg font-medium text-gray-900 mb-3">Available Time Slots</h3>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
        </div>
      </div>
    );
  }

  // No slots available
  if (!slots || slots.length === 0) {
    return (
      <div className="mb-6">
        <h3 className="text-lg font-medium text-gray-900 mb-3">Available Time Slots</h3>
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <p className="text-yellow-800">No available slots for this date. Please select another date.</p>
        </div>
      </div>
    );
  }

  // Display slots
  return (
    <div className="mb-6">
      <h3 className="text-lg font-medium text-gray-900 mb-3">Available Time Slots</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
        {slots.map((slot) => {
          const isSelected = selectedSlot?.start === slot.start;
          return (
            <button
              key={slot.start}
              onClick={() => onSlotSelect(slot)}
              className={`p-4 border-2 rounded-lg text-left transition-all ${
                isSelected
                  ? 'bg-blue-500 text-white border-blue-600 shadow-md'
                  : 'bg-white text-gray-900 border-gray-300 hover:border-blue-400 hover:shadow-sm'
              }`}
            >
              <div className="font-medium">
                {formatTime(slot.start)} - {formatTime(slot.end)}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

