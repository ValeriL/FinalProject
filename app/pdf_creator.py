"""PDF files creating module."""

from app.models import MovieInfo
from fpdf import FPDF


def create_history_pdf() -> None:
    """Create a pdf file with serach history."""
    pdf = FPDF(format="A4", unit="in")
    pdf.add_page()
    pdf.set_font("Times", "", 10.0)
    epw = pdf.w - 2 * pdf.l_margin
    col_width = epw / 6
    header = ["Positive %", "Positive p", "Total", "Date"]
    pdf.set_font("Times", "B", 14.0)
    pdf.cell(epw, 0.0, "With more padding", align="C")
    pdf.set_font("Times", "", 10.0)
    pdf.ln(0.5)
    th = pdf.font_size
    pdf.cell(col_width * 0.2, 2 * th, "", border=1)
    pdf.cell(col_width * 3, 2 * th, "Title", border=1)
    for head in header:
        pdf.cell(col_width * 0.7, 2 * th, head, border=1)

    pdf.ln(2 * th)
    movies = MovieInfo.query.all()
    for movie in movies:
        pdf.cell(col_width * 0.2, 2 * th, str(movie.movie_id), border=1)
        pdf.cell(
            col_width * 3,
            2 * th,
            movie.title.encode("latin-1", "replace").decode("latin-1"),
            border=1,
        )
        pdf.cell(col_width * 0.7, 2 * th, str(movie.positive_percent), border=1)
        pdf.cell(col_width * 0.7, 2 * th, str(movie.amount_positive_reviews), border=1)
        pdf.cell(
            col_width * 0.7,
            2 * th,
            str(movie.amount_positive_reviews + movie.amount_negative_reviews),
            border=1,
        )
        pdf.cell(col_width * 0.7, 2 * th, str(movie.search_date.date()), border=1)
        pdf.ln(2 * th)

    pdf.output("app/static/download_file/history.pdf", "F")
