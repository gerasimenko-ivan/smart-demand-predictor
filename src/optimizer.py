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