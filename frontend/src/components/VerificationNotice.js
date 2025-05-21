'use client';

import { AlertTriangle, CheckCircle } from 'lucide-react';

export default function VerificationNotice({ type, message }) {
  if (!message) return null;

  return (
    <div className={`rounded-md p-4 mb-6 ${
      type === 'success' ? 'bg-green-50' : 'bg-yellow-50'
    }`}>
      <div className="flex">
        <div className="flex-shrink-0">
          {type === 'success' ? (
            <CheckCircle className="h-5 w-5 text-green-400" aria-hidden="true" />
          ) : (
            <AlertTriangle className="h-5 w-5 text-yellow-400" aria-hidden="true" />
          )}
        </div>
        <div className="ml-3">
          <h3 className={`text-sm font-medium ${
            type === 'success' ? 'text-green-800' : 'text-yellow-800'
          }`}>
            {message}
          </h3>
        </div>
      </div>
    </div>
  );
}
