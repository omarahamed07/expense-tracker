import pytest
import db


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_NAME", str(tmp_path / "test.db"))
    db.init_db()


def test_add_and_list():
    db.add_expense(100, "food", "lunch")
    rows = db.list_expenses()
    assert len(rows) == 1
    assert rows[0][1] == 100
    assert rows[0][2] == "food"


def test_add_rejects_non_positive_amount():
    with pytest.raises(ValueError):
        db.add_expense(0, "food")
    with pytest.raises(ValueError):
        db.add_expense(-5, "food")


def test_filter_by_category():
    db.add_expense(100, "food")
    db.add_expense(50, "transport")
    rows = db.list_expenses(category="food")
    assert len(rows) == 1
    assert rows[0][2] == "food"


def test_filter_by_month():
    db.add_expense(10, "food", date="2026-09-15")
    db.add_expense(20, "food", date="2026-10-02")
    rows = db.list_expenses(month="2026-10")
    assert len(rows) == 1
    assert rows[0][1] == 20


def test_delete():
    new_id = db.add_expense(100, "food")
    assert db.delete_expense(new_id) is True
    assert db.delete_expense(new_id) is False
    assert db.list_expenses() == []


def test_summary():
    db.add_expense(100, "food")
    db.add_expense(50, "food")
    db.add_expense(30, "transport")
    total, by_category = db.get_summary()
    assert total == 180
    assert by_category[0] == ("food", 150)