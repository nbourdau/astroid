# Licensed under the LGPL: https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html
# For details: https://github.com/PyCQA/astroid/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/astroid/blob/main/CONTRIBUTORS.txt

import unittest

try:
    import numpy  # pylint: disable=unused-import

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

from astroid import builder


@unittest.skipUnless(HAS_NUMPY, "This test requires the numpy library.")
class BrainNumpyCoreFromNumericTest(unittest.TestCase):
    """
    Test the numpy core fromnumeric brain module
    """

    numpy_functions = (("sum", "[1, 2]"),)

    def _inferred_numpy_func_call(self, func_name, *func_args):
        node = builder.extract_node(
            f"""
        import numpy as np
        func = np.{func_name:s}
        func({','.join(func_args):s})
        """
        )
        return node.infer()

    def test_numpy_function_calls_inferred_as_ndarray(self):
        """
        Test that calls to numpy functions are inferred as numpy.ndarray
        """
        licit_array_types = (".ndarray",)
        for func_ in self.numpy_functions:
            with self.subTest(typ=func_):
                inferred_values = list(self._inferred_numpy_func_call(*func_))
                self.assertTrue(
                    len(inferred_values) == 1,
                    msg=f"Too much inferred value for {func_[0]:s}",
                )
                self.assertTrue(
                    inferred_values[-1].pytype() in licit_array_types,
                    msg=f"Illicit type for {func_[0]:s} ({inferred_values[-1].pytype()})",
                )


if __name__ == "__main__":
    unittest.main()
