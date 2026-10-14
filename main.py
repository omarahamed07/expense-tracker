import argparse
import datetime
import sys

import db


def positive_amount(value):
    try:
        amount = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a number")
    if amount <= 0:
        raise argparse.ArgumentTypeError("amount must be greater than 0")
    return amount


def month_string(value):
    try:
        datetime.datetime.strptime(value, "%Y-%m")
    except ValueError:
        raise argparse.ArgumentTypeError("month must be YYYY-MM, e.g. 2026-10")
    return value


def build_parser():
    parser = argparse.ArgumentParser(description="CLI Expense Tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_p = subparsers.add_parser("add", help="Add a new expense")
    add_p.add_argument("amount", type=positive_amount, help="Amount spent")
    add_p.add_argument("--category", default="other", help="Expense category")
    add_p.add_argument("--note", default=None, help="Optional note")

    list_p = subparsers.add_parser("list", help="List expenses")
    list_p.add_argument("--category", help="Filter by category")
    list_p.add_argument("--month", type=month_string, help="Filter by month (YYYY-MM)")

    del_p = subparsers.add_parser("delete", help="Delete an expense by ID")
    del_p.add_argument("id", type=int, help="Expense ID")

    sum_p = subparsers.add_parser("summary", help="Show spending summary")
    sum_p.add_argument("--month", type=month_string, help="Month (YYYY-MM)")

    return parser


def print_expenses(rows):
    if not rows:
        print("No expenses found.")
        return
    print(f"{'ID':<5}{'Date':<12}{'Amount':>10}  {'Category':<14}Note")
    print("-" * 60)
    for id_, amount, category, note, date in rows:
        print(f"{id_:<5}{date:<12}{amount:>10.2f}  {category:<14}{note or ''}")
    total = sum(row[1] for row in rows)
    print("-" * 60)
    print(f"{'Total':<17}{total:>10.2f}")


def print_summary(total, rows, month):
    print(f"Summary for {month}" if month else "Summary (all time)")
    if not rows:
        print("No expenses found.")
        return
    for category, amount in rows:
        share = amount / total * 100
        print(f"  {category:<14}{amount:>10.2f}  ({share:.0f}%)")
    print(f"  {'Total':<14}{total:>10.2f}")


def main():
    args = build_parser().parse_args()
    db.init_db()

    if args.command == "add":
        category = args.category.lower()
        db.add_expense(args.amount, category, args.note)
        print(f"Added: {args.amount:.2f} in '{category}'")

    elif args.command == "list":
        category = args.category.lower() if args.category else None
        print_expenses(db.list_expenses(category=category, month=args.month))

    elif args.command == "delete":
        if db.delete_expense(args.id):
            print(f"Deleted expense {args.id}")
        else:
            sys.exit(f"No expense found with ID {args.id}")

    elif args.command == "summary":
        total, rows = db.get_summary(args.month)
        print_summary(total, rows, args.month)


if __name__ == "__main__":
    main()