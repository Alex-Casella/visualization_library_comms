"""simple_eda -- a minimal, pandas-first visualization library.

Public API is re-exported from :mod:`simple_eda.core`:

    from simple_eda import Chart, line, bar, scatter, hist
"""

from .core import Chart, bar, hist, line, scatter

__version__ = "0.1.0"
__all__ = ["Chart", "line", "bar", "scatter", "hist"]
