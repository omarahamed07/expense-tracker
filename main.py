import argparse
import db


def build_parser():
    parser = argparse.ArgumentParser(description="CLI Expense Tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("amount", type=float, help="Amount spent")
    add_parser.add_argument("--category", default="other", help="Expense category")
    add_parser.add_argument("--note", default=None, help="Optional note")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    db.init_db()

    if args.command == "add":
        db.add_expense(args.amount, args.category, args.note)
        print(f"Added: {args.amount} in '{args.category}'")


if __name__ == "__main__":
    main()