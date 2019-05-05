#!/usr/bin/env python3

# std
from pathlib import Path

# 3rd
import pandas as pd
import numpy as np

# ours
from ankipandas.util.misc import invert_dict

tables_ours2anki = {
    "revs": "revlog",
    "cards": "cards",
    "notes": "notes"
}
tables_anki2ours = invert_dict(tables_ours2anki)

fields_file = Path(__file__).parent / "data" / "anki_fields.csv"
fields_df = pd.read_csv(fields_file)

our_tables = sorted(list(tables_ours2anki.keys()))
our_columns = {
    table: sorted(list(
        fields_df[np.logical_and(
            fields_df["Table"] == table,
            fields_df["Default"] == True
        )]["Column"].unique()
    ))
    for table in our_tables
}

columns_ours2anki = {
    table: dict(zip(
        fields_df[fields_df["Table"] == table]["Column"],
        fields_df[fields_df["Table"] == table]["AnkiColumn"]
    ))
    for table in our_tables
}


columns_anki2ours = {
    table: invert_dict(columns_ours2anki[table])
    for table in our_tables
}

value_maps = {
    "cards": {
        "cqueue": {
            -3: "sched buried",
            -2: "user buried",
            -1: "suspended",
            0: "new",
            1: "learning",
            2: "due",
            3: "in learning"
        },
        "ctype": {
            0: "learning",
            1: "review",
            2: "relearn",
            3: "cram"
        }
    },
    "revs": {
        "rtype": {
            0: "learning",
            1: "review",
            2: "relearn",
            3: "cram"
        }
    }
}

dtype_casts = {
    "notes": {"id": str, "mid": str},
    "cards": {"id": str, "nid": str, "did": str},
    "revs": {"id": str, "cid": str}
}