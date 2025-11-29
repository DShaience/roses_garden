from typing import List, Dict, Tuple


# Field is 6 rows × 4 columns
test_field_height = 6
test_field_width = 4

test_garden_height = 3
test_garden_width = 3

# Purchased squares: the red squares from the figure
test_purchased_squares = [
    (0, 2),  # row 0, col 2
    (1, 0),  # row 1, col 0
]

# Squares with roses (>0)
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
        

    def _find_all_potential_gardens(self) -> List[Tuple[int, int]]:
        """Finding all potential gardens in the field. These are sub-rectangles of size garden_width x garden_height."""
        potential_gardens = []
        for row in range(self.field_height - self.garden_height + 1):
            for col in range(self.field_width - self.garden_width + 1):
                potential_gardens.append((row, col))
        return potential_gardens
        

    def set_garden_shape(self, garden_width: int, garden_height: int):
        """Setting the desired garden's shape"""
        pass

    def find_best_garden(self, budget: float) -> tuple:
        """Finding the best garden given budget"""
        pass


if __name__ == "__main__":
    roses_field = RosesField(
        test_field_width, test_field_height,
        test_purchased_squares,
        test_location_roses,
        test_location_costs,
        test_garden_width, test_garden_height
    )
    



