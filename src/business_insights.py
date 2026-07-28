class BusinessInsightGenerator:

    def generate(
            self,
            product,
            predicted_demand,
            current_stock,
            reorder_quantity,
            stock_risk,
            feature_importance
    ):

        insights = []

        # Demand explanation
        if predicted_demand > current_stock:
            insights.append(
                f"⚠️ Expected demand ({predicted_demand} items) "
                f"is higher than current inventory ({current_stock} items)."
            )
        else:
            insights.append(
                f"✅ Current inventory ({current_stock} items) "
                f"covers predicted demand ({predicted_demand} items)."
            )


        # Reorder explanation
        if reorder_quantity > 0:

            insights.append(
                f"📦 Recommended reorder: {reorder_quantity} items "
                f"to avoid potential shortage."
            )

        else:

            insights.append(
                "✅ No additional stock is required at this time."
            )


        # Risk explanation
        if stock_risk == "High":

            insights.append(
                "🔴 High stock risk detected. "
                "Current inventory may not satisfy expected demand."
            )

        elif stock_risk == "Medium":

            insights.append(
                "🟠 Medium stock risk. "
                "Inventory should be monitored."
            )

        else:

            insights.append(
                "🟢 Low stock risk. Inventory level looks healthy."
            )


        # Feature importance explanation
        if feature_importance is not None:

            top_feature = self.friendly_feature_name(
                feature_importance.iloc[0]["Feature"]
            )

            top_value = (
                feature_importance.iloc[0]["Importance"] * 100
            )

            top_value = round(top_value, 2)

            insights.append(
                f"✨ AI explanation: The strongest factor "
                f"affecting this forecast is '{top_feature}' "
                f"({top_value}% importance)."
            )


        return insights

    def friendly_feature_name(self, feature):

        names = {
            "Average3Days": "recent 3-day sales trend",
            "Average7Days": "weekly demand trend",
            "Average14Days": "two-week demand pattern",
            "Average30Days": "monthly demand pattern",
            "YesterdaySales": "previous day sales",
            "LastWeekSales": "previous week sales",
            "Stock_Start_Count": "current inventory level",
            "DayOfWeek": "weekly shopping pattern",
            "DayOfYear": "seasonal calendar pattern",
        }

        return names.get(feature, feature)