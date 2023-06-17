import logging

import pandas as pd
import pytest

logger = logging.getLogger()

from bsp.lib import Preprocessor

class TestPreprocessor:
    @pytest.fixture
    def preprocessor(self):
        return Preprocessor("database")

    def test_preprocessor_init(self, preprocessor):
        pass

    def test_preprocessor_get_table(self, preprocessor):
        tab = preprocessor.get_table()
        tab.year = pd.to_numeric(tab.year)
        expected_first_part = pd.DataFrame({
            'year': [1920, 1940],
            'region': ["Brasil", "Brasil"],
            'production': [0, 1928.0],
            'area': [0.0, 0.0],
        })
        expected_last_part = pd.DataFrame({
            'year': [2022, 2023],
            'region': ["Sul", "Sul"],
            'production': [23690251.0, 40129200.0],
            'area': [12689049.0, 13201434.0],
        })
        actual_last_part = tab.iloc[-2:].reset_index(drop=True)
        assert tab.iloc[:2].equals(expected_first_part)
        assert actual_last_part.equals(expected_last_part)
