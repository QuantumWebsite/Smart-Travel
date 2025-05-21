'use client';

import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchUserSavedDeals } from '@/lib/redux/slices/dealsSlice';
import Link from 'next/link';
import { 
  Bookmark, 
  CalendarDays, 
  DollarSign, 
  MapPin, 
  Plane, 
  Tag, 
  Loader2, 
  AlertTriangle, 
  Building
} from 'lucide-react';

export default function SavedDealsPage() {
  const dispatch = useDispatch();
  const { savedDeals, loading, error } = useSelector((state) => state.deals);
  const { isAuthenticated } = useSelector((state) => state.auth);

  useEffect(() => {
    if (isAuthenticated) {
      dispatch(fetchUserSavedDeals());
    }
  }, [dispatch, isAuthenticated]);

  // Helper function to get the appropriate icon for the deal type
  const getDealTypeIcon = (type) => {
    switch(type) {
      case 'flight':
        return <Plane className="w-4 h-4" />;
      case 'hotel':
        return <Building className="w-4 h-4" />;
      default:
        return <Tag className="w-4 h-4" />;
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <Bookmark className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-2">You need to be logged in</h1>
          <p className="text-gray-600 mb-6">Please log in to view your saved deals</p>
          <Link href="/login" className="px-4 py-2 bg-indigo-600 text-white rounded-md">
            Login
          </Link>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center p-12">
        <Loader2 className="animate-spin h-10 w-10 text-indigo-600" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6 bg-red-50 p-4 rounded-md flex">
          <AlertTriangle className="h-5 w-5 text-red-400 mr-2" />
          <p className="text-sm text-red-700">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">My Saved Deals</h1>
        <p className="mt-2 text-lg text-gray-600">
          All your favorite travel deals saved in one place.
        </p>
      </div>

      {savedDeals.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg shadow-sm">
          <Bookmark className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-medium text-gray-900 mb-2">No saved deals yet</h2>
          <p className="text-gray-500 mb-6">Save interesting deals for later by clicking the bookmark icon.</p>
          <Link href="/deals" className="text-indigo-600 font-medium hover:text-indigo-800">
            Browse deals now
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {savedDeals.map((deal) => (
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
                    {getDealTypeIcon(deal.type)}
                    <span className="ml-1">{deal.type.charAt(0).toUpperCase() + deal.type.slice(1)}</span>
                  </span>
                  <span className="text-indigo-600">
                    <Bookmark className="h-5 w-5 fill-current" />
                  </span>
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-1">{deal.title}</h3>
                <p className="text-gray-600 text-sm mb-3 line-clamp-2">{deal.description}</p>
                <div className="flex items-center mb-3">
                  <MapPin className="h-4 w-4 text-gray-500 mr-1" />
                  <span className="text-gray-700 text-sm">{deal.destination}</span>
                </div>
                <div className="flex items-center mb-3">
                  <CalendarDays className="h-4 w-4 text-gray-500 mr-1" />
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
          ))}
        </div>
      )}
    </div>
  );
}
