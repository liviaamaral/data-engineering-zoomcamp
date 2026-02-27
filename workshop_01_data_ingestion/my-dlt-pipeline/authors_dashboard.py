
import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import dlt
    import ibis
    return dlt, ibis, mo


@app.cell
def _(mo):
    mo.md("""
    # 📚 Open Library — Top 10 Authors by Book Count
    """)
    return


@app.cell
def _(dlt):
    # Connect to the dlt pipeline dataset via ibis
    pipeline = dlt.attach(pipeline_name="open_library_pipeline")
    dataset = pipeline.dataset()
    ibis_con = dataset.ibis()
    dataset_name = pipeline.dataset_name
    return dataset_name, ibis_con


@app.cell
def _(dataset_name, ibis, ibis_con):
    # Get ibis table expressions
    # In the trending API, author names are in books__author_name with a "value" column
    books_expr = ibis_con.table("books", database=dataset_name)
    author_names_expr = ibis_con.table("books__author_name", database=dataset_name)

    # Join author_name with books and count books per author
    top_authors = (
        author_names_expr
        .join(
            books_expr.select("_dlt_id", "title"),
            author_names_expr["_dlt_parent_id"] == books_expr["_dlt_id"],
        )
        .group_by(author_names_expr["value"])
        .aggregate(book_count=author_names_expr["value"].count())
        .rename({"name": "value"})
        .order_by(ibis.desc("book_count"))
        .limit(10)
        .execute()
    )
    return (top_authors,)


@app.cell
def _(mo, top_authors):
    mo.ui.table(top_authors, label="Top 10 Authors by Book Count")
    return


@app.cell
def _(top_authors):
    import altair as alt

    chart = (
        alt.Chart(top_authors)
        .mark_bar()
        .encode(
            x=alt.X("book_count:Q", title="Number of Books"),
            y=alt.Y("name:N", sort="-x", title="Author"),
            color=alt.Color(
                "book_count:Q",
                scale=alt.Scale(scheme="blues"),
                legend=None,
            ),
            tooltip=["name", "book_count"],
        )
        .properties(
            title="Top 10 Authors by Book Count",
            width=600,
            height=350,
        )
    )
    chart
    return


if __name__ == "__main__":
    app.run()
