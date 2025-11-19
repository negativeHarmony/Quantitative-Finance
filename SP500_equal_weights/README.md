# S&P 500 Equal-Weights Portfolio (CSV Generator)

Generate an equal-weighted allocation for the S&P 500:

- Fetches the current S&P 500 constituents from the API Ninjas `sp500` endpoint
- Pulls Price and MarketCap using Yahoo Finance via `yfinance`
- Drops tickers with missing Price/MarketCap
- Computes suggested whole-share counts for an equal-weight portfolio
- Saves results to a CSV you name at runtime

---

## Requirements

- Python 3.9+ recommended
- Packages:
  - `pandas`
  - `yfinance`
  - `python-dotenv` (optional; only needed if you load `.env`)

Install packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install pandas yfinance requests python-dotenv
```

---

## API key

This project requires an API Ninjas key for the S&P 500 constituents endpoint.

- Environment variable: `API_KEY`
- Endpoint used: `https://api.api-ninjas.com/v1/sp500`

You can provide the key in either of two ways:

1) Export in your shell before running:
```bash
export API_KEY="your-real-api-key"
```

2) Create a `.env` file in this directory and load it with `python-dotenv`:
```
API_KEY=your-real-api-key
```

> If the script raises “Missing API_KEY environment variable”, ensure the key is exported or `.env` is present and loaded.

---

## Running

From this directory:

```bash
python3 equal_weights.py
```

The script will prompt you for:
- Portfolio amount (number)
- CSV file name (enter without “.csv”; the script appends it)

The output CSV is saved alongside the script as `<your_name>.csv`.

---

## What it does (high level)

1. Downloads current S&P 500 tickers from API Ninjas using `API_KEY`.
2. Normalizes ticker symbols (e.g., dots replaced with hyphens for Yahoo compatibility).
3. Uses `yfinance` to fetch:
   - `Price` (current/regular market price)
   - `MarketCap`
4. Converts `Price`/`MarketCap` to numeric and drops rows where either is missing.
5. Computes equal position size:
   \[
   \text{position\_size} = \frac{\text{portfolio\_amount}}{\text{num\_valid\_tickers}}
   \]
6. Calculates whole shares per ticker:
   \[
   \text{suggested\_shares} = \left\lfloor \frac{\text{position\_size}}{\text{Price}} \right\rfloor
   \]
7. Writes the final DataFrame to CSV with columns:
   - `Ticker`
   - `Price`
   - `MarketCap`
   - `suggested shares to buy`

---

## Caveats and data notes

- Some tickers may intermittently return missing data from Yahoo Finance (e.g., `PARA` can return 404 Not Found on the quoteSummary API). Those rows are dropped before allocation.
- Prices and market caps are subject to change and may differ slightly from other sources.
- Rate limits or connectivity issues can cause partial data; re-running can help.

---

## Troubleshooting

- Missing module `dotenv`:
  - Either install: `pip install python-dotenv`
  - Or remove `dotenv` usage and export `API_KEY` via shell

- “Missing API_KEY environment variable”:
  - Export `API_KEY` or create a `.env` file and ensure `load_dotenv()` is called

- Output CSV includes an index column:
  - That’s expected with `to_csv(..., index=True)`. If you prefer no index, change to `index=False` in the code.

- No rows in output:
  - If all tickers lacked valid `Price`/`MarketCap` at fetch time, the script drops them all. Try again later.

---

## Security

- Do not commit your `.env` or API keys to version control.
- Consider adding `.env` to your `.gitignore`.

---

## Acknowledgments

- [API Ninjas](https://api-ninjas.com) for the S&P 500 constituents endpoint


---



