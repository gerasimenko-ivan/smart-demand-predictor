class InventoryOptimizer:

    def calculate_reorder(
        self,
        current_stock,
        predicted_demand
    ):

        reorder = predicted_demand - current_stock

        if reorder < 0:
            reorder = 0

        return round(reorder)

    def calculate_stock_risk(
            self,
            current_stock,
            predicted_demand
    ):

        remaining = current_stock - predicted_demand

        if remaining < 0:
            return "🔴High"

        if remaining < 10:
            return "🟠Medium"

        return "🟢Low"