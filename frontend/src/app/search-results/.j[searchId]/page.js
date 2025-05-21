'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { searchAPI } from '@/lib/api';

export default function SearchResultsPage({ params }) {
  const router = useRouter();
  const searchId = params.searchId;
  
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('flights');

  useEffect(() => {
    if (!searchId) return;

    const fetchResults = async () => {
      try {
        setLoading(true);
        const response = await searchAPI.getSearchResults(searchId);
        setResults(response.data);
      } catch (err) {
        console.error('Error fetching search results:', err);
        setError(err.response?.data?.detail || 'Failed to fetch search results');
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
    
    // Poll for results every 10 seconds if the status is 'processing'
    const intervalId = setInterval(async () => {
      try {
        const response = await searchAPI.getSearchResults(searchId);
        setResults(response.data);
        
        // If we have results, stop polling
        if (response.data?.status === 'completed') {
          clearInterval(intervalId);
        }
      } catch (err) {
        console.error('Error polling search results:', err);
        clearInterval(intervalId);
      }
    }, 10000);

    return () => clearInterval(intervalId);
  }, [searchId]);

  const handleSaveDeal = (recommendationId) => {
    // Implementation for saving a deal will be added later
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
          <h2 className="mt-4 text-xl font-semibold">Searching for the best travel options...</h2>
          <p className="mt-2 text-gray-600">This may take a minute or two.</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
              <div className="mt-4">
                <Link
                  href="/search"
                  className="text-sm font-medium text-red-700 hover:text-red-600"
                >
                  Go back to search <span aria-hidden="true">&rarr;</span>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (results?.status === 'processing') {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
          <h2 className="mt-4 text-xl font-semibold">Processing your travel options...</h2>
          <p className="mt-2 text-gray-600">{results.message || 'We're finding the best deals for you.'}</p>
        </div>
      </div>
    );
  }

  const renderFlights = () => {
    if (!results?.flights || results.flights.length === 0) {
      return (
        <p className="text-gray-600 italic">No flight options found for your search criteria.</p>
      );
    }

    return (
      <div className="grid grid-cols-1 gap-6">
        {results.flights.map((flight, index) => (
          <div key={index} className="bg-white rounded-lg shadow overflow-hidden">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <div>
                  <h3 className="text-lg font-bold text-gray-900">{flight.airline}</h3>
                  <p className="text-sm text-gray-600">{flight.flight_number}</p>
                </div>
                <div className="text-right">
                  <p className="text-xl font-bold text-indigo-600">${flight.price}</p>
                  <p className="text-sm text-gray-600">{flight.duration}</p>
                </div>
              </div>
              
              <div className="flex justify-between items-center mb-4">
                <div>
                  <p className="text-sm font-medium text-gray-900">{flight.departure_time}</p>
                  <p className="text-sm text-gray-600">{flight.departure_airport}</p>
                </div>
                <div className="flex-1 mx-4">
                  <div className="relative">
                    <div className="absolute inset-0 flex items-center">
                      <div className="w-full border-t border-gray-300"></div>
                    </div>
                    <div className="relative flex justify-center">
                      <span className="bg-white px-2 text-sm text-gray-500">
                        {flight.stops === 0 ? 'Direct' : `${flight.stops} stop${flight.stops > 1 ? 's' : ''}`}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900">{flight.arrival_time}</p>
                  <p className="text-sm text-gray-600">{flight.arrival_airport}</p>
                </div>
              </div>
              
              <div className="mt-4 flex justify-end">
                <button
                  className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                >
                  View Details
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderHotels = () => {
    if (!results?.hotels || results.hotels.length === 0) {
      return (
        <p className="text-gray-600 italic">No hotel options found for your search criteria.</p>
      );
    }

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {results.hotels.map((hotel, index) => (
          <div key={index} className="bg-white rounded-lg shadow overflow-hidden">
            <div className="p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-2">{hotel.name}</h3>
              <div className="flex items-center mb-2">
                <div className="flex text-yellow-400">
                  {[...Array(hotel.stars || 0)].map((_, i) => (
                    <svg key={i} className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  ))}
                </div>
                <span className="ml-2 text-sm text-gray-600">{hotel.location}</span>
              </div>
              <p className="text-sm text-gray-600 mb-4">{hotel.description?.substring(0, 150)}...</p>
              
              <div className="flex justify-between items-center mt-4">
                <div>
                  <p className="text-xl font-bold text-indigo-600">${hotel.price_per_night} <span className="text-sm font-normal text-gray-600">per night</span></p>
                </div>
                <button
                  className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                >
                  View Details
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderWeather = () => {
    if (!results?.weather_data || results.weather_data.length === 0) {
      return (
        <p className="text-gray-600 italic">No weather data available for this destination.</p>
      );
    }

    return (
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Weather forecast for {results.search?.destination}</h3>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {results.weather_data.map((day, index) => (
              <div key={index} className="border rounded-lg p-4 text-center">
                <p className="font-medium text-gray-900">{new Date(day.date).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}</p>
                <div className="my-2 flex justify-center">
                  {day.condition?.toLowerCase().includes('sun') && (
                    <svg className="h-8 w-8 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                  )}
                  {day.condition?.toLowerCase().includes('cloud') && (
                    <svg className="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
                    </svg>
                  )}
                  {day.condition?.toLowerCase().includes('rain') && (
                    <svg className="h-8 w-8 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                    </svg>
                  )}
                </div>
                <p className="text-lg font-bold">{day.high_temp}°F</p>
                <p className="text-sm text-gray-600">{day.low_temp}°F</p>
                <p className="mt-1 text-xs text-gray-500">{day.condition}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const renderEvents = () => {
    if (!results?.events || results.events.length === 0) {
      return (
        <p className="text-gray-600 italic">No events found during your travel dates.</p>
      );
    }

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {results.events.map((event, index) => (
          <div key={index} className="bg-white rounded-lg shadow overflow-hidden">
            <div className="p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-2">{event.name}</h3>
              <div className="flex items-center mb-2">
                <svg className="h-5 w-5 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span className="text-sm text-gray-600">
                  {new Date(event.date).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
                </span>
              </div>
              <div className="flex items-center mb-4">
                <svg className="h-5 w-5 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span className="text-sm text-gray-600">{event.venue}, {event.location}</span>
              </div>
              <p className="text-sm text-gray-600 mb-4">{event.description?.substring(0, 150)}...</p>
              
              <div className="flex justify-between items-center mt-4">
                <div>
                  {event.price ? (
                    <p className="text-lg font-bold text-indigo-600">${event.price}</p>
                  ) : (
                    <p className="text-sm font-medium text-green-600">Free Event</p>
                  )}
                </div>
                <button
                  className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                >
                  View Details
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderRecommendations = () => {
    if (!results?.recommendations || results.recommendations.length === 0) {
      return (
        <p className="text-gray-600 italic">No recommendations available yet. Please check back soon.</p>
      );
    }

    return (
      <div className="space-y-6">
        {results.recommendations.map((rec, index) => (
          <div key={index} className="bg-white rounded-lg shadow overflow-hidden">
            <div className="p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-2">Recommendation #{index + 1}</h3>
              <p className="text-gray-600 mb-4">{rec.description}</p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
                <div className="border rounded-lg p-4">
                  <h4 className="font-medium text-gray-900 mb-2">Flight</h4>
                  <p className="text-sm text-gray-600">{rec.flight_details?.airline} {rec.flight_details?.flight_number}</p>
                  <p className="text-sm text-gray-600">{rec.flight_details?.departure_time} - {rec.flight_details?.arrival_time}</p>
                  <p className="text-sm font-medium text-indigo-600 mt-2">${rec.flight_details?.price}</p>
                </div>
                
                <div className="border rounded-lg p-4">
                  <h4 className="font-medium text-gray-900 mb-2">Hotel</h4>
                  <p className="text-sm text-gray-600">{rec.hotel_details?.name}</p>
                  <p className="text-sm text-gray-600">{rec.hotel_details?.location}</p>
                  <p className="text-sm font-medium text-indigo-600 mt-2">${rec.hotel_details?.price_per_night} per night</p>
                </div>
              </div>
              
              <div className="mt-6 border-t border-gray-200 pt-4">
                <h4 className="font-medium text-gray-900 mb-2">Why this works for you:</h4>
                <ul className="list-disc list-inside text-sm text-gray-600">
                  {rec.reasons?.map((reason, i) => (
                    <li key={i}>{reason}</li>
                  ))}
                </ul>
              </div>
              
              <div className="mt-6 flex justify-between items-center">
                <p className="text-lg font-bold text-indigo-600">
                  Total estimated cost: ${rec.total_cost}
                </p>
                <div className="flex space-x-4">
                  <button
                    className="inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-indigo-600 shadow-sm ring-1 ring-inset ring-indigo-600 hover:bg-indigo-50"
                  >
                    View Details
                  </button>
                  <button
                    onClick={() => handleSaveDeal(rec.id)}
                    className="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                  >
                    Save This Deal
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Travel Options for {results.search?.destination}</h1>
        <p className="mt-2 text-gray-600">
          {results.search?.departure_location} to {results.search?.destination} • {' '}
          {new Date(results.search?.departure_date).toLocaleDateString()} - {new Date(results.search?.return_date).toLocaleDateString()}
        </p>
      </div>
      
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8" aria-label="Tabs">
          {['flights', 'hotels', 'weather', 'events', 'recommendations'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`
                whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm
                ${activeTab === tab
                  ? 'border-indigo-500 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}
              `}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </nav>
      </div>
      
      <div className="mt-8">
        {activeTab === 'flights' && renderFlights()}
        {activeTab === 'hotels' && renderHotels()}
        {activeTab === 'weather' && renderWeather()}
        {activeTab === 'events' && renderEvents()}
        {activeTab === 'recommendations' && renderRecommendations()}
      </div>
      
      <div className="mt-12 text-center">
        <Link
          href="/search"
          className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
        >
          Start a new search
        </Link>
      </div>
    </div>
  );
}
