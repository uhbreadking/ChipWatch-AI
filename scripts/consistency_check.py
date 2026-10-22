import sys
from pathlib import Path

import pandas as pd

LABELS = Path("data/labels/to_label.csv")
CHECK = Path("data/labels/consistency_check.csv")


def make_check_file():
    df = pd.read_csv(LABELS, encoding="utf-8-sig", keep_default_na=False)
    labeled = df[df["label"].notna() & (df["label"] != "")]
    sample = labeled.sample(n=min(10, len(labeled)), random_state=7)
    blank = sample[["headline_id", "title"]].copy()
    blank["label"] = ""
    blank["event_status"] = ""
    blank.to_csv(CHECK, index=False, encoding="utf-8-sig")
    print(f"Created {CHECK} with {len(blank)} headlines. Label them without looking at your earlier answers.")


def compare():
    original = pd.read_csv(LABELS, encoding="utf-8-sig", keep_default_na=False)
    redo = pd.read_csv(CHECK, encoding="utf-8-sig", keep_default_na=False)
    merged = redo.merge(original, on="headline_id", suffixes=("_redo", "_original"))

    same_label = (merged["label_redo"] == merged["label_original"]).sum()
    same_status = (merged["event_status_redo"] == merged["event_status_original"]).sum()
    print(f"Label agreement:  {same_label} of {len(merged)}")
    print(f"Status agreement: {same_status} of {len(merged)}")

    differences = merged[
        (merged["label_redo"] != merged["label_original"])
        | (merged["event_status_redo"] != merged["event_status_original"])
    ]
    if not differences.empty:
        print("\nDisagreements:")
        print(differences[["headline_id", "title_redo", "label_original", "label_redo",
                           "event_status_original", "event_status_redo"]].to_string())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "compare":
        compare()
    else:
        make_check_file()