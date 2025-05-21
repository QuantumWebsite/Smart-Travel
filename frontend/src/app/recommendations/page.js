'use client';

import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchRecommendations, fetchPersonalizedRecommendations } from '@/lib/redux/slices/recommendationsSlice';
import Link from 'next/link';
import { 
  MapPin, 
  Calendar, 
  TrendingUp, 
  ThumbsUp, 
  Tag, 
  Loader2, 
  AlertTriangle
} from 'lucide-react';

export default function RecommendationsPage() {
  const dispatch = useDispatch();
  const { recommendations, loading, error } = useSelector((state) => state.recommendations);
  const [preferences, setPreferences] = useState({
    budget: 'medium',
    climate: 'warm',
    activityType: 'cultural',
    travelStyle: 'relaxed'
  });

  useEffect(() => {
    dispatch(fetchRecommendations());
  }, [dispatch]);

  const handlePreferenceChange = (e) => {
    setPreferences({
      ...preferences,
      [e.target.name]: e.target.value
    });
  };

  const handleGetPersonalized = () => {
    dispatch(fetchPersonalizedRecommendations(preferences));
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <Loader2 className="w-12 h-12 text-indigo-600 animate-spin" />
        <p className="mt-4 text-lg text-gray-600">Loading recommendations...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <AlertTriangle className="w-12 h-12 text-red-600" />
        <p className="mt-4 text-lg text-gray-600">Error: {error}</p>
        <button 
          onClick={() => dispatch(fetchRecommendations())} 
          className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Travel Recommendations</h1>
      
      {/* Preferences Section */}
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-xl font-semibold mb-4">Personalize Your Recommendations</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Budget</label>
            <select 
              name="budget" 
              value={preferences.budget}
              onChange={handlePreferenceChange}
              className="w-full border border-gray-300 rounded-md py-2 px-3"
            >
              <option value="low">Budget-Friendly</option>
              <option value="medium">Mid-Range</option>
              <option value="high">Luxury</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Climate</label>
            <select 
              name="climate" 
              value={preferences.climate}
              onChange={handlePreferenceChange}
              className="w-full border border-gray-300 rounded-md py-2 px-3"
            >
              <option value="warm">Warm</option>
              <option value="cold">Cold</option>
              <option value="tropical">Tropical</option>
              <option value="temperate">Temperate</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Activity Type</label>
            <select 
              name="activityType" 
              value={preferences.activityType}
              onChange={handlePreferenceChange}
              className="w-full border border-gray-300 rounded-md py-2 px-3"
            >
              <option value="cultural">Cultural</option>
              <option value="adventure">Adventure</option>
              <option value="relaxation">Relaxation</option>
              <option value="nature">Nature</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Travel Style</label>
            <select 
              name="travelStyle" 
              value={preferences.travelStyle}
              onChange={handlePreferenceChange}
              className="w-full border border-gray-300 rounded-md py-2 px-3"
            >
              <option value="relaxed">Relaxed</option>
              <option value="packed">Packed Itinerary</option>
              <option value="spontaneous">Spontaneous</option>
              <option value="planned">Planned</option>
            </select>
          </div>
        </div>
        <button 
          onClick={handleGetPersonalized}
          className="mt-4 bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition-colors"
        >
          Get Personalized Recommendations
        </button>
      </div>
      
      {/* Recommendations Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {recommendations && recommendations.map((recommendation) => (
          <div key={recommendation.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
            <div className="h-48 bg-gray-200 relative">
              {/* If you have images, you can add them here */}
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
              <div className="absolute bottom-0 left-0 p-4">
                <h3 className="text-xl font-bold text-white">{recommendation.destination}</h3>
                <div className="flex items-center mt-1">
                  <MapPin className="w-4 h-4 text-white mr-1" />
                  <p className="text-sm text-white">{recommendation.country}</p>
                </div>
              </div>
            </div>
            <div className="p-4">
              <div className="flex justify-between items-center mb-3">
                <div className="flex items-center">
                  <Calendar className="w-4 h-4 text-gray-500 mr-1" />
                  <span className="text-sm text-gray-500">
                    {recommendation.best_time_to_visit || 'Year-round'}
                  </span>
                </div>
                <div className="flex items-center">
                  <Tag className="w-4 h-4 text-gray-500 mr-1" />
                  <span className="text-sm text-gray-500">
                    ${recommendation.average_cost || 'Varies'}
                  </span>
                </div>
              </div>
              <p className="text-gray-600 mb-4 line-clamp-3">{recommendation.description}</p>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <ThumbsUp className="w-4 h-4 text-indigo-600 mr-1" />
                  <span className="text-sm text-gray-600">{recommendation.rating || '4.5'}/5</span>
                </div>
                <Link
                  href={`/recommendations/${recommendation.id}`}
                  className="text-indigo-600 hover:text-indigo-800 text-sm font-medium"
                >
                  Explore More
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {recommendations && recommendations.length === 0 && (
        <div className="text-center py-12">
          <TrendingUp className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900">No recommendations found</h3>
          <p className="mt-2 text-gray-500">Try adjusting your preferences or check back later.</p>
        </div>
      )}
    </div>
  );
}
