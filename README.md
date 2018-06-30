# `airtable-backup`

[Airtable](https://airtable.com/) supports [online snapshots](https://support.airtable.com/hc/en-us/articles/202584799-Taking-and-restoring-base-snapshots), but [no way to take home your data](https://community.airtable.com/t/offline-local-backup/754).

## Usage

    # Replace (fake) sample data with your data.

    export AIRTABLE_API_KEY=keyAf4JcAuRJkr2AA
    ./backup-airtable.py appSD3jreJRer3Rer "Table 1" "Other Table" "One More Table"

Right now, `airtable-backup` assumes every table has a `Grid view`, and backs up that view.

## Limitations

Right now, you have to list every table by hand, rather than just specifying the base. I can only hope that Airtable doesn't [have a nefarious reason for this](https://en.wikipedia.org/wiki/Vendor_lock-in), but [they haven't added it to their API yet](https://community.airtable.com/t/list-tables-given-api-key-and-baseid/1173).
