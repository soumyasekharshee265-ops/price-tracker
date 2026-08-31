from database import Base, engine
from models.product import Product
from models.price_history import PriceHistory
from models.alert import Alert
from models.coupon import Coupon
from models.stock_status import StockStatus
from models.trending_deal import TrendingDeal
from models.suggestion import Suggestion
from models.review import Review

Base.metadata.create_all(bind=engine)

print("Tables created successfully.")