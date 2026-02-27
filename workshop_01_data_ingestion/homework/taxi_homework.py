import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import dlt
    import altair as alt

    return alt, dlt, mo


@app.cell
def _(dlt):
    pipeline = dlt.attach(pipeline_name="taxi_pipeline")
    dataset = pipeline.dataset()
    ibis_con = dataset.ibis()
    dataset_name = pipeline.dataset_name
    return dataset_name, ibis_con


@app.cell
def _(mo):
    mo.md("""
    # 🚕 NYC Taxi Rides — Homework Answers
    """)
    return


@app.cell
def _(alt, dataset_name, ibis_con, mo):
    import ibis as _ibis
    rides = ibis_con.table("rides", database=dataset_name)

    _date_range = rides.aggregate(
        start_date=rides["trip_pickup_date_time"].min(),
        end_date=rides["trip_pickup_date_time"].max(),
    ).execute()

    _trips_per_day = (
        rides
        .mutate(pickup_date=rides["trip_pickup_date_time"].date())
        .group_by("pickup_date")
        .aggregate(trip_count=rides["trip_pickup_date_time"].count())
        .order_by("pickup_date")
        .execute()
    )

    _start = str(_date_range["start_date"][0])[:10]
    _end = str(_date_range["end_date"][0])[:10]

    _chart = (
        alt.Chart(_trips_per_day)
        .mark_bar(color="#f7c948")
        .encode(
            x=alt.X("pickup_date:T", title="Pickup Date"),
            y=alt.Y("trip_count:Q", title="Number of Trips"),
            tooltip=["pickup_date:T", "trip_count:Q"],
        )
        .properties(title="Number of Trips per Day", width=640, height=220)
    )
    mo.vstack([
        mo.md("## Question 1: Start and end date of the dataset"),
        mo.callout(mo.md(f"**Start date:** `{_start}`  \n**End date:** `{_end}`"), kind="success"),
        mo.ui.altair_chart(_chart),
    ])
    return (rides,)


@app.cell
def _(alt, mo, rides):
    _payment_df = (
        rides
        .group_by("payment_type")
        .aggregate(trip_count=rides["payment_type"].count())
        .execute()
        .sort_values("trip_count", ascending=False)
        .reset_index(drop=True)
    )
    _total = _payment_df["trip_count"].sum()
    _payment_df["pct"] = (_payment_df["trip_count"] / _total * 100).round(2)

    _credit_pct = float(
        _payment_df.loc[
            _payment_df["payment_type"].str.lower() == "credit", "pct"
        ].values[0]
    )

    _chart = (
        alt.Chart(_payment_df)
        .mark_arc(innerRadius=70)
        .encode(
            theta=alt.Theta("trip_count:Q"),
            color=alt.Color("payment_type:N", legend=alt.Legend(title="Payment Type")),
            tooltip=["payment_type:N", "trip_count:Q", "pct:Q"],
        )
        .properties(title="Payment Type Distribution", width=360, height=320)
    )
    mo.vstack([
        mo.md("## Question 2: Proportion of trips paid with credit card"),
        mo.callout(mo.md(f"**Credit card proportion:** `{_credit_pct:.2f}%`"), kind="success"),
        mo.ui.altair_chart(_chart),
    ])
    return


@app.cell
def _(alt, mo, rides):
    _total_tips = float(rides["tip_amt"].sum().execute())

    _tips_dist = (
        rides.filter(rides["tip_amt"] > 0)
        .select("tip_amt")
        .execute()
    )

    _chart = (
        alt.Chart(_tips_dist)
        .mark_bar(color="#3b82f6")
        .encode(
            x=alt.X("tip_amt:Q", bin=alt.Bin(maxbins=40), title="Tip Amount ($)"),
            y=alt.Y("count():Q", title="Number of Trips"),
            tooltip=["count():Q"],
        )
        .properties(title="Tip Amount Distribution (non-zero tips)", width=640, height=250)
    )
    mo.vstack([
        mo.md("## Question 3: Total amount generated in tips"),
        mo.callout(mo.md(f"**Total tips:** `${_total_tips:,.2f}`"), kind="success"),
        mo.ui.altair_chart(_chart),
    ])
    return


if __name__ == "__main__":
    app.run()
