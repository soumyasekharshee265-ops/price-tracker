from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import search, trends, deal_score, fake_discount, compare, alerts, stock, coupons, recommend, predict, deals, suggestions, reviews

app = FastAPI(title="Price Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",       
        "https://your-frontend-domain.vercel.app",  
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(trends.router, prefix="/api", tags=["trends"])
app.include_router(deal_score.router, prefix="/api", tags=["deal_score"])
app.include_router(fake_discount.router, prefix="/api", tags=["fake_discount"])
app.include_router(compare.router, prefix="/api", tags=["compare"])
app.include_router(alerts.router, prefix="/api", tags=["alerts"])
app.include_router(stock.router, prefix="/api", tags=["stock"])
app.include_router(coupons.router, prefix="/api", tags=["coupons"])
app.include_router(recommend.router, prefix="/api", tags=["recommend"])
app.include_router(predict.router, prefix="/api", tags=["predict"])
app.include_router(deals.router, prefix="/api", tags=["deals"])
app.include_router(suggestions.router, prefix="/api", tags=["suggestions"])
app.include_router(reviews.router, prefix="/api", tags=["reviews"])

@app.get("/")
def root():
    return {"message": "Price Tracker API is running"}