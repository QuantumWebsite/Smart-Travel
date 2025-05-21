'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import { useDispatch, useSelector } from 'react-redux';
import { resendVerificationEmail, clearVerificationStatus } from '@/lib/redux/slices/authSlice';
import { AlertCircle, Loader2 } from 'lucide-react';

export default function ResendVerification() {
  const [email, setEmail] = useState('');
  const router = useRouter();
  const dispatch = useDispatch();
  const { loading, verificationStatus, verificationMessage, error } = useSelector((state) => state.auth);

  useEffect(() => {
    // Clear any previous verification status when component mounts
    dispatch(clearVerificationStatus());
  }, [dispatch]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    dispatch(resendVerificationEmail(email));
  };

  return (
    <div className="flex min-h-full flex-1 flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="mx-auto flex justify-center">
          <Image
            className="h-10 w-auto"
            src="/globe.svg"
            alt="Smart Travel"
            width={40}
            height={40}
          />
        </div>
        <h2 className="mt-6 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
          Resend Verification Email
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Enter your email address below to receive a new verification link.
        </p>
      </div>      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-[480px]">
        <div className="bg-white px-6 py-12 shadow sm:rounded-lg sm:px-12">
          {verificationStatus === 'success' ? (
            <div>
              <div className="rounded-md bg-green-50 p-4">
                <div className="flex">
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-green-800">
                      Verification email sent!
                    </h3>
                    <div className="mt-2 text-sm text-green-700">
                      <p>
                        {verificationMessage || 'Please check your email for the verification link. If you don\'t see it in your inbox, please check your spam folder.'}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              <div className="mt-6">
                <Link
                  href="/login"
                  className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                >
                  Return to Login
                </Link>
              </div>
            </div>
          ) : (
            <form className="space-y-6" onSubmit={handleSubmit}>
              {error && (
                <div className="rounded-md bg-red-50 p-4">
                  <div className="flex">
                    <AlertCircle className="h-5 w-5 text-red-400" aria-hidden="true" />
                    <div className="ml-3">
                      <h3 className="text-sm font-medium text-red-800">{error}</h3>
                    </div>
                  </div>
                </div>
              )}

              <div>
                <label htmlFor="email" className="block text-sm font-medium leading-6 text-gray-900">
                  Email address
                </label>
                <div className="mt-2">
                  <input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                  />
                </div>
              </div>

              <div>
                <button
                  type="submit"
                  disabled={loading}
                  className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <span className="flex items-center">
                      <Loader2 className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" />
                      Sending...
                    </span>
                  ) : (
                    'Send Verification Email'
                  )}
                </button>
              </div>

              <div>
                <Link 
                  href="/login" 
                  className="block text-center text-sm font-medium text-indigo-600 hover:text-indigo-500"
                >
                  Back to login
                </Link>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
