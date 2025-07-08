from enum import Enum
import os

class Data(Enum):
    BRAND_DATA = "test_brand.csv"
    CLASS_DATA = "test_class.csv"
    GOODS_DATA = "test_goods.csv"
    UNIT_DATA = "test_unit.csv"

    @property
    def path(self):
        # Use a relative path based on the project structure
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(current_file_dir, '..', '..', 'test_data')
        return os.path.join(base_path, self.value)
