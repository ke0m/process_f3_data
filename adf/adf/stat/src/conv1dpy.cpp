/**
 * Python interface to the conv1d functions
 * @author: Joseph Jennings
 * @version: 2020.11.19
 */

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include "conv1d.h"

namespace py = pybind11;

PYBIND11_MODULE(conv1d,m) {
  m.doc() = "Estimation of PEFs in 1D";
  m.def("conv1df_fwd",[](
      int nlag,
      py::array_t<int, py::array::c_style> lag,
      int n,
      py::array_t<float, py::array::c_style> aux,
      py::array_t<float, py::array::c_style> flt,
      py::array_t<float, py::array::c_style> dat
      )
      {
        conv1df_fwd(nlag, lag.mutable_data(), n, aux.mutable_data(),
            flt.mutable_data(), dat.mutable_data());
      },
      py::arg("nlag"), py::arg("lag"), py::arg("n"),
      py::arg("aux"), py::arg("flt"), py::arg("dat")
      );
  m.def("conv1df_adj",[](
      int nlag,
      py::array_t<int, py::array::c_style> lag,
      int n,
      py::array_t<float, py::array::c_style> aux,
      py::array_t<float, py::array::c_style> flt,
      py::array_t<float, py::array::c_style> dat
      )
      {
        conv1df_adj(nlag, lag.mutable_data(), n, aux.mutable_data(),
            flt.mutable_data(), dat.mutable_data());
      },
      py::arg("nlag"), py::arg("lag"), py::arg("n"),
      py::arg("aux"), py::arg("flt"), py::arg("dat")
      );
  m.def("conv1dm_fwd",[](
      int nlag,
      py::array_t<int, py::array::c_style> lag,
      int n,
      py::array_t<float, py::array::c_style> flt,
      py::array_t<float, py::array::c_style> mod,
      py::array_t<float, py::array::c_style> dat
      )
      {
        conv1dm_fwd(nlag, lag.mutable_data(), n, flt.mutable_data(),
            mod.mutable_data(), dat.mutable_data());
      },
      py::arg("nlag"), py::arg("lag"), py::arg("n"),
      py::arg("flt"), py::arg("mod"), py::arg("dat")
      );
  m.def("conv1dm_adj",[](
      int nlag,
      py::array_t<int, py::array::c_style> lag,
      int n,
      py::array_t<float, py::array::c_style> flt,
      py::array_t<float, py::array::c_style> mod,
      py::array_t<float, py::array::c_style> dat
      )
      {
        conv1dm_adj(nlag, lag.mutable_data(), n, flt.mutable_data(),
            mod.mutable_data(), dat.mutable_data());
      },
      py::arg("nlag"), py::arg("lag"), py::arg("n"),
      py::arg("flt"), py::arg("mod"), py::arg("dat")
      );
}
