"""
Kassenabgleich.py
-----------------
Ein einfaches Python-Tool zum Vergleichen von Kassendaten (cash_data.csv)
und Finanzdaten (finance_data.csv).
Es erkennt:
 - Übereinstimmende Transaktionen
 - Abweichende Beträge
 - Fehlende oder zusätzliche Transaktionen

Autor: Dhruvit Goti
Version: 1.0
"""

import pandas as pd
from datetime import datetime
import os

# ---- Konfiguration ----
DATA_DIR = "../data"
CASH_FILE = os.path.join(DATA_DIR, "cash_data.csv")
FIN_FILE = os.path.join(DATA_DIR, "finance_data.csv")

# ---- Daten einlesen ----
cash_df = pd.read_csv(CASH_FILE)
fin_df = pd.read_csv(FIN_FILE)

# ---- Transaktionen vergleichen ----
merged = pd.merge(
    cash_df, fin_df, on="transaction_id", how="outer",
    suffixes=('_cash', '_fin')
)

# ---- Ergebnisse vorbereiten ----
matched = merged[(merged["amount_cash"] == merged["amount_fin"]) & merged["amount_cash"].notna()]
mismatched = merged[(merged["amount_cash"] != merged["amount_fin"]) & merged["amount_cash"].notna() & merged["amount_fin"].notna()]
missing_in_fin = merged[merged["amount_fin"].isna()]
extra_in_fin = merged[merged["amount_cash"].isna()]

# ---- Bericht generieren ----
report_lines = []
report_lines.append(f"Reconciliation Report – {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report_lines.append("-" * 60)
report_lines.append(f"Total in Cash Register: {len(cash_df)}")
report_lines.append(f"Total in Finance System: {len(fin_df)}")
report_lines.append("")
report_lines.append(f"✅ Matched Transactions: {len(matched)}")
report_lines.append(f"⚠️ Mismatched Transactions: {len(mismatched)}")
report_lines.append(f"❌ Missing in Finance: {len(missing_in_fin)}")
report_lines.append(f"➕ Extra in Finance: {len(extra_in_fin)}")
report_lines.append("")

if not mismatched.empty:
    report_lines.append("Details of mismatched transactions:")
    for _, row in mismatched.iterrows():
        report_lines.append(
            f"- {row['transaction_id']}: Cash = {row['amount_cash']} | Finance = {row['amount_fin']}"
        )
    report_lines.append("")

if not missing_in_fin.empty:
    report_lines.append("Transactions missing in Finance:")
    for _, row in missing_in_fin.iterrows():
        report_lines.append(f"- {row['transaction_id']} ({row['amount_cash']} EUR)")
    report_lines.append("")

if not extra_in_fin.empty:
    report_lines.append("Transactions extra in Finance:")
    for _, row in extra_in_fin.iterrows():
        report_lines.append(f"- {row['transaction_id']} ({row['amount_fin']} EUR)")
    report_lines.append("")

# ---- Bericht speichern ----
output_dir = "../outputs"
os.makedirs(output_dir, exist_ok=True)
report_path = os.path.join(output_dir, f"reconciliation_report_{datetime.now().strftime('%Y%d%m_%H%M%S')}.txt")

with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print("✅ Kassenabgleich abgeschlossen!")
print(f"Bericht gespeichert unter: {report_path}")
