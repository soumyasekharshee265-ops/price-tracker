# Price Tracker

**The problem it solves:** When you shop online, the same product often has different prices on different websites. Also, discounts aren't always real — a store might raise the price first and then say "50% off" to make it look better. This project checks multiple stores automatically and shows you the real price, real discounts, and price history in one place.

## Demo

*(Video goes here — see instructions below)*

## Screenshots

<img width="1920" height="1080" alt="Screenshot 2026-09-01 082751" src="https://github.com/user-attachments/assets/0e4528e5-8fdb-4d2d-914e-a2e227ba4fc9" />
<img width="1920" height="1080" alt="Screenshot 2026-09-01 083117" src="https://github.com/user-attachments/assets/2709fec1-9a1f-4e7b-a19b-99c0c082d7c7" />
<img width="1920" height="1080" alt="Screenshot 2026-09-01 082919" src="https://github.com/user-attachments/assets/7faf591c-7ad4-458d-9977-23fab6e7b9a4" />
<img width="1920" height="1080" alt="Screenshot 2026-09-01 083320" src="https://github.com/user-attachments/assets/e3de33cd-b044-42e0-a270-558b75392220" />
<img width="1920" height="1080" alt="Screenshot 2026-09-01 083346" src="https://github.com/user-attachments/assets/917b9d9b-1109-4cc0-9e81-5a725d3a1610" />





## Features

- **Cross-platform price search** — search once, get live results from Amazon, Flipkart, and Myntra simultaneously
- **No API keys or rate limits** — uses Playwright (real browser automation) instead of paid/rate-limited third-party APIs
- **AI-powered data cleanup** — a local Ollama (llama3.2) model parses and structures messy scraped page data
- **Smart relevance ranking** — filters out irrelevant accessories (cases, chargers) and ranks results by genuine product match, not just keyword overlap
- **Price history tracking** — see how a product's price has changed over time
- **Deals page** — browse trending deals filtered by price range, discount percentage, or category
- **User reviews & feature suggestions** — visitors can leave reviews and suggest features directly from the site
- **Self-updating** — a background scheduler keeps re-scraping and refreshing data automatically, with no manual work needed

## Tech Stack

**Backend:** FastAPI · SQLAlchemy · PostgreSQL (Supabase) · APScheduler · Playwright · Ollama (llama3.2)

**Frontend:** React · Vite · React Router · Recharts · Framer Motion

## How It Works

The data flows through the system in six steps:

1. **Scraping** — the backend visits store websites regularly using Playwright and pulls out the raw page data
2. **Understanding** — the raw data is passed to a local AI model (Ollama), which reads it and extracts clean information: product name, price, image, discount percentage
3. **Storage** — the clean data is saved in a PostgreSQL database, along with older prices too, so price history can be tracked
4. **Auto-refresh** — a background scheduler (APScheduler) keeps repeating the scrape-and-update process at fixed intervals — this is what makes the project "self-updating"
5. **Serving** — the FastAPI backend exposes clean endpoints for each feature (search, compare, alerts, fake-discount check, trends) that the frontend calls
6. **Display** — the React frontend takes the data from the APIs and displays it as cards, layouts, and animations for the user

### Why each tool is needed

| Tool | Why it's needed | What it does |
|---|---|---|
| **Playwright** | Modern shopping sites load content using JavaScript, so a simple request can't get the real data | Opens an actual browser automatically (like a person would), fully loads the page, then pulls out the content |
| **Ollama (local AI model)** | Every store website looks different, so fixed scraping rules would break whenever a site changes its layout | Reads the raw scraped text and understands it well enough to extract the title, price, and discount — even if the layout changes |
| **APScheduler** | Prices change all the time and can't be updated by hand | Runs scraping and update jobs automatically at fixed intervals in the background — this is what makes the "self-update" feature work |
| **PostgreSQL (Supabase)** | Extracted data needs to be stored reliably so it can be searched and reused | Stores product details, price history, alerts, and coupons |
| **FastAPI** | The frontend shouldn't directly touch the database | Provides clean endpoints for each feature that the frontend calls |
| **React + Vite** | Users need a visual, easy-to-understand page, not raw data | Takes the data from the APIs and displays it as cards, layouts, and animations |

**The overall goal:** show the user accurate, always up-to-date price comparisons, without anyone having to check manually. Playwright keeps the data fresh, Ollama makes sense of it regardless of how each site is structured, APScheduler keeps the whole process running automatically, and the database keeps a history that also helps detect patterns like fake discounts.

## Project Structure

```
price-tracker/
├── backend/
│   ├── agent/                # Playwright scrapers + AI extraction logic (search_agent.py, prompts.py)
│   ├── api/                  # Route handlers (search, compare, deals, reviews, alerts, coupons, etc.)
│   ├── models/                # Database models (product, review, alert, coupon, etc.)
│   ├── scheduler/             # Background jobs (price refresh, stock checks, deal refresh, etc.)
│   ├── main.py
│   ├── database.py
│   ├── create_tables.py
│   └── requirements.txt
└── frontend/
    ├── public/
    │   └── logos/             # Platform brand logos
    ├── src/
    │   ├── components/        # Navbar, Footer, SearchBar, ProductCard, etc.
    │   ├── pages/              # Home, ComparisonResults, DealsPage, ProductDetail, Alert
    │   ├── config.js
    │   └── App.jsx
    └── package.json
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- [Ollama](https://ollama.com) installed locally, with the `llama3.2` model pulled (`ollama pull llama3.2`)
- A free [Supabase](https://supabase.com) account (for the database)

### 1. Clone the repository

```bash
git clone https://github.com/soumyasekharshee265-ops/price-tracker.git
cd price-tracker
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
playwright install --with-deps chromium
```

Create a `.env` file in the `backend/` folder with your Supabase connection string:

```
DATABASE_URL=postgresql://postgres.[your-project]:[password]@[your-pooler-host]:5432/postgres
```

Create the database tables:

```bash
python create_tables.py
```

Start the backend:

```bash
uvicorn main:app --reload
```

The API will be running at `http://localhost:8000`.

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

The site will be running at `http://localhost:5173`.

### 4. Ollama setup

Make sure Ollama is running locally with the model pulled:

```bash
ollama pull llama3.2
```

The backend expects Ollama's API at `http://localhost:11434` by default.

## Known Limitations

- Meesho is not supported due to aggressive bot detection blocking automated scraping
- Some Flipkart product listings may not include images if none exist in the page's source data

## License

This project does not currently have an open-source license. Feel free to reach out if you'd like to use or build on it.
