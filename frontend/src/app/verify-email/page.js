'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { useDispatch, useSelector } from 'react-redux';
import { verifyEmail } from '@/lib/redux/slices/authSlice';
import { CheckCircle, AlertTriangle, Loader2 } from 'lucide-react';

export default function VerifyEmail() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const dispatch = useDispatch();
  const token = searchParams.get('token');
  
  const { loading, verificationStatus, verificationMessage } = useSelector((state) => state.auth);

  useEffect(() => {
    if (!token) {
      // Set error directly in component since we don't have a token to dispatch an action
      return;
    }

    // Use the Redux action to verify email
    dispatch(verifyEmail(token));
  }, [token, dispatch]);
  const renderContent = () => {
    if (loading || verificationStatus === 'pending') {
      return (
        <div className="flex items-center justify-center">
          <Loader2 className="h-8 w-8 text-indigo-500 animate-spin mr-2" />
          <p>Verifying your email address...</p>
        </div>
      );
    }
    
    if (verificationStatus === 'success') {
      return (
        <>
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
            <CheckCircle className="h-6 w-6 text-green-600" aria-hidden="true" />
          </div>
          <h2 className="mt-6 text-center text-2xl font-bold tracking-tight text-gray-900">
            Email Verified!
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">{verificationMessage}</p>
          <div className="mt-8">
            <Link
              href="/login?verification=success"
              className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              Sign in
            </Link>
          </div>
        </>
      );
    }
    
    if (verificationStatus === 'error' || !token) {
      const displayMessage = !token 
        ? 'Invalid verification link. No token provided.' 
        : verificationMessage;
        
      return (
        <>
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-red-100">
            <AlertTriangle className="h-6 w-6 text-red-600" aria-hidden="true" />
          </div>
          <h2 className="mt-6 text-center text-2xl font-bold tracking-tight text-gray-900">
            Verification Failed
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">{displayMessage}</p>
          <div className="mt-8 space-y-4">
            <Link
              href="/login"
              className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              Return to Sign In
            </Link>
            <button
              onClick={() => router.push('/resend-verification')}
              className="flex w-full justify-center rounded-md bg-white px-3 py-1.5 text-sm font-semibold leading-6 text-indigo-600 shadow-sm border border-indigo-300 hover:bg-gray-50"
            >
              Resend Verification Email
            </button>
          </div>
        </>
      );
    }
    
    // Default loading state if nothing else matches
    return (
      <div className="flex items-center justify-center">
        <Loader2 className="h-8 w-8 text-indigo-500 animate-spin mr-2" />
        <p>Loading...</p>
      </div>
    );
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
          Email Verification
        </h2>
      </div>

      <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-[480px]">
        <div className="bg-white px-6 py-12 shadow sm:rounded-lg sm:px-12">
          {renderContent()}
        </div>
      </div>
    </div>
  );
}
