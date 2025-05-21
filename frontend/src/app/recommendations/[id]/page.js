'use client';

import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchRecommendationById, fetchPackingSuggestions } from '@/lib/redux/slices/recommendationsSlice';
import { 
  MapPin, 
  Calendar, 
  Tag, 
  ThumbsUp, 
  ArrowLeft, 
  Umbrella, 
  Sun, 
  Wind, 
  Backpack, 
  Clock, 
  Loader2, 
  AlertTriangle 
} from 'lucide-react';
import Link from 'next/link';

export default function RecommendationDetail({ params }) {
  const dispatch = useDispatch();
  const { currentRecommendation, packingSuggestions, loading, error } = useSelector(
    (state) => state.recommendations
  );
  const recommendationId = params.id;

  useEffect(() => {
    if (recommendationId) {
      dispatch(fetchRecommendationById(recommendationId));
      dispatch(fetchPackingSuggestions(recommendationId));
    }
  }, [dispatch, recommendationId]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <Loader2 className="w-12 h-12 text-indigo-600 animate-spin" />
        <p className="mt-4 text-lg text-gray-600">Loading recommendation details...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <AlertTriangle className="w-12 h-12 text-red-600" />
        <p className="mt-4 text-lg text-gray-600">Error: {error}</p>
        <Link
          href="/recommendations"
          className="mt-4 inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Recommendations
        </Link>
      </div>
    );
  }

  if (!currentRecommendation) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-12">
          <AlertTriangle className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900">Recommendation not found</h3>
          <Link
            href="/recommendations"
            className="mt-4 inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Recommendations
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <Link
          href="/recommendations"
          className="inline-flex items-center text-indigo-600 hover:text-indigo-800"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Recommendations
        </Link>
      </div>

      {/* Hero Section */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden mb-8">
        <div className="h-64 md:h-96 bg-gray-200 relative">
          {/* If you have an image for the recommendation */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
          <div className="absolute bottom-0 left-0 p-6 w-full">
            <div className="flex flex-col md:flex-row md:justify-between md:items-end">
              <div>
                <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
                  {currentRecommendation.destination}
                </h1>
                <div className="flex items-center">
                  <MapPin className="w-5 h-5 text-white mr-2" />
                  <p className="text-xl text-white">{currentRecommendation.country}</p>
                </div>
              </div>
              <div className="mt-4 md:mt-0 flex items-center bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full">
                <ThumbsUp className="w-5 h-5 text-white mr-2" />
                <span className="text-white font-medium">
                  {currentRecommendation.rating || '4.5'}/5 Rating
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Details Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-2xl font-semibold mb-4">About {currentRecommendation.destination}</h2>
            <p className="text-gray-700 mb-6 leading-relaxed">
              {currentRecommendation.description || 
                `${currentRecommendation.destination} is a beautiful destination known for its unique 
                blend of culture, cuisine, and natural landscapes. Visitors can explore historical 
                sites, enjoy local delicacies, and experience the warm hospitality of the locals.`}
            </p>

            {/* Highlights */}
            <h3 className="text-xl font-semibold mb-3">Highlights</h3>
            <ul className="space-y-2 mb-6">
              {(currentRecommendation.highlights || [
                'Iconic landmarks and historical sites',
                'Vibrant local markets and shopping districts',
                'Beautiful natural landscapes and outdoor activities',
                'Rich cultural experiences and traditions',
                'Delicious local cuisine and dining options'
              ]).map((highlight, index) => (
                <li key={index} className="flex items-start">
                  <span className="inline-flex items-center justify-center h-6 w-6 rounded-full bg-indigo-100 text-indigo-800 mr-3 flex-shrink-0">
                    {index + 1}
                  </span>
                  <span className="text-gray-700">{highlight}</span>
                </li>
              ))}
            </ul>

            {/* Best Time To Visit */}
            <h3 className="text-xl font-semibold mb-3">Best Time to Visit</h3>
            <div className="bg-indigo-50 p-4 rounded-lg mb-6">
              <div className="flex items-start">
                <Calendar className="w-5 h-5 text-indigo-600 mr-3 mt-1" />
                <div>
                  <p className="text-gray-700">
                    {currentRecommendation.best_time_to_visit || 'Year-round destination with peak seasons during summer (June-August) and holiday periods. Spring (April-May) and fall (September-October) offer pleasant weather with fewer crowds.'}
                  </p>
                </div>
              </div>
            </div>

            {/* Weather Info */}
            <h3 className="text-xl font-semibold mb-3">Weather Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-blue-50 p-4 rounded-lg flex items-center">
                <Umbrella className="w-5 h-5 text-blue-600 mr-3" />
                <div>
                  <p className="text-sm text-gray-500">Precipitation</p>
                  <p className="font-medium">
                    {currentRecommendation.precipitation || 'Moderate'}
                  </p>
                </div>
              </div>
              <div className="bg-yellow-50 p-4 rounded-lg flex items-center">
                <Sun className="w-5 h-5 text-yellow-600 mr-3" />
                <div>
                  <p className="text-sm text-gray-500">Temperature</p>
                  <p className="font-medium">
                    {currentRecommendation.temperature || '15°C - 28°C'}
                  </p>
                </div>
              </div>
              <div className="bg-indigo-50 p-4 rounded-lg flex items-center">
                <Wind className="w-5 h-5 text-indigo-600 mr-3" />
                <div>
                  <p className="text-sm text-gray-500">Climate</p>
                  <p className="font-medium">
                    {currentRecommendation.climate || 'Temperate'}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div>
          {/* Quick Info Card */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h3 className="text-xl font-semibold mb-4">Quick Information</h3>
            
            <div className="space-y-4">
              <div className="flex items-start">
                <Tag className="w-5 h-5 text-gray-500 mr-3 mt-1" />
                <div>
                  <p className="text-sm text-gray-500">Average Cost</p>
                  <p className="font-medium">
                    ${currentRecommendation.average_cost || '100-150'}/day
                  </p>
                </div>
              </div>
              
              <div className="flex items-start">
                <Clock className="w-5 h-5 text-gray-500 mr-3 mt-1" />
                <div>
                  <p className="text-sm text-gray-500">Recommended Duration</p>
                  <p className="font-medium">
                    {currentRecommendation.recommended_duration || '5-7 days'}
                  </p>
                </div>
              </div>
              
              <div className="border-t border-gray-200 my-4"></div>
              
              <button className="w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700 transition">
                Save to My Trips
              </button>
            </div>
          </div>

          {/* Packing Suggestions */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center mb-4">
              <Backpack className="w-5 h-5 text-indigo-600 mr-2" />
              <h3 className="text-xl font-semibold">Packing Suggestions</h3>
            </div>
            
            {packingSuggestions && packingSuggestions.length > 0 ? (
              <ul className="space-y-2">
                {packingSuggestions.map((item, index) => (
                  <li key={index} className="flex items-center">
                    <span className="inline-block w-2 h-2 rounded-full bg-indigo-600 mr-2"></span>
                    <span className="text-gray-700">{item.item}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="text-gray-500">
                <p>Packing suggestions will be personalized based on your travel dates and destination weather.</p>
                <ul className="mt-3 space-y-2">
                  <li className="flex items-center">
                    <span className="inline-block w-2 h-2 rounded-full bg-indigo-600 mr-2"></span>
                    <span>Weather-appropriate clothing</span>
                  </li>
                  <li className="flex items-center">
                    <span className="inline-block w-2 h-2 rounded-full bg-indigo-600 mr-2"></span>
                    <span>Travel adapters</span>
                  </li>
                  <li className="flex items-center">
                    <span className="inline-block w-2 h-2 rounded-full bg-indigo-600 mr-2"></span>
                    <span>Comfortable walking shoes</span>
                  </li>
                </ul>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
