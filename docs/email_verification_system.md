# Email Verification System Documentation

This document provides an overview of the email verification system implemented in the Smart Travel application.

## Overview

The email verification system ensures that users provide valid email addresses during registration. It improves security and reduces spam by requiring users to verify their email addresses before they can fully use the application.

## Features

- User registration with automatic verification email
- Verification token generation and validation
- Email verification endpoint
- Token expiration (24 hours)
- Option to resend verification emails
- Prevention of login until email is verified

## Implementation Details

### Database Schema (User Model)

The User model includes the following fields for email verification:

- `email_verified`: Boolean flag indicating if the email has been verified
- `verification_token`: String containing a secure token for email verification
- `verification_token_expires`: DateTime for token expiration
- `is_active`: Boolean flag that is set to true once the email is verified

### Backend Components

#### Security Module (`app/core/security.py`)

- `generate_verification_token()`: Generates a secure random token for email verification
- `create_verification_token_expiry()`: Creates an expiration timestamp (24 hours in the future)

#### User CRUD Operations (`app/crud/user.py`)

- `create_with_verification()`: Creates a user with verification token
- `get_by_verification_token()`: Finds a user by their verification token
- `verify_email()`: Marks the user's email as verified and activates their account
- `update_verification_token()`: Updates a user's verification token

#### Authentication Endpoints (`app/api/api_v1/endpoints/auth.py`)

- `POST /api/v1/auth/register`: Registers a user and sends a verification email
- `GET /api/v1/auth/verify-email/{token}`: Verifies an email using the provided token
- `POST /api/v1/auth/resend-verification`: Sends a new verification email
- `POST /api/v1/auth/login/access-token`: Checks for email verification before allowing login

#### Email Service (`app/services/email/email_service.py`)

- `send_verification_email()`: Sends an email with a verification link to the user

### Frontend Components

#### API Client (`frontend/src/lib/api.js`)

- `verifyEmail(token)`: Calls the verification endpoint with a token
- `resendVerification(email)`: Requests a new verification email

#### Redux Slice (`frontend/src/lib/redux/slices/authSlice.js`)

- Manages verification state, statuses, and messages
- Provides async actions for verification and resend operations

#### Verification Pages

- `frontend/src/app/verify-email/page.js`: Handles the verification token and shows success/error states
- `frontend/src/app/resend-verification/page.js`: Allows users to request a new verification email

#### VerificationNotice Component (`frontend/src/components/VerificationNotice.js`)

- Reusable component for displaying verification-related messages

## User Flow

1. **Registration**:
   - User registers with their email and other information
   - Backend creates a user with `email_verified=false` and `is_active=false`
   - A verification token is generated and stored with an expiration time
   - A verification email is sent to the user

2. **Email Verification**:
   - User clicks the verification link in their email
   - Frontend extracts the token and sends it to the backend
   - Backend validates the token and updates the user's status
   - User is redirected to login page with success message

3. **Login After Verification**:
   - User attempts to log in with their credentials
   - Backend checks if email is verified before allowing login
   - If verified, user gets access token; if not, error message is shown

4. **Resend Verification**:
   - If the verification email is lost or the token expired, user can request a new one
   - Backend generates a new token and sends a fresh verification email

## Testing

The verification system is thoroughly tested with:

- Unit tests for individual components
- Integration tests for verification endpoints
- End-to-end flow tests for the complete verification process

## Security Considerations

- Tokens are cryptographically secure and URL-safe
- Tokens expire after 24 hours for security
- User accounts are inactive until verified
- Email addresses are validated on the frontend and backend
- All email addresses must be unique in the system
