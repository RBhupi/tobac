"""Tests for the iris/xarray conversion decorators"""

import pytest
import tobac
import tobac.testing
import xarray
import iris
from  iris.cube import Cube
import pandas as pd
from pandas.testing import assert_frame_equal
from copy import deepcopy
from tobac.utils import xarray_to_iris, iris_to_xarray, xarray_to_irispandas, irispandas_to_xarray

@pytest.mark.parametrize(
    "decorator, input_types, expected_internal_types, expected_output_type",
    [(xarray_to_iris, [xarray.DataArray, xarray.DataArray], [Cube, Cube], xarray.DataArray),
    (xarray_to_iris, [Cube, Cube], [Cube, Cube], Cube),
    (xarray_to_iris, [Cube, xarray.DataArray], [Cube, Cube], Cube),
    (xarray_to_iris, [xarray.DataArray, Cube], [Cube, Cube], xarray.DataArray),

    (iris_to_xarray, [Cube, Cube], [xarray.DataArray, xarray.DataArray], Cube),
    (iris_to_xarray, [xarray.DataArray, xarray.DataArray], [xarray.DataArray, xarray.DataArray], xarray.DataArray),
    (iris_to_xarray, [xarray.DataArray, Cube], [xarray.DataArray, xarray.DataArray], xarray.DataArray),
    (iris_to_xarray, [Cube, xarray.DataArray], [xarray.DataArray, xarray.DataArray], Cube),

    (xarray_to_irispandas, [xarray.DataArray, xarray.DataArray], [Cube, Cube], xarray.DataArray)]
)
def test_converting(decorator, input_types, expected_internal_types, expected_output_type):
    """Function to test if the xarray_to_iris decorator converts the correct
    types to the intended types"""

    def test_function_kwarg(test_input, kwarg=None):
        assert type(test_input) == expected_internal_types[0], "Expected internal type {}, but got {} for {}".format(expected_internal_types[0], type(test_input), decorator.__name__)
        assert type(kwarg) == expected_internal_types[1], "Expected internal type {}, but got {} for {} as keyword argument".format(expected_internal_types[1], type(kwarg), decorator.__name__)
        return (test_input)

    decorated_function_kwarg = decorator(test_function_kwarg)

    if input_types[0] == xarray.DataArray:
        data = xarray.DataArray.from_iris(tobac.testing.make_simple_sample_data_2D())
    elif input_types[0] == Cube:
        data = tobac.testing.make_simple_sample_data_2D()
    elif input_types[0] == xarray.Dataset:
        data = tobac.testing.generate_single_feature(1, 1).to_xarray()
    elif input_types[0] == pd.DataFrame:
        data = tobac.testing.generate_single_feature(1, 1)
    elif input_types[0] == int:
        data = 1

    if input_types[1] == xarray.DataArray:
        kwarg = xarray.DataArray.from_iris(tobac.testing.make_simple_sample_data_2D())
    elif input_types[1] == Cube:
        kwarg = tobac.testing.make_simple_sample_data_2D()
    elif input_types[1] == xarray.Dataset:
        kwarg = tobac.testing.generate_single_feature(1, 1).to_xarray()
    elif input_types[1] == pd.DataFrame:
        kwarg = tobac.testing.generate_single_feature(1, 1)
    elif input_types[1] == int:
        kwarg = 1

    output = decorated_function_kwarg(
        data, kwarg=kwarg
    )

    assert type(output) == expected_output_type, "Expected output type {}, but got {} for {}".format(expected_output_type, type(output), decorator.__name__)

def test_converting_xarray_to_iris():
    """Function to test if the xarray_to_iris decorator converts the correct
    types to the intended types"""

    def test_function(test_input):
        assert type(test_input) == iris.cube.Cube
        return test_input

    def test_function_kwargs(test_input_1, test_input_2, kwarg_1=None, kwarg_2=None):
        assert type(test_input_1) == iris.cube.Cube
        assert type(test_input_2) == iris.cube.Cube
        assert type(kwarg_1) == iris.cube.Cube
        assert type(kwarg_2) == iris.cube.Cube
        return (test_input_1, test_input_2)

    decorated_function = tobac.utils.xarray_to_iris(test_function)
    decorated_function_kwargs = tobac.utils.xarray_to_iris(test_function_kwargs)

    data = xarray.DataArray.from_iris(tobac.testing.make_simple_sample_data_2D())

    output = decorated_function(data)
    output_kwargs_1, output_kwargs_2 = decorated_function_kwargs(
        data, data, kwarg_1=data, kwarg_2=data
    )

    assert type(output) == xarray.DataArray
    assert type(output_kwargs_1) == xarray.DataArray
    assert type(output_kwargs_2) == xarray.DataArray


def test_converting_iris_to_xarray():
    """Function to test if the iris_to_xarray decorator converts the correct
    types to the intended types"""

    def test_function(test_input):
        assert type(test_input) == xarray.DataArray
        return test_input

    def test_function_kwargs(test_input_1, test_input_2, kwarg_1=None, kwarg_2=None):
        assert type(test_input_1) == xarray.DataArray
        assert type(test_input_2) == xarray.DataArray
        assert type(kwarg_1) == xarray.DataArray
        assert type(kwarg_2) == xarray.DataArray
        return (test_input_1, test_input_2)

    decorated_function = tobac.utils.iris_to_xarray(test_function)
    decorated_function_kwargs = tobac.utils.iris_to_xarray(test_function_kwargs)

    data = tobac.testing.make_simple_sample_data_2D()

    output = decorated_function(data)
    output_kwargs_1, output_kwargs_2 = decorated_function_kwargs(
        data, data, kwarg_1=data, kwarg_2=data
    )

    assert type(output) == iris.cube.Cube
    assert type(output_kwargs_1) == iris.cube.Cube
    assert type(output_kwargs_2) == iris.cube.Cube


def test_converting_xarray_to_irispandas():
    """Function to test if the xarray_to_irispandas decorator converts the correct
    types to the intended types"""

    def test_function_iris(test_input):
        assert type(test_input) == iris.cube.Cube
        return test_input

    def test_function_dataframe(test_input):
        assert type(test_input) == pd.DataFrame
        return test_input

    def test_function_kwargs(test_input_1, test_input_2, kwarg_1=None, kwarg_2=None):
        assert type(test_input_1) == iris.cube.Cube
        assert type(test_input_2) == pd.DataFrame
        assert type(kwarg_1) == iris.cube.Cube
        assert type(kwarg_2) == pd.DataFrame
        return (test_input_1, test_input_2)

    decorated_function_iris = tobac.utils.xarray_to_irispandas(test_function_iris)
    decorated_function_dataframe = tobac.utils.xarray_to_irispandas(
        test_function_dataframe
    )
    decorated_function_kwargs = tobac.utils.xarray_to_irispandas(test_function_kwargs)

    feature = tobac.testing.generate_single_feature(1, 1).to_xarray()
    data = xarray.DataArray.from_iris(tobac.testing.make_simple_sample_data_2D())

    output_iris = decorated_function_iris(data)
    output_dataframe = decorated_function_dataframe(feature)
    output_kwargs_1, output_kwargs_2 = decorated_function_kwargs(
        data, feature, kwarg_1=data, kwarg_2=feature
    )

    assert type(output_iris) == xarray.DataArray
    assert type(output_dataframe) == xarray.Dataset
    assert type(output_kwargs_1) == xarray.DataArray
    assert type(output_kwargs_2) == xarray.Dataset


def test_converting_irispandas_to_xarray():
    """Function to test if the irispandas_to_xarray decorator converts the correct
    types to the intended types"""

    def test_function_iris(test_input):
        assert type(test_input) == xarray.DataArray
        return test_input

    def test_function_dataframe(test_input):
        assert type(test_input) == xarray.Dataset
        return test_input

    def test_function_kwargs(test_input_1, test_input_2, kwarg_1=None, kwarg_2=None):
        assert type(test_input_1) == xarray.DataArray
        assert type(test_input_2) == xarray.Dataset
        assert type(kwarg_1) == xarray.DataArray
        assert type(kwarg_2) == xarray.Dataset
        return (test_input_1, test_input_2)

    decorated_function_iris = tobac.utils.irispandas_to_xarray(test_function_iris)
    decorated_function_dataframe = tobac.utils.irispandas_to_xarray(
        test_function_dataframe
    )
    decorated_function_kwargs = tobac.utils.irispandas_to_xarray(test_function_kwargs)

    feature = tobac.testing.generate_single_feature(1, 1)
    data = tobac.testing.make_simple_sample_data_2D()

    output_iris = decorated_function_iris(data)
    output_dataframe = decorated_function_dataframe(feature)
    output_kwargs_1, output_kwargs_2 = decorated_function_kwargs(
        data, feature, kwarg_1=data, kwarg_2=feature
    )

    assert type(output_iris) == iris.cube.Cube
    assert type(output_dataframe) == pd.DataFrame
    assert type(output_kwargs_1) == iris.cube.Cube
    assert type(output_kwargs_2) == pd.DataFrame


def test_xarray_workflow():
    """Test comparing the outputs of the standard functions of tobac for a test dataset
    with the output of the same functions decorated with tobac.utils.xarray_to_iris"""

    data = tobac.testing.make_sample_data_2D_3blobs()
    data_xarray = xarray.DataArray.from_iris(deepcopy(data))

    # Testing the get_spacings utility
    get_spacings_xarray = tobac.utils.xarray_to_iris(tobac.utils.get_spacings)
    dxy, dt = tobac.utils.get_spacings(data)
    dxy_xarray, dt_xarray = get_spacings_xarray(data_xarray)

    assert dxy == dxy_xarray
    assert dt == dt_xarray

    # Testing feature detection
    feature_detection_xarray = tobac.utils.xarray_to_iris(
        tobac.feature_detection.feature_detection_multithreshold
    )
    features = tobac.feature_detection.feature_detection_multithreshold(data, dxy, 1.0)
    features_xarray = feature_detection_xarray(data_xarray, dxy_xarray, 1.0)

    assert_frame_equal(features, features_xarray)

    # Testing the segmentation
    segmentation_xarray = tobac.utils.xarray_to_iris(tobac.segmentation.segmentation)
    mask, features = tobac.segmentation.segmentation(features, data, dxy, 1.0)
    mask_xarray, features_xarray = segmentation_xarray(
        features_xarray, data_xarray, dxy_xarray, 1.0
    )

    assert (mask.data == mask_xarray.to_iris().data).all()

    # testing tracking
    tracking_xarray = tobac.utils.xarray_to_iris(tobac.tracking.linking_trackpy)
    track = tobac.tracking.linking_trackpy(features, data, dt, dxy, v_max=100.0)
    track_xarray = tracking_xarray(
        features_xarray, data_xarray, dt_xarray, dxy_xarray, v_max=100.0
    )

    assert_frame_equal(track, track_xarray)
