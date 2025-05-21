"""
AI services for Smart Travel app 

This package contains AI-powered services for generating travel recommendations,
analyzing prices, and generating packing suggestions.
"""

from app.services.ai.recommendation_engine import RecommendationEngine
from app.services.ai.price_analyzer import PriceAnalyzer
from app.services.ai.packing_suggestion import PackingSuggestionGenerator

__all__ = ['RecommendationEngine', 'PriceAnalyzer', 'PackingSuggestionGenerator']