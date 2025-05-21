'use client';

import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getSearchResults } from '@/lib/redux/slices/searchSlice';
import { 
  Loader2, 
  AlertTriangle, 
  Plane, 
  Building, 
  Map, 
  Calendar, 
  DollarSign, 
  ArrowRight, 
  Clock, 
  Star, 
  ArrowLeft,
  ChevronDown,
  ChevronUp,
  Filter,
  MapPin
} from 'lucide-react';
import Link from 'next/link';

export default function SearchResultsPage({ params }) {
  const dispatch = useDispatch();
  const { searchResults, loading, error } = useSelector((state) => state.search);
  const searchId = params.id;
  
  const [sortBy, setSortBy] = useState('price');
  const [filterType, setFilterType] = useState('all');
  const [showFilters, setShowFilters] = useState(false);
  
  useEffect(() => {
    if (searchId) {
      dispatch(getSearchResults(searchId));
    }
  }, [dispatch, searchId]);
  
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <Loader2 className="w-12 h-12 text-indigo-600 animate-spin" />
        <p className="mt-4 text-lg text-gray-600">Searching for the best options...</p>
        <p className="text-sm text-gray-500">This may take a moment</p>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <AlertTriangle className="w-12 h-12 text-red-600" />
        <p className="mt-4 text-lg text-gray-600">Error: {error}</p>
        <Link
          href="/search"
          className="mt-4 inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Search
        </Link>
      </div>
    );
  }
  
  if (!searchResults) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-12">
          <AlertTriangle className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900">Search results not found</h3>
          <Link
            href="/search"
            className="mt-4 inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Search
          </Link>
        </div>
      </div>
    );
  }
  
  const flights = searchResults.flights || [];
  const hotels = searchResults.hotels || [];
  const packages = searchResults.packages || [];
  
  // Combine all results for display
  let allResults = [
    ...flights.map(item => ({ ...item, type: 'flight' })),
    ...hotels.map(item => ({ ...item, type: 'hotel' })),
    ...packages.map(item => ({ ...item, type: 'package' })),
  ];
  
  // Filter by type if needed
  if (filterType !== 'all') {
    allResults = allResults.filter(item => item.type === filterType);
  }
  
  // Sort results
  allResults.sort((a, b) => {
    switch (sortBy) {
      case 'price':
        return a.price - b.price;
      case 'duration':
        if (a.type === 'flight' && b.type === 'flight') {
          return a.duration - b.duration;
        }
        return 0;
      case 'rating':
        return (b.rating || 0) - (a.rating || 0);
      default:
        return 0;
    }
  });
  
  const getIcon = (type) => {
    switch (type) {
      case 'flight':
        return <Plane className="w-5 h-5" />;
      case 'hotel':
        return <Building className="w-5 h-5" />;
      case 'package':
        return <Map className="w-5 h-5" />;
      default:
        return null;
    }
  };
  
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">Search Results</h1>
      <p className="text-gray-600 mb-6">
        {searchResults.origin || 'Your location'} to {searchResults.destination || 'Selected destination'} • 
        {searchResults.departure_date && ` ${formatDate(searchResults.departure_date)}`}
        {searchResults.return_date && ` - ${formatDate(searchResults.return_date)}`}
      </p>
      
      <div className="mb-6">
        <button 
          onClick={() => setShowFilters(!showFilters)}
          className="flex items-center text-indigo-600 font-medium"
        >
          <Filter className="w-4 h-4 mr-2" />
          {showFilters ? 'Hide Filters' : 'Show Filters'}
          {showFilters ? <ChevronUp className="w-4 h-4 ml-1" /> : <ChevronDown className="w-4 h-4 ml-1" />}
        </button>
        
        {showFilters && (
          <div className="bg-white p-4 rounded-lg shadow-md mt-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Filter By Type</label>
                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => setFilterType('all')}
                    className={`px-3 py-1 rounded text-sm ${
                      filterType === 'all' 
                        ? 'bg-indigo-600 text-white' 
                        : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                    }`}
                  >
                    All
                  </button>
                  <button
                    onClick={() => setFilterType('flight')}
                    className={`px-3 py-1 rounded text-sm flex items-center ${
                      filterType === 'flight' 
                        ? 'bg-indigo-600 text-white' 
                        : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                    }`}
                  >
                    <Plane className="w-3 h-3 mr-1" />
                    Flights
                  </button>
                  <button
                    onClick={() => setFilterType('hotel')}
                    className={`px-3 py-1 rounded text-sm flex items-center ${
                      filterType === 'hotel' 
                        ? 'bg-indigo-600 text-white' 
                        : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                    }`}
                  >
                    <Building className="w-3 h-3 mr-1" />
                    Hotels
                  </button>
                  <button
                    onClick={() => setFilterType('package')}
                    className={`px-3 py-1 rounded text-sm flex items-center ${
                      filterType === 'package' 
                        ? 'bg-indigo-600 text-white' 
                        : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                    }`}
                  >
                    <Map className="w-3 h-3 mr-1" />
                    Packages
                  </button>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Sort By</label>
                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => setSortBy('price')}
                    className={`px-3 py-1 rounded text-sm flex items-center ${
                      sortBy === 'price' 
                        ? 'bg-indigo-600 text-white' 
                        : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                    }`}
                  >
                    <DollarSign className="w-3 h-3 mr-1" />
                    Price
                  </button>
                  <button
                    onClick={() => setSortBy('duration')}
                    className={`px-3 py-1 rounded text-sm flex items-center ${
                      sortBy === 'duration' 
                        ? 'bg-indigo-600 text-white' 
                        : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                    }`}
                  >
                    <Clock className="w-3 h-3 mr-1" />
                    Duration
                  </button>
                  <button
                    onClick={() => setSortBy('rating')}
                    className={`px-3 py-1 rounded text-sm flex items-center ${
                      sortBy === 'rating' 
                        ? 'bg-indigo-600 text-white' 
                        : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                    }`}
                  >
                    <Star className="w-3 h-3 mr-1" />
                    Rating
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
      
      {allResults.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg shadow-md">
          <AlertTriangle className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">No results found</h2>
          <p className="text-gray-600 mb-6">We couldn't find any matches for your search criteria.</p>
          <Link
            href="/search"
            className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Modify Search
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {allResults.map((result, idx) => {
            if (result.type === 'flight') {
              return (
                <div key={idx} className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200">
                  <div className="flex flex-col md:flex-row">
                    <div className="flex-1 p-4 md:border-r border-gray-200">
                      <div className="flex items-center mb-3">
                        <span className="inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 mr-2">
                          <Plane className="w-3 h-3 mr-1" />
                          Flight
                        </span>
                        <span className="text-sm text-gray-500">{result.airline}</span>
                      </div>
                      
                      <div className="flex items-center justify-between mb-4">
                        <div className="text-center">
                          <p className="text-xl font-bold">{result.departure_time}</p>
                          <p className="text-sm text-gray-500">{result.origin_code}</p>
                        </div>
                        
                        <div className="flex-1 mx-4">
                          <div className="relative">
                            <div className="absolute inset-0 flex items-center">
                              <div className="w-full border-t border-gray-300"></div>
                            </div>
                            <div className="relative flex justify-center text-xs">
                              <span className="px-2 bg-white text-gray-500">
                                {result.duration_text || `${result.duration} mins`}
                              </span>
                            </div>
                          </div>
                          <div className="text-center text-xs text-gray-500 mt-1">
                            {result.stops === 0 ? 'Nonstop' : `${result.stops} ${result.stops === 1 ? 'stop' : 'stops'}`}
                          </div>
                        </div>
                        
                        <div className="text-center">
                          <p className="text-xl font-bold">{result.arrival_time}</p>
                          <p className="text-sm text-gray-500">{result.destination_code}</p>
                        </div>
                      </div>
                      
                      {result.features && result.features.length > 0 && (
                        <div className="mt-2">
                          <div className="flex flex-wrap gap-2">
                            {result.features.map((feature, idx) => (
                              <span key={idx} className="inline-flex items-center rounded-full bg-gray-50 px-2 py-1 text-xs text-gray-600">
                                {feature}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                    
                    <div className="bg-gray-50 p-4 flex flex-col justify-between">
                      <div>
                        <p className="text-2xl font-bold text-indigo-600">${result.price}</p>
                        <p className="text-sm text-gray-500">per person</p>
                      </div>
                      <button className="mt-4 bg-indigo-600 text-white py-2 px-4 rounded hover:bg-indigo-700 transition-colors">
                        Select Flight
                      </button>
                    </div>
                  </div>
                </div>
              );
            } else if (result.type === 'hotel') {
              return (
                <div key={idx} className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200">
                  <div className="flex flex-col md:flex-row">
                    <div className="w-full md:w-1/4 bg-gray-200 h-auto md:h-auto">
                      <img 
                        src={result.image_url || 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8aG90ZWx8ZW58MHx8MHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'} 
                        alt={result.name}
                        className="h-48 md:h-full w-full object-cover"
                      />
                    </div>
                    <div className="flex-1 p-4">
                      <div className="flex justify-between">
                        <div>
                          <div className="flex items-center mb-1">
                            <span className="inline-flex items-center rounded-md bg-green-50 px-2 py-1 text-xs font-medium text-green-700 mr-2">
                              <Building className="w-3 h-3 mr-1" />
                              Hotel
                            </span>
                          </div>
                          <h3 className="text-lg font-bold">{result.name}</h3>
                          <div className="flex items-center mt-1 mb-2">
                            <div className="flex">
                              {Array.from({ length: Math.floor(result.rating || 0) }).map((_, i) => (
                                <Star key={i} className="w-4 h-4 text-yellow-400 fill-current" />
                              ))}
                            </div>
                            <span className="text-sm text-gray-600 ml-1">{result.rating}/5</span>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-2xl font-bold text-indigo-600">${result.price}</p>
                          <p className="text-sm text-gray-500">per night</p>
                        </div>
                      </div>
                      
                      <div className="flex items-center text-sm text-gray-600 mb-3">
                        <MapPin className="w-4 h-4 text-gray-400 mr-1" />
                        <span>{result.location}</span>
                      </div>
                      
                      <p className="text-gray-600 mb-4 line-clamp-2">{result.description}</p>
                      
                      <div className="flex flex-wrap gap-2 mb-4">
                        {(result.amenities || []).slice(0, 4).map((amenity, i) => (
                          <span key={i} className="inline-flex items-center rounded-full bg-gray-50 px-2 py-1 text-xs text-gray-600">
                            {amenity}
                          </span>
                        ))}
                        {(result.amenities || []).length > 4 && (
                          <span className="inline-flex items-center rounded-full bg-gray-50 px-2 py-1 text-xs text-gray-600">
                            +{(result.amenities || []).length - 4} more
                          </span>
                        )}
                      </div>
                      
                      <div className="flex justify-end">
                        <button className="bg-indigo-600 text-white py-2 px-4 rounded hover:bg-indigo-700 transition-colors">
                          View Details
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              );
            } else {
              // Package
              return (
                <div key={idx} className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200">
                  <div className="flex flex-col md:flex-row">
                    <div className="w-full md:w-1/4 bg-gray-200 h-auto md:h-auto">
                      <img 
                        src={result.image_url || 'https://images.unsplash.com/photo-1544644181-1484b3fdfc32?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8cGFja2FnZXxlbnwwfHwwfHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'} 
                        alt={result.name}
                        className="h-48 md:h-full w-full object-cover"
                      />
                    </div>
                    <div className="flex-1 p-4">
                      <div className="flex justify-between">
                        <div>
                          <div className="flex items-center mb-1">
                            <span className="inline-flex items-center rounded-md bg-purple-50 px-2 py-1 text-xs font-medium text-purple-700 mr-2">
                              <Map className="w-3 h-3 mr-1" />
                              Package
                            </span>
                          </div>
                          <h3 className="text-lg font-bold">{result.name}</h3>
                          <div className="flex items-center mt-1 mb-2">
                            <Calendar className="w-4 h-4 text-gray-400 mr-1" />
                            <span className="text-sm text-gray-600">{result.duration} days</span>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-2xl font-bold text-indigo-600">${result.price}</p>
                          <p className="text-sm text-gray-500">per person</p>
                        </div>
                      </div>
                      
                      <div className="flex items-center text-sm text-gray-600 mb-3">
                        <MapPin className="w-4 h-4 text-gray-400 mr-1" />
                        <span>{result.destinations?.join(', ') || result.destination}</span>
                      </div>
                      
                      <p className="text-gray-600 mb-4 line-clamp-2">{result.description}</p>
                      
                      <div className="flex flex-wrap gap-2 mb-4">
                        {(result.includes || []).slice(0, 4).map((item, i) => (
                          <span key={i} className="inline-flex items-center rounded-full bg-gray-50 px-2 py-1 text-xs text-gray-600">
                            {item}
                          </span>
                        ))}
                        {(result.includes || []).length > 4 && (
                          <span className="inline-flex items-center rounded-full bg-gray-50 px-2 py-1 text-xs text-gray-600">
                            +{(result.includes || []).length - 4} more
                          </span>
                        )}
                      </div>
                      
                      <div className="flex justify-end">
                        <button className="bg-indigo-600 text-white py-2 px-4 rounded hover:bg-indigo-700 transition-colors">
                          View Package
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              );
            }
          })}
        </div>
      )}
    </div>
  );
}
