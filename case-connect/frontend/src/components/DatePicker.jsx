import React from 'react';
import { Calendar } from 'lucide-react';

const DatePicker = ({ startDate, endDate, onDateChange }) => {
  return (
    <div className="flex flex-col space-y-2">
      <label className="text-sm font-medium text-gray-700">Date Range</label>
      <div className="flex items-center space-x-4">
        <div className="relative">
          <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <input
            type="date"
            value={startDate}
            onChange={(e) => onDateChange('start', e.target.value)}
            className="pl-10 pr-3 py-2 border rounded-md text-sm focus:ring-2 focus:ring-pink-200 focus:border-pink-300"
          />
        </div>
        <span className="text-gray-500">to</span>
        <div className="relative">
          <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <input
            type="date"
            value={endDate}
            onChange={(e) => onDateChange('end', e.target.value)}
            className="pl-10 pr-3 py-2 border rounded-md text-sm focus:ring-2 focus:ring-pink-200 focus:border-pink-300"
          />
        </div>
      </div>
    </div>
  );
};

export default DatePicker;
