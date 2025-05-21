'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useDispatch, useSelector } from 'react-redux';
import { logoutUser } from '@/lib/redux/slices/authSlice';
import { userAPI } from '@/lib/api';

export default function ProfilePage() {
  const { user } = useSelector(state => state.auth);
  const dispatch = useDispatch();
  const router = useRouter();
  
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    current_password: '',
    new_password: '',
    confirm_password: '',
  });
  
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });
  useEffect(() => {
    if (user) {
      setFormData(prevData => ({
        ...prevData,
        full_name: user.full_name || '',
        email: user.email || '',
      }));
    }
  }, [user]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage({ text: '', type: '' });

    try {
      await userAPI.updateCurrentUser({
        full_name: formData.full_name,
        email: formData.email,
      });
      
      setMessage({
        text: 'Profile updated successfully',
        type: 'success',
      });
    } catch (error) {
      console.error('Profile update error:', error);
      setMessage({
        text: error.response?.data?.detail || 'Failed to update profile',
        type: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    
    if (formData.new_password !== formData.confirm_password) {
      setMessage({
        text: 'New passwords do not match',
        type: 'error',
      });
      return;
    }
    
    setIsLoading(true);
    setMessage({ text: '', type: '' });

    try {
      await userAPI.updateCurrentUser({
        password: formData.new_password,
        current_password: formData.current_password,
      });
      
      setMessage({
        text: 'Password updated successfully',
        type: 'success',
      });
      
      // Clear password fields
      setFormData({
        ...formData,
        current_password: '',
        new_password: '',
        confirm_password: '',
      });
    } catch (error) {
      console.error('Password update error:', error);
      setMessage({
        text: error.response?.data?.detail || 'Failed to update password',
        type: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };
  const handleDeleteAccount = async () => {
    if (window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      setIsLoading(true);
      
      try {
        // Implementation for account deletion would be added here
        // For now, just log out the user
        dispatch(logoutUser());
        router.push('/');
      } catch (error) {
        console.error('Account deletion error:', error);
        setMessage({
          text: error.response?.data?.detail || 'Failed to delete account',
          type: 'error',
        });
        setIsLoading(false);
      }
    }
  };

  if (!user) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="text-center">
          <p className="text-gray-600">Please log in to view your profile.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <div className="md:grid md:grid-cols-3 md:gap-6">
        <div className="md:col-span-1">
          <div className="px-4 sm:px-0">
            <h3 className="text-lg font-medium leading-6 text-gray-900">Profile</h3>
            <p className="mt-1 text-sm text-gray-600">
              Manage your account settings and preferences.
            </p>
          </div>
        </div>
        
        <div className="mt-5 md:mt-0 md:col-span-2">
          {message.text && (
            <div className={`mb-4 p-4 rounded-md ${message.type === 'success' ? 'bg-green-50' : 'bg-red-50'}`}>
              <p className={`text-sm ${message.type === 'success' ? 'text-green-700' : 'text-red-700'}`}>
                {message.text}
              </p>
            </div>
          )}
          
          <div className="shadow sm:rounded-md sm:overflow-hidden">
            <div className="px-4 py-5 bg-white space-y-6 sm:p-6">
              <div>
                <h2 className="text-xl font-medium text-gray-900">Personal Information</h2>
                <p className="mt-1 text-sm text-gray-500">
                  Update your basic profile information.
                </p>
              </div>
              
              <form onSubmit={handleProfileUpdate}>
                <div className="grid grid-cols-6 gap-6">
                  <div className="col-span-6 sm:col-span-4">
                    <label htmlFor="full_name" className="block text-sm font-medium text-gray-700">
                      Full name
                    </label>
                    <input
                      type="text"
                      name="full_name"
                      id="full_name"
                      value={formData.full_name}
                      onChange={handleChange}
                      className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    />
                  </div>

                  <div className="col-span-6 sm:col-span-4">
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                      Email address
                    </label>
                    <input
                      type="email"
                      name="email"
                      id="email"
                      value={formData.email}
                      onChange={handleChange}
                      className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    />
                  </div>
                </div>
                
                <div className="mt-6">
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                  >
                    {isLoading ? 'Saving...' : 'Save'}
                  </button>
                </div>
              </form>
            </div>
          </div>
          
          <div className="shadow sm:rounded-md sm:overflow-hidden mt-8">
            <div className="px-4 py-5 bg-white space-y-6 sm:p-6">
              <div>
                <h2 className="text-xl font-medium text-gray-900">Change Password</h2>
                <p className="mt-1 text-sm text-gray-500">
                  Update your password to keep your account secure.
                </p>
              </div>
              
              <form onSubmit={handlePasswordChange}>
                <div className="grid grid-cols-6 gap-6">
                  <div className="col-span-6 sm:col-span-4">
                    <label htmlFor="current_password" className="block text-sm font-medium text-gray-700">
                      Current password
                    </label>
                    <input
                      type="password"
                      name="current_password"
                      id="current_password"
                      value={formData.current_password}
                      onChange={handleChange}
                      required
                      className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    />
                  </div>

                  <div className="col-span-6 sm:col-span-4">
                    <label htmlFor="new_password" className="block text-sm font-medium text-gray-700">
                      New password
                    </label>
                    <input
                      type="password"
                      name="new_password"
                      id="new_password"
                      value={formData.new_password}
                      onChange={handleChange}
                      required
                      className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    />
                  </div>
                  
                  <div className="col-span-6 sm:col-span-4">
                    <label htmlFor="confirm_password" className="block text-sm font-medium text-gray-700">
                      Confirm new password
                    </label>
                    <input
                      type="password"
                      name="confirm_password"
                      id="confirm_password"
                      value={formData.confirm_password}
                      onChange={handleChange}
                      required
                      className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    />
                  </div>
                </div>
                
                <div className="mt-6">
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                  >
                    {isLoading ? 'Updating...' : 'Update Password'}
                  </button>
                </div>
              </form>
            </div>
          </div>
          
          <div className="shadow sm:rounded-md sm:overflow-hidden mt-8">
            <div className="px-4 py-5 bg-white space-y-6 sm:p-6">
              <div>
                <h2 className="text-xl font-medium text-gray-900">Danger Zone</h2>
                <p className="mt-1 text-sm text-gray-500">
                  Permanent actions that cannot be undone.
                </p>
              </div>
              
              <div className="border border-red-200 rounded-md p-4">
                <h3 className="text-lg font-medium text-gray-900">Delete Account</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Permanently delete your account and all your data. This action cannot be undone.
                </p>
                <div className="mt-4">
                  <button
                    type="button"
                    onClick={handleDeleteAccount}
                    disabled={isLoading}
                    className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
                  >
                    Delete Account
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
