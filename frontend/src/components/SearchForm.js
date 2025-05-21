'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useDispatch, useSelector } from 'react-redux';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { performSearch, updateSearchParams, clearError } from '@/lib/redux/slices/searchSlice';
import { MapPin, Calendar, Users, DollarSign, Plane, Search, AlertCircle } from 'lucide-react';

export default function SearchForm({ initialData = {} }) {
  const router = useRouter();
  const dispatch = useDispatch();
  const { loading, error, currentSearch } = useSelector((state) => state.search);
  
  const [formData, setFormData] = useState({
    destination: initialData.destination || '',
    departure_location: initialData.departure_location || '',
    departure_date: initialData.departure_date ? new Date(initialData.departure_date) : null,
    return_date: initialData.return_date ? new Date(initialData.return_date) : null,
    adults: initialData.adults || 1,
    children: initialData.children || 0,
    budget: initialData.budget || '',
    preferences: initialData.preferences || {},
  });

  useEffect(() => {
    dispatch(clearError());
  }, [dispatch]);

  useEffect(() => {
    if (currentSearch) {
      router.push(`/search-results/${currentSearch.id}`);
    }
  }, [currentSearch, router]);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'number' ? parseInt(value, 10) : value,
    });
  };

  const handleDateChange = (date, name) => {
    setFormData({
      ...formData,
      [name]: date,
    });
  };

  const handlePreferenceChange = (e) => {
    const { name, value, checked, type } = e.target;
    
    setFormData({
      ...formData,
      preferences: {
        ...formData.preferences,
        [name]: type === 'checkbox' ? checked : value,
      },
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Save to redux and also perform search
    dispatch(updateSearchParams(formData));

    // Format the dates for API
    const searchData = {
      ...formData,
      departure_date: formData.departure_date.toISOString().split('T')[0],
      return_date: formData.return_date.toISOString().split('T')[0],
      budget: formData.budget ? parseFloat(formData.budget) : null,
    };

    dispatch(performSearch(searchData));
  };

  return (
    <div className="bg-white shadow-md rounded-lg overflow-hidden">
      <div className="p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Find your perfect trip</h2>
        
        {error && (
          <div className="mb-6 bg-red-50 p-4 rounded-md flex">
            <AlertCircle className="h-5 w-5 text-red-400 mr-2" />
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="destination" className="block text-sm font-medium text-gray-700 mb-1">
                Destination
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <MapPin className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="text"
                  id="destination"
                  name="destination"
                  value={formData.destination}
                  onChange={handleChange}
                  required
                  placeholder="Where do you want to go?"
                  className="block w-full rounded-md border-gray-300 pl-10 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-3 px-4"
                />
              </div>
            </div>

            <div>
              <label htmlFor="departure_location" className="block text-sm font-medium text-gray-700 mb-1">
                Departure location
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Plane className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="text"
                  id="departure_location"
                  name="departure_location"
                  value={formData.departure_location}
                  onChange={handleChange}
                  required
                  placeholder="Where are you traveling from?"
                  className="block w-full rounded-md border-gray-300 pl-10 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-3 px-4"
                />
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label htmlFor="departure_date" className="block text-sm font-medium text-gray-700 mb-1">
                Departure date
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Calendar className="h-5 w-5 text-gray-400" />
                </div>
                <DatePicker
                  selected={formData.departure_date}
                  onChange={(date) => handleDateChange(date, 'departure_date')}
                  required
                  minDate={new Date()}
                  className="block w-full rounded-md border-gray-300 pl-10 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-3 px-4"
                />
              </div>
            </div>

            <div>
              <label htmlFor="return_date" className="block text-sm font-medium text-gray-700 mb-1">
                Return date
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Calendar className="h-5 w-5 text-gray-400" />
                </div>
                <DatePicker
                  selected={formData.return_date}
                  onChange={(date) => handleDateChange(date, 'return_date')}
                  required
                  minDate={formData.departure_date || new Date()}
                  className="block w-full rounded-md border-gray-300 pl-10 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-3 px-4"
                />
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label htmlFor="adults" className="block text-sm font-medium text-gray-700 mb-1">
                Adults
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Users className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="number"
                  id="adults"
                  name="adults"
                  value={formData.adults}
                  onChange={handleChange}
                  min="1"
                  max="10"
                  className="block w-full rounded-md border-gray-300 pl-10 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-3 px-4"
                />
              </div>
            </div>

            <div>
              <label htmlFor="children" className="block text-sm font-medium text-gray-700 mb-1">
                Children
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Users className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="number"
                  id="children"
                  name="children"
                  value={formData.children}
                  onChange={handleChange}
                  min="0"
                  max="10"
                  className="block w-full rounded-md border-gray-300 pl-10 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-3 px-4"
                />
              </div>
            </div>

            <div>
              <label htmlFor="budget" className="block text-sm font-medium text-gray-700 mb-1">
                Budget (USD)
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <DollarSign className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="number"
                  id="budget"
                  name="budget"
                  value={formData.budget}
                  onChange={handleChange}
                  min="0"
                  step="100"
                  placeholder="Optional"
                  className="block w-full rounded-md border-gray-300 pl-10 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-3 px-4"
                />
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-medium text-gray-900 mb-3">Travel preferences</h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
              <div className="flex items-center">
                <input
                  id="beach"
                  name="beach"
                  type="checkbox"
                  checked={formData.preferences.beach || false}
                  onChange={handlePreferenceChange}
                  className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                />
                <label htmlFor="beach" className="ml-3 text-sm text-gray-700">
                  Beach
                </label>
              </div>
              <div className="flex items-center">
                <input
                  id="mountains"
                  name="mountains"
                  type="checkbox"
                  checked={formData.preferences.mountains || false}
                  onChange={handlePreferenceChange}
                  className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                />
                <label htmlFor="mountains" className="ml-3 text-sm text-gray-700">
                  Mountains
                </label>
              </div>
              <div className="flex items-center">
                <input
                  id="city"
                  name="city"
                  type="checkbox"
                  checked={formData.preferences.city || false}
                  onChange={handlePreferenceChange}
                  className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                />
                <label htmlFor="city" className="ml-3 text-sm text-gray-700">
                  City
                </label>
              </div>
              <div className="flex items-center">
                <input
                  id="luxury"
                  name="luxury"
                  type="checkbox"
                  checked={formData.preferences.luxury || false}
                  onChange={handlePreferenceChange}
                  className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                />
                <label htmlFor="luxury" className="ml-3 text-sm text-gray-700">
                  Luxury
                </label>
              </div>
              <div className="flex items-center">
                <input
                  id="budget_friendly"
                  name="budget_friendly"
                  type="checkbox"
                  checked={formData.preferences.budget_friendly || false}
                  onChange={handlePreferenceChange}
                  className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                />
                <label htmlFor="budget_friendly" className="ml-3 text-sm text-gray-700">
                  Budget-friendly
                </label>
              </div>
              <div className="flex items-center">
                <input
                  id="family_friendly"
                  name="family_friendly"
                  type="checkbox"
                  checked={formData.preferences.family_friendly || false}
                  onChange={handlePreferenceChange}
                  className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                />
                <label htmlFor="family_friendly" className="ml-3 text-sm text-gray-700">
                  Family-friendly
                </label>
              </div>
            </div>
          </div>

          <div className="flex justify-center">
            <button
              type="submit"
              disabled={loading}
              className="flex justify-center items-center bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-8 rounded-md focus:outline-none focus:shadow-outline disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Searching...
                </>
              ) : (
                <>
                  <Search className="mr-2 h-5 w-5" />
                  Search for trips
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
