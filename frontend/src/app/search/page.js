'use client';

import SearchForm from '@/components/SearchForm';

export default function SearchPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Plan Your Perfect Trip</h1>
        <p className="mt-2 text-gray-600">
          Let us help you find the best flights, hotels, and activities for your next adventure.
        </p>
      </div>
      
      <SearchForm />
      
      <div className="mt-12">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">How it works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
              <span className="text-indigo-600 font-bold text-xl">1</span>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Tell us your travel plans</h3>
            <p className="text-gray-600">
              Enter your destination, travel dates, and preferences to get started.
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
              <span className="text-indigo-600 font-bold text-xl">2</span>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Review personalized recommendations</h3>
            <p className="text-gray-600">
              Our AI analyzes thousands of options to find the best matches for you.
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
              <span className="text-indigo-600 font-bold text-xl">3</span>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Book with confidence</h3>
            <p className="text-gray-600">
              Save your favorite deals and book when you're ready, all in one place.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
