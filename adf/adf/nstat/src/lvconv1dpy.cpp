/**
 * Python interface to the lvconv1d functions
 * @author: Joseph Jennings
 * @version: 2020.03.08
 */

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include "lvconv1d.h"

namespace py = pybind11;

PYBIND11_MODULE(lvconv1d,m) {
  m.doc() = "Estimation of linearly-varying PEFs in 1D";
  m.def("lvconv1df_fwd",[](
      int nb,
      py::array_t<int, py::array::c_style> b,
      py::array_t<int, py::array::c_style> e,
      int nlag,
      py::array_t<int, py::array::c_style> lag,
      int n,
      py::array_t<float, py::array::c_style> aux,
      py::array_t<float, py::array::c_style> flt,
      py::array_t<float, py::array::c_style> dat
      )
      {
        lvconv1df_fwd(nb, b.mutable_data(), e.mutable_data(), nlag, lag.mutable_data(), n, aux.mutable_data(),
            flt.mutable_data(), dat.mutable_data());
      },
      py::arg("nb"), py::arg("b"), py::arg("e"), py::arg("nlag"), py::arg("lag"),
      py::arg("n"), py::arg("aux"), py::arg("flt"), py::arg("dat")
      );
  m.def("lvconv1df_adj",[](
      int nb,
      py::array_t<int, py::array::c_style> b,
      py::array_t<int, py::array::c_style> e,
      int nlag,
      py::array_t<int, py::array::c_style> lag,
      int n,
      py::array_t<float, py::array::c_style> aux,
      py::array_t<float, py::array::c_style> flt,
      py::array_t<float, py::array::c_style> dat
      )
      {
        lvconv1df_adj(nb, b.mutable_data(), e.mutable_data(), nlag, lag.mutable_data(), n, aux.mutable_data(),
            flt.mutable_data(), dat.mutable_data());
      },
      py::arg("nb"), py::arg("b"), py::arg("e"), py::arg("nlag"), py::arg("lag"),
      py::arg("n"), py::arg("aux"), py::arg("flt"), py::arg("dat")
      );
}
