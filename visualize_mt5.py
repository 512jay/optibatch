# visualize_mt5.py

import streamlit as st
import pandas as pd
import argparse
from pathlib import Path
from lxml import etree
import re
import xml.etree.ElementTree as ET
import pandas as pd
import re
from pathlib import Path


def parse_mt5_report(file_path: Path):
    namespaces = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"}

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except Exception as e:
        print(f"❌ Failed to parse {file_path.name}: {e}")
        return pd.DataFrame()

    # Find the worksheet with optimization results
    table_elem = root.find(".//ss:Worksheet/ss:Table", namespaces)
    if table_elem is None:
        print(f"⚠️ No Table found in {file_path.name}")
        return pd.DataFrame()

    # Parse rows
    rows = table_elem.findall("ss:Row", namespaces)
    if not rows:
        return pd.DataFrame()

    # Extract header
    headers = [
        cell.findtext("ss:Data", default="", namespaces=namespaces) for cell in rows[0]
    ]
    data = []

    for row in rows[1:]:
        row_data = []
        for cell in row.findall("ss:Cell", namespaces):
            text = cell.findtext("ss:Data", default="", namespaces=namespaces)
            row_data.append(text)
        if len(row_data) == len(headers):
            data.append(row_data)

    df = pd.DataFrame(data, columns=headers)

    # Extract metadata from filename
    match = re.match(
        r"(?P<expert>[^.]+)\.(?P<symbol>[A-Z]+)\.(?P<tf>[A-Z0-9]+)\.(?P<start>\d{8})_(?P<end>\d{8})\.(?P<run>\d+)(?:\.(?P<suffix>\w+))?\.xml",
        file_path.name,
    )
    if match:
        meta = match.groupdict()
        df["expert"] = meta["expert"]
        df["symbol"] = meta["symbol"]
        df["timeframe"] = meta["tf"]
        df["start_date"] = pd.to_datetime(meta["start"], format="%Y%m%d")
        df["end_date"] = pd.to_datetime(meta["end"], format="%Y%m%d")
        df["run_id"] = meta["run"]
        df["report_type"] = meta.get("suffix") or "main"
    else:
        df["expert"] = "Unknown"
        df["symbol"] = "Unknown"
        df["timeframe"] = "Unknown"
        df["start_date"] = None
        df["end_date"] = None
        df["run_id"] = "?"
        df["report_type"] = "main"

    return df


def extract_additional_info(tree: etree._ElementTree) -> dict:
    ns = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"}
    workbook_props = tree.xpath("//ss:Workbook/ss:DocumentProperties", namespaces=ns)
    info = {}
    for prop in workbook_props:
        for child in prop.iterchildren():
            tag = child.tag.split("}")[-1]
            info[tag.lower()] = child.text
    return info


def main(folder):
    st.title("📊 MT5 Optimization Report Viewer")

    folder = Path(folder)
    files = list(folder.glob("*.xml"))
    if not files:
        st.warning("No XML files found in folder.")
        return

    dfs = [parse_mt5_report(f) for f in files]
    dfs = [df for df in dfs if not df.empty]

    if not dfs:
        st.error("No valid MT5 XML reports found.")
        return

    df = pd.concat(dfs, ignore_index=True)

    with st.sidebar:
        st.header("🔎 Filters")
        experts = st.multiselect(
            "Expert Advisor", sorted(df["expert"].unique()), default=None
        )
        symbols = st.multiselect("Symbol", sorted(df["symbol"].unique()), default=None)

        if experts:
            df = df[df["expert"].isin(experts)]
        if symbols:
            df = df[df["symbol"].isin(symbols)]

    st.dataframe(df)

    if "Profit" in df.columns and "Drawdown" in df.columns:
        df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
        df["Drawdown"] = pd.to_numeric(df["Drawdown"], errors="coerce")
        st.subheader("Profit vs Drawdown")
        st.scatter_chart(df[["Profit", "Drawdown"]].dropna())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--folder", required=True, help="Path to folder with MT5 XML files"
    )
    args = parser.parse_args()
    main(args.folder)
