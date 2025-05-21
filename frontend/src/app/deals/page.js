'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useDispatch, useSelector } from 'react-redux';
import { fetchDeals, saveUserDeal } from '@/lib/redux/slices/dealsSlice';
import { Tag, Calendar, DollarSign, Bookmark, MapPin, Plane, AlertCircle } from 'lucide-react';

export default function DealsPage() {
  const dispatch = useDispatch();
  const { deals, loading, error } = useSelector((state) => state.deals);
  const [filterType, setFilterType] = useState('all');

  useEffect(() => {
    dispatch(fetchDeals());
  }, [dispatch]);

  const handleSaveDeal = (dealId) => {
    dispatch(saveUserDeal(dealId));
  };

  const filteredDeals = filterType === 'all' 
    ? deals 
    : deals.filter(deal => deal.type === filterType);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Travel Deals</h1>
        <p className="mt-2 text-lg text-gray-600">
          Discover our latest and greatest travel deals from around the world.
        </p>
      </div>

      {error && (
        <div className="mb-6 bg-red-50 p-4 rounded-md flex">
          <AlertCircle className="h-5 w-5 text-red-400 mr-2" />
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      <div className="mb-6">
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setFilterType('all')}
            className={`px-4 py-2 rounded-full text-sm font-medium ${
              filterType === 'all'
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
            }`}
          >
            All Deals
          </button>
          <button
            onClick={() => setFilterType('flight')}
            className={`px-4 py-2 rounded-full text-sm font-medium ${
              filterType === 'flight'
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
            }`}
          >
            <Plane className="inline-block w-4 h-4 mr-1" />
            Flights
          </button>
          <button
            onClick={() => setFilterType('hotel')}
            className={`px-4 py-2 rounded-full text-sm font-medium ${
              filterType === 'hotel'
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
            }`}
          >
            <MapPin className="inline-block w-4 h-4 mr-1" />
            Hotels
          </button>
          <button
            onClick={() => setFilterType('package')}
            className={`px-4 py-2 rounded-full text-sm font-medium ${
              filterType === 'package'
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
            }`}
          >
            <Tag className="inline-block w-4 h-4 mr-1" />
            Packages
          </button>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center items-center p-12">
          <svg className="animate-spin h-10 w-10 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {filteredDeals.length > 0 ? (
            filteredDeals.map((deal) => (
              <div key={deal.id} className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200 hover:shadow-lg transition-shadow">
                <div className="relative">
                  <img 
                    src={deal.image_url || 'https://images.unsplash.com/photo-1569949381669-ecf31ae8e613?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8dHJhdmVsfGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'} 
                    alt={deal.title}
                    className="w-full h-48 object-cover"
                  />
                  {deal.discount_percentage && (
                    <div className="absolute top-2 right-2 bg-red-500 text-white py-1 px-2 rounded-md text-sm font-bold">
                      {deal.discount_percentage}% OFF
                    </div>
                  )}
                </div>
                <div className="p-4">
                  <div className="flex justify-between items-center mb-2">
                    <span className="inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-xs font-medium text-indigo-700">
                      {deal.type === 'flight' ? <Plane className="mr-1 h-3 w-3" /> 
                      : deal.type === 'hotel' ? <MapPin className="mr-1 h-3 w-3" /> 
                      : <Tag className="mr-1 h-3 w-3" />}
                      {deal.type.charAt(0).toUpperCase() + deal.type.slice(1)}
                    </span>
                    <button 
                      onClick={() => handleSaveDeal(deal.id)}
                      className="text-gray-400 hover:text-indigo-600"
                      aria-label="Save deal"
                    >
                      <Bookmark className="h-5 w-5" />
                    </button>
                  </div>
                  <h3 className="text-lg font-bold text-gray-900 mb-1">{deal.title}</h3>
                  <p className="text-gray-600 text-sm mb-3">{deal.description}</p>
                  <div className="flex items-center mb-3">
                    <MapPin className="h-4 w-4 text-gray-500 mr-1" />
                    <span className="text-gray-700 text-sm">{deal.destination}</span>
                  </div>
                  <div className="flex items-center mb-3">
                    <Calendar className="h-4 w-4 text-gray-500 mr-1" />
                    <span className="text-gray-700 text-sm">
                      {new Date(deal.valid_from).toLocaleDateString()} - {new Date(deal.valid_to).toLocaleDateString()}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <div className="flex items-center">
                      <DollarSign className="h-5 w-5 text-indigo-600" />
                      <span className="text-2xl font-bold text-indigo-600">${deal.price}</span>
                      {deal.original_price && (
                        <span className="ml-2 text-sm text-gray-500 line-through">${deal.original_price}</span>
                      )}
                    </div>
                    <Link 
                      href={`/deals/${deal.id}`}
                      className="text-sm font-medium text-indigo-600 hover:text-indigo-500"
                    >
                      View details →
                    </Link>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="col-span-3 text-center p-12">
              <p className="text-lg text-gray-600">No deals found matching your filter criteria.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
