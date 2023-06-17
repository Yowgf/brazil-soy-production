import logging

import pandas as pd
import pytest

logger = logging.getLogger()

from bsp.lib import Preprocessor

class TestPreprocessor:
    @pytest.fixture
    def preprocessor_default(self):
        return Preprocessor("database")

    @pytest.fixture
    def preprocessor_states(self):
        return Preprocessor("database", "states")

    def test_preprocessor_init(self, preprocessor_default):
        pass

    def test_preprocessor_get_table_default(self, preprocessor_default):
        tab = preprocessor_default.get_table()
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
        actual_first_part = tab.iloc[:2].reset_index(drop=True)
        actual_last_part = tab.iloc[-2:].reset_index(drop=True)
        print(actual_first_part.dtypes)
        print(expected_first_part.dtypes)
        assert actual_first_part.equals(expected_first_part)
        assert actual_last_part.equals(expected_last_part)

    def test_preprocessor_get_table_state(self, preprocessor_states):
        tab = preprocessor_states.get_table()
        expected_first_part = pd.DataFrame({
            'year': [1920, 1940],
            'region': ["Acre", "Acre"],
            'production': [0.0, 0.0],
            'area': [0.0, 0.0],
        })
        expected_last_part = pd.DataFrame({
            'year': [2022, 2023],
            'region': ["Tocantins", "Tocantins"],
            'production': [3369389.0, 3999595.0],
            'area': [1144764.0, 1194967.0],
        })
        actual_first_part = tab.iloc[:2].reset_index(drop=True)
        actual_last_part = tab.iloc[-2:].reset_index(drop=True)
        assert actual_first_part.equals(expected_first_part)
        assert actual_last_part.equals(expected_last_part)
