import FinanceDataReader as fdr
import yfinance as yf
import json, datetime, time, warnings

warnings.filterwarnings("ignore")

US = ["GEV", "CRDO", "AVGO", "DELL", "BE", "INTC"]

# (코드, 야후접미사) — 코스닥=.KQ, 코스피=.KS
KR = [
    ("010060", ".KS"),
    ("000660", ".KS"),
    ("005930", ".KS"),
    ("017670", ".KS"),
    ("487240", ".KS"),
    ("329180", ".KS"),
    ("006400", ".KS"),
    ("009150", ".KS"),
]

today = datetime.date.today()
start = (today - datetime.timedelta(days=10)).strftime("%Y-%m-%d")

out = []

for t in US:
    try:
        df = fdr.DataReader(t, start)
        out.append({
            "ticker": t,
            "price": round(float(df["Close"].iloc[-1]), 2),
            "prevClose": round(float(df["Close"].iloc[-2]), 2),
            "date": str(df.index[-1].date()),
            "currency": "USD",
        })
    except Exception as e:
        out.append({"ticker": t, "price": None, "err": str(e)[:80]})
    time.sleep(0.5)

for code, suf in KR:
    try:
        df = yf.Ticker(code + suf).history(period="7d")
        out.append({
            "ticker": code,
            "price": int(df["Close"].iloc[-1]),
            "prevClose": int(df["Close"].iloc[-2]),
            "date": str(df.index[-1].date()),
            "currency": "KRW",
        })
    except Exception as e:
        out.append({"ticker": code, "price": None, "err": str(e)[:80]})
    time.sleep(0.5)

with open("prices.json", "w", encoding="utf-8") as f:
    json.dump(
        {"updated": datetime.datetime.utcnow().isoformat() + "Z", "data": out},
        f,
        ensure_ascii=False,
        indent=2,
    )

print("done", len(out), "tickers")
