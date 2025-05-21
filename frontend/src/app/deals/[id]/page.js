'use client';

import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchDealById, saveUserDeal } from '@/lib/redux/slices/dealsSlice';
import Link from 'next/link';
import { 
  ArrowLeft, 
  MapPin, 
  CalendarDays, 
  DollarSign, 
  Bookmark, 
  Clock, 
  Tag, 
  Building, 
  Plane, 
  Loader2, 
  AlertTriangle,
  Star,
  Check,
  Share2
} from 'lucide-react';
import Image from 'next/image';

export default function DealDetail({ params }) {
  const dispatch = useDispatch();
  const { currentDeal, savedDeals, loading, error } = useSelector((state) => state.deals);
  const dealId = params.id;
  
  const [isSaved, setIsSaved] = useState(false);
  
  useEffect(() => {
    if (dealId) {
      dispatch(fetchDealById(dealId));
    }
  }, [dispatch, dealId]);
  
  useEffect(() => {
    // Check if this deal is already saved
    if (savedDeals && savedDeals.some(deal => deal.id === dealId)) {
      setIsSaved(true);
    }
  }, [savedDeals, dealId]);
  
  const handleSaveDeal = () => {
    dispatch(saveUserDeal(dealId));
    setIsSaved(true);
  };
  
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <Loader2 className="w-12 h-12 text-indigo-600 animate-spin" />
        <p className="mt-4 text-lg text-gray-600">Loading deal details...</p>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <AlertTriangle className="w-12 h-12 text-red-600" />
        <p className="mt-4 text-lg text-gray-600">Error: {error}</p>
        <Link
          href="/deals"
          className="mt-4 inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Deals
        </Link>
      </div>
    );
  }
  
  if (!currentDeal) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-12">
          <AlertTriangle className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900">Deal not found</h3>
          <Link
            href="/deals"
            className="mt-4 inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Deals
          </Link>
        </div>
      </div>
    );
  }
  
  // Decide which icon to use based on deal type
  const getDealTypeIcon = () => {
    switch(currentDeal.type) {
      case 'flight':
        return <Plane className="w-5 h-5" />;
      case 'hotel':
        return <Building className="w-5 h-5" />;
      default:
        return <Tag className="w-5 h-5" />;
    }
  };
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <Link
          href="/deals"
          className="inline-flex items-center text-indigo-600 hover:text-indigo-800"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to All Deals
        </Link>
      </div>
      
      <div className="bg-white rounded-lg shadow-md overflow-hidden mb-8">
        <div className="relative">
          <Image 
            src={currentDeal.image_url || 'https://images.unsplash.com/photo-1569949381669-ecf31ae8e613?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8dHJhdmVsfGVufDB8fDB8fA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1200&q=80'} 
            alt={currentDeal.title}
            className="w-full h-64 md:h-96 object-cover"
            width={1200}
            height={400}
          />
          
          {currentDeal.discount_percentage && (
            <div className="absolute top-4 right-4 bg-red-500 text-white py-2 px-4 rounded-md text-base font-bold">
              {currentDeal.discount_percentage}% OFF
            </div>
          )}
          
          <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
          <div className="absolute bottom-0 left-0 p-6 w-full">
            <div className="flex flex-col md:flex-row md:justify-between md:items-end">
              <div>
                <span className="inline-flex items-center rounded-md bg-indigo-100 px-3 py-1 text-sm font-medium text-indigo-800 mb-2">
                  {getDealTypeIcon()}
                  <span className="ml-1">{currentDeal.type.charAt(0).toUpperCase() + currentDeal.type.slice(1)}</span>
                </span>
                <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
                  {currentDeal.title}
                </h1>
                <div className="flex items-center">
                  <MapPin className="w-5 h-5 text-white mr-2" />
                  <p className="text-xl text-white">{currentDeal.destination}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="p-6">
          <div className="flex flex-col md:flex-row justify-between mb-6">
            <div className="mb-4 md:mb-0">
              <div className="flex items-center">
                <CalendarDays className="h-5 w-5 text-gray-500 mr-2" />
                <span className="text-gray-700">
                  Valid from <span className="font-medium">{new Date(currentDeal.valid_from).toLocaleDateString()}</span> to <span className="font-medium">{new Date(currentDeal.valid_to).toLocaleDateString()}</span>
                </span>
              </div>
              
              <div className="flex items-center mt-2">
                <Clock className="h-5 w-5 text-gray-500 mr-2" />
                <span className="text-gray-700">
                  Limited time offer - <span className="font-medium text-red-600">Expires in {Math.ceil((new Date(currentDeal.valid_to) - new Date()) / (1000 * 60 * 60 * 24))} days</span>
                </span>
              </div>
            </div>
            
            <div className="flex items-end">
              <div className="flex flex-col items-end">
                <div className="flex items-center">
                  <DollarSign className="h-6 w-6 text-indigo-600" />
                  <span className="text-3xl font-bold text-indigo-600">${currentDeal.price}</span>
                  {currentDeal.original_price && (
                    <span className="ml-2 text-lg text-gray-500 line-through">${currentDeal.original_price}</span>
                  )}
                </div>
                <div className="text-sm text-gray-500 mt-1">per person</div>
              </div>
            </div>
          </div>
          
          <hr className="my-6" />
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="md:col-span-2">
              <h2 className="text-2xl font-semibold mb-4">About this Deal</h2>
              <p className="text-gray-700 mb-6 leading-relaxed">
                {currentDeal.description || 'No detailed description available for this deal.'}
              </p>
              
              <h3 className="text-xl font-semibold mb-3">{'What\'s Included'}</h3>
              <ul className="space-y-2 mb-6">
                {(currentDeal.inclusions || [
                  'Round-trip flights',
                  'Hotel accommodation',
                  'Airport transfers',
                  'Daily breakfast',
                  'City tour'
                ]).map((item, index) => (
                  <li key={index} className="flex items-start">
                    <Check className="h-5 w-5 text-green-500 mr-2 flex-shrink-0" />
                    <span className="text-gray-700">{item}</span>
                  </li>
                ))}
              </ul>
              
              <h3 className="text-xl font-semibold mb-3">Highlights</h3>
              <div className="bg-gray-50 p-4 rounded-lg mb-6">
                <ul className="space-y-2">
                  {(currentDeal.highlights || [
                    'Exclusive discount for limited time',
                    'Flexible booking conditions',
                    'Premium accommodations',
                    'Special activities included'
                  ]).map((highlight, index) => (
                    <li key={index} className="flex items-start">
                      <Star className="h-5 w-5 text-yellow-400 mr-2 flex-shrink-0" />
                      <span className="text-gray-700">{highlight}</span>
                    </li>
                  ))}
                </ul>
              </div>
              
              {currentDeal.terms_conditions && (
                <>
                  <h3 className="text-xl font-semibold mb-3">Terms & Conditions</h3>
                  <p className="text-gray-700 text-sm mb-6 leading-relaxed">
                    {currentDeal.terms_conditions}
                  </p>
                </>
              )}
            </div>
            
            <div>
              <div className="bg-indigo-50 p-6 rounded-lg mb-6">
                <h3 className="text-xl font-semibold mb-4">Book This Deal</h3>
                <p className="text-gray-700 mb-4">
                  Secure this limited-time offer before it expires. Easy booking process with flexible payment options.
                </p>
                <button className="w-full bg-indigo-600 text-white py-3 px-4 rounded-md hover:bg-indigo-700 transition mb-3">
                  Book Now
                </button>
                <button 
                  onClick={handleSaveDeal}
                  className={`w-full py-3 px-4 rounded-md transition border flex justify-center items-center ${
                    isSaved 
                      ? 'bg-gray-100 text-gray-700 border-gray-300' 
                      : 'bg-white text-indigo-600 border-indigo-600 hover:bg-indigo-50'
                  }`}
                  disabled={isSaved}
                >
                  <Bookmark className="h-5 w-5 mr-2" />
                  {isSaved ? 'Saved to My Deals' : 'Save for Later'}
                </button>
                
                <div className="mt-6">
                  <p className="text-sm text-gray-500 mb-3">Share this deal:</p>
                  <div className="flex space-x-3">
                    <button className="text-gray-600 hover:text-indigo-600" aria-label="Share on Twitter">
                      <Share2 className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              </div>
              
              <div className="bg-white border border-gray-200 p-5 rounded-lg">
                <h4 className="font-semibold mb-3">Need Help?</h4>
                <p className="text-gray-600 text-sm mb-3">
                  Have questions about this deal? Our travel experts are here to help.
                </p>
                <a href="tel:+1234567890" className="text-indigo-600 font-medium text-sm hover:text-indigo-800">
                  Call 123-456-7890
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
