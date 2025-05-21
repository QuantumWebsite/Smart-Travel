'use client';

import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchUserTrips, deleteTrip } from '@/lib/redux/slices/tripsSlice';
import Link from 'next/link';
import ProtectedRoute from '@/components/ProtectedRoute';
import { 
  CalendarDays, 
  MapPin, 
  Users, 
  Trash2, 
  PlusCircle, 
  Plane, 
  ArrowRight, 
  Loader2, 
  AlertTriangle 
} from 'lucide-react';

export default function MyTripsPage() {
  const dispatch = useDispatch();
  const { trips, loading, error } = useSelector((state) => state.trips);

  useEffect(() => {
    dispatch(fetchUserTrips());
  }, [dispatch]);
  
  const handleDeleteTrip = (tripId) => {
    if (window.confirm('Are you sure you want to delete this trip?')) {
      dispatch(deleteTrip(tripId));
    }
  };

  return (
    <ProtectedRoute>
      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Trips</h1>
            <p className="mt-2 text-gray-600">
              Plan and manage your upcoming and past travels.
            </p>
          </div>
          <Link
            href="/search"
            className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            <PlusCircle className="h-4 w-4 mr-2" />
            Plan a new trip
          </Link>
        </div>
        
        {loading ? (
          <div className="flex justify-center items-center p-12">
            <Loader2 className="h-10 w-10 text-indigo-600 animate-spin" />
            <span className="ml-3 text-lg text-gray-600">Loading your trips...</span>
          </div>
        ) : error ? (
          <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded">
            <div className="flex">
              <AlertTriangle className="h-5 w-5 text-red-400 mr-2" />
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        ) : trips && trips.length === 0 ? (
          <div className="bg-white shadow rounded-lg overflow-hidden">
            <div className="p-8 text-center">
              <Plane className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-lg font-medium text-gray-900">No trips found</h3>
              <p className="mt-1 text-gray-500">
                {"You haven't planned any trips yet. Start by searching for your next destination."}
              </p>
              <div className="mt-6">
                <Link
                  href="/search"
                  className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
                >
                  Plan a trip
                </Link>
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <ul className="divide-y divide-gray-200">
              {trips.map((trip) => (
                <li key={trip.id}>
                  <div className="px-6 py-5">
                    <div className="flex items-center justify-between">
                      <div className="flex flex-col sm:flex-row sm:items-center">
                        <p className="text-lg font-medium text-indigo-600 truncate">
                          {trip.destination}
                        </p>
                        <div className="sm:ml-2 flex items-center text-sm text-gray-500">
                          <MapPin className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
                          from {trip.departure_location}
                        </div>
                      </div>
                      <div className="ml-2 flex-shrink-0 flex">
                        <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          trip.status === 'upcoming' 
                            ? 'bg-green-100 text-green-800' 
                            : trip.status === 'past' 
                              ? 'bg-gray-100 text-gray-800' 
                              : 'bg-blue-100 text-blue-800'
                        }`}>
                          {trip.status ? trip.status.charAt(0).toUpperCase() + trip.status.slice(1) : 'Planned'}
                        </span>
                      </div>
                    </div>
                    
                    <div className="mt-4 sm:flex sm:justify-between">
                      <div className="sm:flex">
                        <p className="flex items-center text-sm text-gray-500">
                          <CalendarDays className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
                          {new Date(trip.departure_date).toLocaleDateString()} - {new Date(trip.return_date).toLocaleDateString()}
                        </p>
                        <p className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0 sm:ml-6">
                          <Users className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
                          {trip.adults + (trip.children || 0)} {trip.adults + (trip.children || 0) === 1 ? 'traveler' : 'travelers'}
                        </p>
                      </div>
                    </div>
                    
                    <div className="mt-4 flex justify-end space-x-3">
                      <Link
                        href={`/my-trips/${trip.id}`}
                        className="inline-flex items-center px-3 py-2 border border-transparent text-sm rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200"
                      >
                        View Details
                        <ArrowRight className="ml-1 h-4 w-4" />
                      </Link>
                      <button
                        onClick={() => handleDeleteTrip(trip.id)}
                        className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm rounded-md text-gray-700 bg-white hover:bg-gray-50"
                      >
                        <Trash2 className="mr-1 h-4 w-4 text-gray-500" />
                        Delete
                      </button>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
