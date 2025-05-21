from typing import Any, Dict, Optional, Union
import datetime

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        Get user by email
        
        Args:
            db: Database session
            email: Email of the user
            
        Returns:
            User if found, None otherwise
        """
        return db.query(User).filter(User.email == email).first()
        
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        Create a new user with password hashing
        
        Args:
            db: Database session
            obj_in: Schema for creating a user
            
        Returns:
            Created user
        """
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
            is_active=False  # User is inactive until email is verified
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
        
    def create_with_verification(self, db: Session, *, obj_in: UserCreate, 
                               verification_token: str, token_expires: datetime.datetime) -> User:
        """
        Create a new user with verification token
        
        Args:
            db: Database session
            obj_in: Schema for creating a user
            verification_token: Token for email verification
            token_expires: Token expiration timestamp
            
        Returns:
            Created user
        """
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
            is_active=False,  # User is inactive until email is verified
            email_verified=False,
            verification_token=verification_token,
            verification_token_expires=token_expires
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """
        Update a user
        
        Args:
            db: Database session
            db_obj: Existing user to update
            obj_in: Schema for updating a user or a dictionary
            
        Returns:
            Updated user
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
            
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password
        
        Args:
            db: Database session
            email: Email of the user
            password: Password to verify
            
        Returns:
            Authenticated user if valid, None otherwise
        """
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
        
    def is_active(self, user: User) -> bool:
        """
        Check if user is active
        
        Args:
            user: User to check
            
        Returns:
            True if user is active, False otherwise
        """
        return user.is_active
        
    def is_superuser(self, user: User) -> bool:
        """
        Check if user is superuser
        
        Args:
            user: User to check
            
        Returns:
            True if user is superuser, False otherwise
        """
        return user.is_superuser
        
    # This method is already defined above - removed duplicate implementation
        
    def get_by_verification_token(self, db: Session, *, token: str) -> Optional[User]:
        """
        Get user by verification token
        
        Args:
            db: Database session
            token: Verification token
            
        Returns:
            User if found, None otherwise
        """
        return db.query(User).filter(User.verification_token == token).first()
        
    def verify_email(self, db: Session, *, user: User) -> User:
        """
        Mark user email as verified and activate the account
        
        Args:
            db: Database session
            user: User to verify
            
        Returns:
            Updated user
        """
        user.email_verified = True
        user.is_active = True
        user.verification_token = None
        user.verification_token_expires = None
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
        
    def update_verification_token(
        self, db: Session, *, user: User, verification_token: str, token_expires: datetime.datetime
    ) -> User:
        """
        Update user's verification token
        
        Args:
            db: Database session
            user: User to update
            verification_token: New verification token
            token_expires: New expiration datetime for the token
            
        Returns:
            Updated user
        """
        user.verification_token = verification_token
        user.verification_token_expires = token_expires
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


user = CRUDUser(User)
