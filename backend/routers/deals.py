"""
MDIP Backend - Deals/Intelligence Feed Router
Protected endpoints for investment opportunities and market intelligence
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging

from backend.security import verify_token

logger = logging.getLogger(__name__)

router = APIRouter()

# Pydantic Models for type safety and documentation
class InvestmentOpportunity(BaseModel):
    """Investment opportunity object for SaaS intelligence feed"""
    id: str
    location: str
    score: float  # 0.0 - 100.0
    value: float  # USD value
    insight: str
    category: str
    risk_level: str
    timestamp: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": "deal_001",
                "location": "San Francisco, CA",
                "score": 87.5,
                "value": 2500000,
                "insight": "High-growth tech startup in AI space with strong market fit",
                "category": "Technology",
                "risk_level": "Medium",
                "timestamp": "2026-05-12T10:30:00Z"
            }
        }


class FeedResponse(BaseModel):
    """Response model for deals feed"""
    total: int
    page: int
    page_size: int
    opportunities: List[InvestmentOpportunity]


# Simulated data store (replace with database)
MOCK_OPPORTUNITIES = [
    {
        "id": "deal_001",
        "location": "San Francisco, CA",
        "score": 87.5,
        "value": 2500000,
        "insight": "AI-powered SaaS startup with strong market fit and experienced team",
        "category": "Technology",
        "risk_level": "Medium",
        "timestamp": datetime.now().isoformat()
    },
    {
        "id": "deal_002",
        "location": "Austin, TX",
        "score": 92.3,
        "value": 5000000,
        "insight": "Biotech company developing breakthrough cancer treatment",
        "category": "Healthcare",
        "risk_level": "High",
        "timestamp": datetime.now().isoformat()
    },
    {
        "id": "deal_003",
        "location": "New York, NY",
        "score": 78.9,
        "value": 1800000,
        "insight": "Fintech solution disrupting traditional banking infrastructure",
        "category": "Finance",
        "risk_level": "Medium",
        "timestamp": datetime.now().isoformat()
    },
    {
        "id": "deal_004",
        "location": "Seattle, WA",
        "score": 85.2,
        "value": 3200000,
        "insight": "Sustainability-focused supply chain optimization platform",
        "category": "GreenTech",
        "risk_level": "Low",
        "timestamp": datetime.now().isoformat()
    },
    {
        "id": "deal_005",
        "location": "Boston, MA",
        "score": 91.1,
        "value": 4500000,
        "insight": "Next-gen cybersecurity platform with AI threat detection",
        "category": "Cybersecurity",
        "risk_level": "Low",
        "timestamp": datetime.now().isoformat()
    }
]


@router.get("/feed", response_model=FeedResponse, dependencies=[Depends(verify_token)])
async def get_deals_feed(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    min_score: float = Query(0, ge=0, le=100, description="Minimum opportunity score"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    """
    Get investment opportunities feed (JWT protected)
    
    Returns paginated list of investment opportunities with scoring and insights.
    Supports filtering by score and category for fine-grained control.
    
    **Security**: Requires valid JWT token in Authorization header
    
    **Future Enhancement**: This endpoint will integrate with AI models to generate
    real-time insights and dynamic scoring based on market conditions.
    """
    
    logger.info(f"Fetching deals feed - page: {page}, size: {page_size}, min_score: {min_score}")
    
    # Filter opportunities
    filtered_opportunities = MOCK_OPPORTUNITIES
    
    if min_score > 0:
        filtered_opportunities = [opp for opp in filtered_opportunities if opp["score"] >= min_score]
    
    if category:
        filtered_opportunities = [opp for opp in filtered_opportunities if opp["category"].lower() == category.lower()]
    
    # Pagination
    total = len(filtered_opportunities)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    paginated_opportunities = filtered_opportunities[start_idx:end_idx]
    
    # Convert to response models
    opportunities = [
        InvestmentOpportunity(**opp) for opp in paginated_opportunities
    ]
    
    return FeedResponse(
        total=total,
        page=page,
        page_size=page_size,
        opportunities=opportunities
    )


@router.get("/feed/{deal_id}", response_model=InvestmentOpportunity, dependencies=[Depends(verify_token)])
async def get_deal_detail(deal_id: str):
    """
    Get detailed information about a specific investment opportunity (JWT protected)
    
    Returns full opportunity details including AI-generated insights.
    
    **Future Enhancement**: Will include historical performance data and AI analysis.
    """
    
    for opportunity in MOCK_OPPORTUNITIES:
        if opportunity["id"] == deal_id:
            return InvestmentOpportunity(**opportunity)
    
    raise HTTPException(status_code=404, detail=f"Deal {deal_id} not found")


@router.post("/feed/search", response_model=FeedResponse, dependencies=[Depends(verify_token)])
async def search_deals(
    query: str = Query(..., description="Search query (location, category, or insight keywords)"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """
    Search investment opportunities by keyword (JWT protected)
    
    Searches across location, category, and insight fields.
    
    **Future Enhancement**: Will integrate with Elasticsearch for production-grade full-text search.
    """
    
    query_lower = query.lower()
    
    filtered = [
        opp for opp in MOCK_OPPORTUNITIES
        if query_lower in opp["location"].lower() or
           query_lower in opp["category"].lower() or
           query_lower in opp["insight"].lower()
    ]
    
    total = len(filtered)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    paginated = filtered[start_idx:end_idx]
    opportunities = [InvestmentOpportunity(**opp) for opp in paginated]
    
    return FeedResponse(
        total=total,
        page=page,
        page_size=page_size,
        opportunities=opportunities
    )
