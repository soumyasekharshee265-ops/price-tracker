from apscheduler.schedulers.blocking import BlockingScheduler
from scheduler.price_refresher import refresh_prices
from scheduler.alert_checker import check_alerts
from scheduler.stock_checker import check_stock
from scheduler.deals_refresher import refresh_trending_deals

def run_full_cycle():
    print("\n--- Starting scheduled check ---")
    refresh_prices()
    check_alerts()
    check_stock()
    print("--- Scheduled check complete ---\n")


def run_deals_cycle():
    print("\n--- Refreshing trending deals ---")
    refresh_trending_deals()
    print("--- Trending deals refresh complete ---\n")

scheduler = BlockingScheduler()
scheduler.add_job(run_full_cycle, "interval", minutes=30)
scheduler.add_job(run_deals_cycle, "interval", hours=12)

if __name__ == "__main__":
    print("Scheduler started. Running every 30 minutes. Press Ctrl+C to stop.")
    run_full_cycle()
    scheduler.start()