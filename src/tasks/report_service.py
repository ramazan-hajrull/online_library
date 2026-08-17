from datetime import datetime
from pathlib import Path

from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

REPORTS_DIR = Path("uploads/reports")


def _ensure_dir() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def generate_library_stats_pdf(stats: dict) -> str:
    """stats keys: new_books, new_reviews, active_users, top_books (list of
    dict with title/average_rating/reviews_count), generated_at."""
    _ensure_dir()
    filename = REPORTS_DIR / f"library_stats_{datetime.utcnow():%Y%m%d_%H%M%S}.pdf"

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(filename), pagesize=A4)
    elements = [
        Paragraph("Отчёт по статистике библиотеки", styles["Title"]),
        Spacer(1, 12),
        Paragraph(f"Сформирован: {stats['generated_at']}", styles["Normal"]),
        Spacer(1, 12),
        Paragraph(f"Новых книг: {stats['new_books']}", styles["Normal"]),
        Paragraph(f"Новых отзывов: {stats['new_reviews']}", styles["Normal"]),
        Paragraph(f"Активных пользователей: {stats['active_users']}", styles["Normal"]),
        Spacer(1, 20),
        Paragraph("Топ книг по рейтингу", styles["Heading2"]),
    ]

    table_data = [["Название", "Средний рейтинг", "Кол-во отзывов"]]
    for book in stats.get("top_books", []):
        table_data.append([book["title"], f"{book['average_rating']:.2f}", str(book["reviews_count"])])

    table = Table(table_data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    elements.append(table)

    doc.build(elements)
    return str(filename)


def generate_library_stats_excel(stats: dict) -> str:
    _ensure_dir()
    filename = REPORTS_DIR / f"library_stats_{datetime.utcnow():%Y%m%d_%H%M%S}.xlsx"

    wb = Workbook()
    summary_ws = wb.active
    summary_ws.title = "Сводка"
    summary_ws.append(["Сформирован", stats["generated_at"]])
    summary_ws.append(["Новых книг", stats["new_books"]])
    summary_ws.append(["Новых отзывов", stats["new_reviews"]])
    summary_ws.append(["Активных пользователей", stats["active_users"]])

    top_ws = wb.create_sheet("Топ книг")
    top_ws.append(["Название", "Средний рейтинг", "Кол-во отзывов"])
    for book in stats.get("top_books", []):
        top_ws.append([book["title"], round(book["average_rating"], 2), book["reviews_count"]])

    wb.save(filename)
    return str(filename)