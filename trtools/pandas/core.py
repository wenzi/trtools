"""
    Mainly has simple monkey patches for easier data access. 
"""
from pandas import Panel, DataFrame, MultiIndex, Series
from pandas.core.groupby import DataFrameGroupBy, PanelGroupBy, GroupBy

from trtools.monkey import patch, patch_prop

@patch(DataFrame)
def cols(self, *args):
    return self.xs(list(args), axis=1)

@patch(Series, 'dropper')
def dropper(self, value=None, *args, **kwargs):
    if value is None:
        return self.dropna(*args, **kwargs)
    return self.ix[self != value].dropna()

@patch(DataFrame, 'dropper')
def dropna_df(self, value=None, *args, **kwargs):
    if value is None:
        return self.dropna(*args, **kwargs)
    return self.ix[self != value].dropna()

@patch([DataFrame, Series])
def selectone(self, func):
    """
        A wrapper around select that only returns the first value
    """
    vals = self.select(func)
    if len(vals) > 0:
        return self.ix[vals.index[0]]

@patch(Series, 'show')
def show(self, val):
    """
        show(val)
        show all rows matching a value
        val can be a value or a func. 
    """
    if callable(val):
        func = np.vectorize(val)
        bools = func(self)
    else:
        bools = self == val
    return self[bools]

class PosIndexer(object):
    """
        Only indexes on int position. So if index is an IntIndex, it will never match
        the name. Only the position.
    """
    def __init__(self, obj):
        self.obj = obj
        self.get_func = self._set_get_item()

    def __getitem__(self, key):
        return self.get_func(key)

    def _set_get_item(self):
        if isinstance(self.obj, Panel):
            return self._getitem_panel
        if isinstance(self.obj, DataFrame):
            return self._getitem_dataframe
        if isinstance(self.obj, Series):
            return self._getitem_series

    def _getitem_panel(self, key):
        label = self.obj.major_axis[key]
        return self.obj.major_xs(label)

    def _getitem_dataframe(self, key):
        label = self.obj.index[key]
        return self.obj.xs(label)

    def _getitem_series(self, key):
        label = self.obj.index[key]
        return self.obj[label]

@patch_prop([Panel, DataFrame, Series], 'rx')
def rx(self):
    """
        For grabbing row-wise which means the axis that a DatetimeIndex would 
        normally be found
    """
    if not hasattr(self, '_rx'):
        self._rx = PosIndexer(self)

    return self._rx

