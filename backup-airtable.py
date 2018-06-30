#!/usr/bin/env python3

import argparse
import datetime
import json
import multiprocessing
import os
import requests
import sys

now = datetime.datetime.now()

parser = argparse.ArgumentParser(description="Back up Airtable Base. Requires you to set $AIRTABLE_API_KEY in the environment.")
parser.add_argument('--filename', type=argparse.FileType("w"),
                    help="Backup file name. Defaults to [base_id][date][time].json")
parser.add_argument("base_id", type=str, help="Base ID")
parser.add_argument("tables", type=str, nargs="+",
                    help="Base Tables.")

args = parser.parse_args()

if "AIRTABLE_API_KEY" not in os.environ:
  print("Please set $AIRTABLE_API_KEY in your shell.")
  sys.exit(1)
AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]

if args.filename is None:
  args.filename = open("[%s]%s.json" % (args.base_id, now.strftime("[%Y-%m-%d][%H-%M-%S]")), "w")
AIRTABLE_API_URL = "https://api.airtable.com/v0"

def get_table_page(table_name, offset=None):
  params = {"view": "Grid view"}
  if offset:
    params["offset"] = offset
  return requests.get(
    "%s/%s/%s" % (AIRTABLE_API_URL, args.base_id, table_name),
    params=params,
    headers={"Authorization": "Bearer %s" % AIRTABLE_API_KEY}
  )

def get_table(table_name):
  print("[Downloading first page] %s" % table_name)
  output = {"records": []}
  offset = None
  while True:
    page = get_table_page(table_name, offset).json()
    output["records"] += page["records"]
    offset = page.get("offset", None)
    if not offset:
      break
    print("[Downloading next page] %s (offset: %s)" % (table_name, offset))

  print("[Done] %s" % table_name)
  return output

def fetch_table(table_name):
  return table_name, get_table(table_name)

if __name__ == "__main__":
  with multiprocessing.Pool(processes=10) as pool:
    all_tables = {}
    print("Downloading %d tables." % len(args.tables))
    for name, data in pool.map(fetch_table, args.tables):
      all_tables[name] = data
    with args.filename:
      json.dump({
        "base_id": args.base_id,
        "timestamp": str(now),
        "tables": all_tables
      }, args.filename, sort_keys=True)
