import numpy as np
import ecce.utils as utils


def describe_utils():
    def categories_to_selections():
        m = np.array([[0, 1, 0, 1, 0]])
        expected = np.array([[0, 1, 0, 0, 0],
                             [0, 0, 0, 1, 0]])

        assert (utils.categories_to_selections(m) == expected).all()

    def n_max_indices():
        m = np.array([1, 5, 3, 8, 4, 1, 9, 11, 22, 1])
        expected = np.array([8, 7, 6, 3, 1])

        assert (utils.n_max_indices(m) == expected).all()
