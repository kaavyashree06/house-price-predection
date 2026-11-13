
# ==========================================
# ANALYTICS
# ==========================================

elif page == "Analytics":

    st.title("Property Analytics")
    st.write("Your property prediction insights at a glance.")

    history = st.session_state.history

    if history:

        df = pd.DataFrame(history)

        total = len(df)
        average = df["Estimated Price"].mean()
        highest = df["Estimated Price"].max()
        lowest = df["Estimated Price"].min()

        # SUMMARY CARDS
        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Predictions", total)
        c2.metric("Average Price", f"${average:,.0f}")
        c3.metric("Highest Price", f"${highest:,.0f}")
        c4.metric("Lowest Price", f"${lowest:,.0f}")

        st.markdown("---")

        # PRICE TREND
        st.subheader("Property Price Trends")

        chart_df = df[["Property", "Estimated Price"]].copy()
        chart_df.index = range(1, len(chart_df) + 1)

        st.line_chart(
            chart_df["Estimated Price"],
            x_label="Prediction Number",
            y_label="Estimated Price (USD)"
        )

        st.markdown("---")

        # PROPERTY COMPARISON
        st.subheader("Property Price Comparison")

        st.bar_chart(
            chart_df.set_index("Property"),
            y="Estimated Price"
        )

        st.markdown("---")

        # RECENT ACTIVITY
        st.subheader("Recent Prediction Activity")

        display_df = df[
            ["Property", "Estimated Price", "Date"]
        ].copy()

        display_df["Estimated Price"] = display_df[
            "Estimated Price"
        ].map(lambda x: f"${x:,.2f}")

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No analytics available yet. "
            "Make your first property prediction to see your insights."
        )

