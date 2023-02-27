from pathlib import Path
from unittest import mock

import pandas as pd
import pytest

from pypeds import C_A, EFC, EFD, FF1, FF2, HD, IC, ICAY, OM, SFA

loader_classes = (HD, IC, SFA, EFC, ICAY, OM, EFD, FF1, FF2, C_A)


def get_test_csv_path(loader_class) -> Path:
    csv_base_path = Path("./tests/static")
    csv_file_names = {
        "C_A": "c2020_a.csv",
        "EFC": "ef2017c.csv",
        "EFD": "ef2017d.csv",
        "FF1": "f1920_f1a.csv",
        "FF2": "f1920_f2.csv",
        "HD": "hd2020.csv",
        "IC": "ic2020.csv",
        "ICAY": "ic2009_ay.csv",
        "OM": "om2017.csv",
        "SFA": "sfa1617.csv",
    }
    return csv_base_path / csv_file_names[loader_class.__name__]


def get_survey_id(loader_class, year: int) -> str:
    survey_ids = {
        C_A: "C" + str(year) + "_A",
        EFC: "EF" + str(year) + "C",
        EFD: "EF" + str(year) + "D",
        FF1: "F" + str(year - 1)[2:] + str(year)[2:] + "_F1A",
        FF2: "F" + str(year - 1)[2:] + str(year)[2:] + "_F2",
        HD: "HD" + str(year),
        IC: "IC" + str(year),
        ICAY: "IC" + str(year) + "_AY",
        OM: "OM" + str(year),
        SFA: "SFA" + str(year - 1)[2:] + str(year)[2:],
    }
    return survey_ids[loader_class]


def get_url(survey_id: str):
    return f"https://nces.ed.gov/ipeds/datacenter/data/{survey_id}.zip"


@pytest.fixture
def ipeds_df():
    return pd.DataFrame({"UNITID": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})


@pytest.mark.parametrize("loader_class", loader_classes)
def test_classes_initialize_correct_instance_vars(loader_class):
    """Calling a loader class (e.g., `HD()`) creates two instance variables:
    a dataframe called `df` and an array of integers called `years`.
    """
    loader_inst = loader_class()
    inst_vars = [
        attr
        for attr in dir(loader_inst)
        if not callable(getattr(loader_inst, attr))
        and not attr.startswith("__")
    ]
    assert set(inst_vars) == set(["df", "years"])
    assert isinstance(loader_inst.df, pd.DataFrame)
    assert isinstance(loader_inst.years, list)


@pytest.mark.parametrize("loader_class", loader_classes)
def test_classes_initialize_with_single_default_year_in_list(loader_class):
    """Calling a loader class without passing in any arguments sets the `years`
    instance variable to a list with a single integer year in it.
    """
    loader_inst = loader_class()
    assert len(loader_inst.years) == 1
    assert isinstance(loader_inst.years[0], int)


@pytest.mark.parametrize("loader_class", loader_classes)
def test_passing_year_list_to_loader_populates_years_var(loader_class):
    """Passing one or more years in a list to the `years` parameter sets
    the instance's `years` variable to a list of those years.
    """
    loader_inst_one_year = loader_class(years=[2015])
    loader_inst_multi_year = loader_class(years=[2014, 2015, 2016])
    assert loader_inst_one_year.years == [2015]
    assert loader_inst_multi_year.years == [2014, 2015, 2016]


@pytest.mark.parametrize("loader_class", loader_classes)
def test_initial_dataframe_is_empty(loader_class):
    """The loader classes' `self.df` instance variable is initially empty."""
    loader_inst = loader_class()
    assert len(loader_inst.df) == 0


@mock.patch("pypeds.ipeds.os.remove")
@mock.patch("pypeds.ipeds.read_survey")
@mock.patch("pypeds.ipeds.zip_parser")
@pytest.mark.parametrize("loader_class", loader_classes)
def test_extract_requests_data_from_correct_url(
    mock_zip_parser, mock_read_survey, mock_remove, loader_class, ipeds_df
):
    """Calling `extract` on a loader class sends a GET request to the
    correct URL.
    """
    mock_read_survey.return_value = ipeds_df
    loader_inst = loader_class(years=[2015])
    loader_inst.extract()

    survey_id = get_survey_id(loader_class, 2015)
    url = get_url(survey_id)

    if loader_class != IC:
        mock_zip_parser.assert_called_with(url=url, survey=survey_id)

    # IC starting in 2014 combines IC and ADM
    else:
        assert mock_zip_parser.call_args_list[0] == mock.call(
            url="https://nces.ed.gov/ipeds/datacenter/data/IC2015.zip",
            survey="IC2015",
        )
        assert mock_zip_parser.call_args_list[1] == mock.call(
            url="https://nces.ed.gov/ipeds/datacenter/data/ADM2015.zip",
            survey="ADM2015",
        )


@mock.patch("pypeds.ipeds.os.remove")
@mock.patch("pypeds.ipeds.zip_parser")
@pytest.mark.parametrize("loader_class", loader_classes)
def test_extract_fills_df_with_data(
    mock_zip_parser, mock_remove, loader_class
):
    """Calling `extract` on a loader class fills the empty `df` instance
    variable with data.
    """
    mock_zip_parser.return_value = get_test_csv_path(loader_class)
    loader_inst = loader_class()
    loader_inst.extract()
    assert len(loader_inst.df) == 2


@mock.patch("pypeds.ipeds.read_survey")
@mock.patch("pypeds.ipeds.zip_parser")
@pytest.mark.parametrize("loader_class", loader_classes)
def test_extract_calls_supporting_funcs_once_for_each_year(
    mock_zip_parser, mock_reader, loader_class, ipeds_df
):
    """Calling `extract` on a loader class calls the `zip_parser` and
    `read_survey` functions once for each year included in the load class's
    `years` list argument.

    The exception to this is the `IC` loader class, which calls each function
    twice--once for the IC survey and once for the ADM survey, which it then
    merges together.
    """
    mock_reader.return_value = ipeds_df
    years = [2015, 2016, 2017]
    loader_inst = loader_class(years=years)
    loader_inst.extract()

    if loader_class.__name__ != "IC":
        assert mock_zip_parser.call_count == len(years)
        assert mock_reader.call_count == len(years)

    # `IC` loads both IC and ADM and merges them together
    else:
        assert mock_zip_parser.call_count == len(years) * 2
        assert mock_reader.call_count == len(years) * 2


@mock.patch("pypeds.ipeds.os.remove")
@mock.patch("pypeds.ipeds.read_survey")
@mock.patch("pypeds.ipeds.zip_parser")
@pytest.mark.parametrize("loader_class", loader_classes)
def test_extract_adds_year_columns_to_df(
    mock_zip_parser, mock_read_survey, mock_remove, loader_class, ipeds_df
):
    """Calling `extract` adds `survey_year` and `fall_year` columns to the `df`
    instance variable.
    """
    mock_read_survey.return_value = ipeds_df
    loader_inst = loader_class()
    loader_inst.extract()
    assert "survey_year" in loader_inst.df.columns
    assert "fall_year" in loader_inst.df.columns


@mock.patch("pypeds.ipeds.os.remove")
@mock.patch("pypeds.ipeds.read_survey")
@mock.patch("pypeds.ipeds.zip_parser")
@pytest.mark.parametrize("loader_class", loader_classes)
def test_extract_converts_df_columns_to_lowercase(
    mock_zip_parser, mock_read_survey, mock_remove, loader_class, ipeds_df
):
    """Calling `extract` makes all `df` instance variable columns lowercase."""
    mock_read_survey.return_value = ipeds_df
    loader_inst = loader_class()
    loader_inst.extract()
    assert all(col.islower() for col in loader_inst.df.columns)


@pytest.mark.parametrize("loader_class", loader_classes)
def test_load_returns_df_instance_var(loader_class):
    """Calling the `load()` method on a loader instance returns the instance's
    `df` variable.
    """
    loader_inst = loader_class()
    assert loader_inst.load() is loader_inst.df
