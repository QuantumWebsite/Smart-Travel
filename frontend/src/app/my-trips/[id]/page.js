'use client';

import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { updateTrip } from '@/lib/redux/slices/tripsSlice';
import Link from 'next/link';
import ProtectedRoute from '@/components/ProtectedRoute';
import { 
  Calendar, 
  MapPin, 
  Users, 
  ArrowLeft, 
  Edit2, 
  Save, 
  X, 
  Plane, 
  Hotel, 
  Luggage, 
  Clock, 
  DollarSign, 
  Loader2, 
  AlertTriangle 
} from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function TripDetailPage({ params }) {
  const router = useRouter();
  const dispatch = useDispatch();
  const { trips, loading, error } = useSelector((state) => state.trips);
  const tripId = params.id;
  
  const [trip, setTrip] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    destination: '',
    departure_location: '',
    departure_date: '',
    return_date: '',
    adults: 1,
    children: 0,
    notes: '',
    budget: ''
  });
  
  useEffect(() => {
    if (trips.length > 0) {
      const foundTrip = trips.find(t => t.id.toString() === tripId);
      if (foundTrip) {
        setTrip(foundTrip);
        setFormData({
          destination: foundTrip.destination || '',
          departure_location: foundTrip.departure_location || '',
          departure_date: foundTrip.departure_date ? new Date(foundTrip.departure_date).toISOString().split('T')[0] : '',
          return_date: foundTrip.return_date ? new Date(foundTrip.return_date).toISOString().split('T')[0] : '',
          adults: foundTrip.adults || 1,
          children: foundTrip.children || 0,
          notes: foundTrip.notes || '',
          budget: foundTrip.budget || ''
        });
      }
    }
  }, [trips, tripId]);
  
  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'number' ? parseInt(value) : value
    });
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    dispatch(updateTrip({ tripId, tripData: formData }))
      .unwrap()
      .then(() => {
        setIsEditing(false);
      })
      .catch(error => {
        console.error('Error updating trip:', error);
      });
  };
  
  const calculateTripDuration = () => {
    if (!trip?.departure_date || !trip?.return_date) return '0 days';
    
    const start = new Date(trip.departure_date);
    const end = new Date(trip.return_date);
    const diffTime = Math.abs(end - start);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    return `${diffDays} ${diffDays === 1 ? 'day' : 'days'}`;
  };
  
  if (loading) {
    return (
      <ProtectedRoute>
        <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
          <div className="flex justify-center items-center p-12">
            <Loader2 className="h-10 w-10 text-indigo-600 animate-spin" />
            <span className="ml-3 text-lg text-gray-600">Loading trip details...</span>
          </div>
        </div>
      </ProtectedRoute>
    );
  }
  
  if (error) {
    return (
      <ProtectedRoute>
        <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
          <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded">
            <div className="flex">
              <AlertTriangle className="h-5 w-5 text-red-400 mr-2" />
              <p className="text-sm text-red-700">{error}</p>
            </div>
            <Link
              href="/my-trips"
              className="mt-4 inline-flex items-center text-indigo-600 hover:text-indigo-800"
            >
              <ArrowLeft className="h-4 w-4 mr-1" />
              Back to My Trips
            </Link>
          </div>
        </div>
      </ProtectedRoute>
    );
  }
  
  if (!trip) {
    return (
      <ProtectedRoute>
        <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <AlertTriangle className="mx-auto h-12 w-12 text-yellow-500" />
            <h3 className="mt-2 text-lg font-medium text-gray-900">Trip not found</h3>
            <p className="mt-1 text-gray-500">
              {"We couldn't find the trip you're looking for."}
            </p>
            <div className="mt-6">
              <Link
                href="/my-trips"
                className="inline-flex items-center text-indigo-600 hover:text-indigo-800"
              >
                <ArrowLeft className="h-4 w-4 mr-1" />
                Back to My Trips
              </Link>
            </div>
          </div>
        </div>
      </ProtectedRoute>
    );
  }
  
  return (
    <ProtectedRoute>
      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-6">
          <Link
            href="/my-trips"
            className="inline-flex items-center text-indigo-600 hover:text-indigo-800"
          >
            <ArrowLeft className="h-4 w-4 mr-1" />
            Back to My Trips
          </Link>
        </div>
        
        {isEditing ? (
          <div className="bg-white shadow overflow-hidden sm:rounded-md p-6">
            <div className="flex justify-between items-center mb-6">
              <h1 className="text-2xl font-bold text-gray-900">Edit Trip</h1>
              <button
                onClick={() => setIsEditing(false)}
                className="inline-flex items-center text-gray-500 hover:text-gray-700"
              >
                <X className="h-5 w-5" />
                <span className="ml-1">Cancel</span>
              </button>
            </div>
            
            <form onSubmit={handleSubmit}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Destination</label>
                  <input
                    type="text"
                    name="destination"
                    value={formData.destination}
                    onChange={handleChange}
                    required
                    className="w-full border border-gray-300 rounded-md py-2 px-3"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Departure Location</label>
                  <input
                    type="text"
                    name="departure_location"
                    value={formData.departure_location}
                    onChange={handleChange}
                    required
                    className="w-full border border-gray-300 rounded-md py-2 px-3"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Departure Date</label>
                  <input
                    type="date"
                    name="departure_date"
                    value={formData.departure_date}
                    onChange={handleChange}
                    required
                    className="w-full border border-gray-300 rounded-md py-2 px-3"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Return Date</label>
                  <input
                    type="date"
                    name="return_date"
                    value={formData.return_date}
                    onChange={handleChange}
                    required
                    className="w-full border border-gray-300 rounded-md py-2 px-3"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Adults</label>
                  <input
                    type="number"
                    name="adults"
                    min="1"
                    value={formData.adults}
                    onChange={handleChange}
                    required
                    className="w-full border border-gray-300 rounded-md py-2 px-3"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Children</label>
                  <input
                    type="number"
                    name="children"
                    min="0"
                    value={formData.children}
                    onChange={handleChange}
                    className="w-full border border-gray-300 rounded-md py-2 px-3"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Budget (USD)</label>
                  <input
                    type="text"
                    name="budget"
                    value={formData.budget}
                    onChange={handleChange}
                    placeholder="e.g. 2000"
                    className="w-full border border-gray-300 rounded-md py-2 px-3"
                  />
                </div>
                
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">Notes</label>
                  <textarea
                    name="notes"
                    value={formData.notes}
                    onChange={handleChange}
                    rows="4"
                    className="w-full border border-gray-300 rounded-md py-2 px-3"
                    placeholder="Add any additional notes or plans for your trip"
                  ></textarea>
                </div>
              </div>
              
              <div className="mt-6 flex justify-end">
                <button
                  type="submit"
                  className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
                >
                  <Save className="h-4 w-4 mr-2" />
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        ) : (
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{trip.destination}</h1>
                <div className="mt-1 flex items-center text-sm text-gray-500">
                  <MapPin className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
                  From {trip.departure_location}
                </div>
              </div>
              <button
                onClick={() => setIsEditing(true)}
                className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                <Edit2 className="mr-1 h-4 w-4" />
                Edit Trip
              </button>
            </div>
            
            <div className="border-t border-gray-200">
              <dl>
                <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500 flex items-center">
                    <Calendar className="h-5 w-5 mr-2 text-indigo-500" />
                    Trip Dates
                  </dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
                    {new Date(trip.departure_date).toLocaleDateString()} - {new Date(trip.return_date).toLocaleDateString()}
                  </dd>
                </div>
                
                <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500 flex items-center">
                    <Clock className="h-5 w-5 mr-2 text-indigo-500" />
                    Duration
                  </dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
                    {calculateTripDuration()}
                  </dd>
                </div>
                
                <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500 flex items-center">
                    <Users className="h-5 w-5 mr-2 text-indigo-500" />
                    Travelers
                  </dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
                    {trip.adults} {trip.adults === 1 ? 'adult' : 'adults'}
                    {trip.children > 0 && `, ${trip.children} ${trip.children === 1 ? 'child' : 'children'}`}
                  </dd>
                </div>
                
                {trip.budget && (
                  <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500 flex items-center">
                      <DollarSign className="h-5 w-5 mr-2 text-indigo-500" />
                      Budget
                    </dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
                      ${trip.budget}
                    </dd>
                  </div>
                )}
                
                {trip.notes && (
                  <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Notes</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:col-span-2 sm:mt-0">
                      {trip.notes}
                    </dd>
                  </div>
                )}
              </dl>
            </div>
            
            <div className="px-4 py-5 sm:px-6 border-t border-gray-200">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Trip Planning</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-indigo-50 p-4 rounded-lg flex flex-col items-center">
                  <Plane className="h-10 w-10 text-indigo-500 mb-3" />
                  <h4 className="font-medium text-gray-900 mb-1">Flights</h4>
                  <p className="text-sm text-gray-600 text-center">Find the best flight options for your trip.</p>
                  <Link
                    href={`/search?destination=${encodeURIComponent(trip.destination)}&departure_location=${encodeURIComponent(trip.departure_location)}&departure_date=${trip.departure_date}&return_date=${trip.return_date}&adults=${trip.adults}&children=${trip.children || 0}`}
                    className="mt-4 text-sm text-indigo-600 hover:text-indigo-800"
                  >
                    Search Flights →
                  </Link>
                </div>
                
                <div className="bg-indigo-50 p-4 rounded-lg flex flex-col items-center">
                  <Hotel className="h-10 w-10 text-indigo-500 mb-3" />
                  <h4 className="font-medium text-gray-900 mb-1">Accommodations</h4>
                  <p className="text-sm text-gray-600 text-center">Find hotels and accommodations for your stay.</p>
                  <Link
                    href={`/search?destination=${encodeURIComponent(trip.destination)}&arrival_date=${trip.departure_date}&departure_date=${trip.return_date}&guests=${trip.adults + (trip.children || 0)}`}
                    className="mt-4 text-sm text-indigo-600 hover:text-indigo-800"
                  >
                    Browse Hotels →
                  </Link>
                </div>
                
                <div className="bg-indigo-50 p-4 rounded-lg flex flex-col items-center">
                  <Luggage className="h-10 w-10 text-indigo-500 mb-3" />
                  <h4 className="font-medium text-gray-900 mb-1">Packing List</h4>
                  <p className="text-sm text-gray-600 text-center">Get personalized packing suggestions.</p>
                  <Link
                    href={`/recommendations?destination=${encodeURIComponent(trip.destination)}&departure_date=${trip.departure_date}&return_date=${trip.return_date}`}
                    className="mt-4 text-sm text-indigo-600 hover:text-indigo-800"
                  >
                    Get Suggestions →
                  </Link>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
