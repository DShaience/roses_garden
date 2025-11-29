from typing import List, Dict, Tuple


# example field 
test_field_height = 6
test_field_width = 4

# Purchased squares
test_purchased_squares = [
    (0, 2),  # row 0, col 2
    (1, 0),  # row 1, col 0
]

# Remember that the the grid is specified (cost, roses) --> (3, 10) means 10 roses at cost 3
# Squares with roses 
test_location_roses = {
    (0, 0): 1,
    (0, 2): 10,
    (1, 0): 4,
    (1, 3): 2,
    (2, 1): 4,
    (2, 2): 5,
    (2, 3): 1,
    (3, 0): 2,
    (3, 2): 9,
    (4, 0): 3,
    (4, 2): 14,
    (5, 0): 5,
    (5, 2): 1,
    (5, 3): 100,
}

# Squares with non-zero cost
test_location_costs = {
    (0, 2): 1,
    (1, 0): 1,
    (1, 3): 5,
    (2, 1): 2,
    (2, 2): 3,
    (2, 3): 1,
    (3, 0): 1,
    (3, 2): 2,
    (4, 0): 2,
    (4, 2): 20,
    (5, 0): 1,
    (5, 2): 10,
    (5, 3): 1,
}

class RosesField:
    def __init__(self, field_width: int, field_height: int,
            purchased_squares: List[Tuple[int, int]],
            location_roses: Dict[Tuple[int, int], int],
            location_costs: Dict[Tuple[int, int], float],
            garden_width: int, garden_height: int
        ):
        self.field_width = field_width
        self.field_height = field_height
        self.purchased_squares = purchased_squares
        self.location_roses = location_roses
        self.location_costs = location_costs
        self.garden_width = garden_width
        self.garden_height = garden_height
        
        # Using a cumulative sum array for memory efficiency, as requested (i.e., O(N) memory was deemed acceptable)
        self.cost_prefix = [[0] * (field_width + 1) for _ in range(field_height + 1)]
        self.roses_prefix = [[0] * (field_width + 1) for _ in range(field_height + 1)]
        self.purchased_prefix = [[0] * (field_width + 1) for _ in range(field_height + 1)]
        
        # Storing purchased squares for O(1) lookup. In a worst-case scenario this can be O(N) memory, which is still acceptable,
        # though I'm expecting that purchased squares are sparse.
        self.purchased_set = set(purchased_squares)
        
        # Compute prefix sums (cumulative sums)
        self._compute_prefix_sums()

    def _compute_prefix_sums(self):
        """
        Compute cumulative sum arrays for cost, roses, and purchased squares.
        This makes it very memory and runtime efficient to query sums over any rectangle in O(1) time,
        saving us from O(HxW) time per query.
        """
        for r in range(1, self.field_height + 1):
            for c in range(1, self.field_width + 1):
                cost_val = self.location_costs.get((r-1, c-1), 0)
                roses_val = self.location_roses.get((r-1, c-1), 0)
                purchased_val = 1 if (r-1, c-1) in self.purchased_set else 0
                
                # Prefix sum formula: current + left + top - top-left
                self.cost_prefix[r][c] = (cost_val + 
                                         self.cost_prefix[r-1][c] + 
                                         self.cost_prefix[r][c-1] - 
                                         self.cost_prefix[r-1][c-1])
                
                self.roses_prefix[r][c] = (roses_val + 
                                          self.roses_prefix[r-1][c] + 
                                          self.roses_prefix[r][c-1] - 
                                          self.roses_prefix[r-1][c-1])
                
                self.purchased_prefix[r][c] = (purchased_val + 
                                              self.purchased_prefix[r-1][c] + 
                                              self.purchased_prefix[r][c-1] - 
                                              self.purchased_prefix[r-1][c-1])

    def _get_rectangle_sum(self, prefix, r1, c1, h, w):
        """Get sum of rectangle starting at (r1,c1) with dimensions hxw using prefix sums."""
        r2 = r1 + h
        c2 = c1 + w
        return (prefix[r2][c2] - 
                prefix[r1][c2] - 
                prefix[r2][c1] + 
                prefix[r1][c1])
    
    def _has_purchased_square(self, r, c, h, w):
        """
        Check if rectangle starting at (r,c) with dimensions hxw contains any purchased square.
        Uses prefix sum for O(1) lookup instead of O(HxW).
        """
        count = self._get_rectangle_sum(self.purchased_prefix, r, c, h, w)
        return count > 0

    def set_garden_shape(self, garden_width: int, garden_height: int):
        self.garden_width = garden_width
        self.garden_height = garden_height


    def find_best_garden(self, budget: float) -> tuple:
        best_roses = -1
        best_position = (-1, -1)
        
        # loop over the valid top-left positions
        for r in range(self.field_height - self.garden_height + 1):
            for c in range(self.field_width - self.garden_width + 1):
                if self._has_purchased_square(r, c, self.garden_height, self.garden_width):
                    continue
                
                # Get cost and roses for this rectangle (O(1) due to prefix sums)
                cost = self._get_rectangle_sum(self.cost_prefix, r, c, self.garden_height, self.garden_width)
                roses = self._get_rectangle_sum(self.roses_prefix, r, c, self.garden_height, self.garden_width)
                
                # Check if within budget and better than current best
                if cost <= budget and roses > best_roses:
                    best_roses = roses
                    best_position = (r, c)
        
        return best_position


if __name__ == "__main__":
    test_garden_height = 2
    test_garden_width = 2
    budget = 10
    roses_field = RosesField(
        test_field_width, test_field_height,
        test_purchased_squares,
        test_location_roses,
        test_location_costs,
        test_garden_width, test_garden_height
    )
    best_position = roses_field.find_best_garden(budget=budget)
    # Row, Col of top-left corner
    print(best_position)