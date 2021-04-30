/**
 * Python interface to the lvconv2d functions
 * @author: Joseph Jennings
 * @version: 2020.03.11
 */

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include "lvconv2d.h"

namespace py = pybind11;

PYBIND11_MODULE(lvconv2d,m) {
  m.doc() = "Estimation of linearly-varying PEFs in 2D";
  m.def("lvconv2df_fwd",[](
      int nb,
      py::array_t<int, py::array::c_style> b1,
      py::array_t<int, py::array::c_style> e1,
      py::array_t<int, py::array::c_style> b2,
      py::array_t<int, py::array::c_style> e2,
      int nlag,
      py::array_t<int, py::array::c_style> lag1,
      py::array_t<int, py::array::c_style> lag2,
      int nd1,
      int nd2,
      py::array_t<float, py::array::c_style> aux,
      py::array_t<int, py::array::c_style> nf,
      py::array_t<float, py::array::c_style> flt,
      py::array_t<float, py::array::c_style> dat
      )
      {
        lvconv2df_fwd(nb, b1.mutable_data(), e1.mutable_data(), b2.mutable_data(), e2.mutable_data(),
            nlag, lag1.mutable_data(), lag2.mutable_data(), nd1, nd2, aux.mutable_data(),
            nf.mutable_data(), flt.mutable_data(), dat.mutable_data());
      },
      py::arg("nb"), py::arg("b1"), py::arg("e1"), py::arg("b2"), py::arg("e2"),
      py::arg("nlag"), py::arg("lag1"), py::arg("lag2"),
      py::arg("nd1"), py::arg("nd2"), py::arg("aux"), py::arg("nf"), py::arg("flt"), py::arg("dat")
      );
  m.def("lvconv2df_adj",[](
      int nb,
      py::array_t<int, py::array::c_style> b1,
      py::array_t<int, py::array::c_style> e1,
      py::array_t<int, py::array::c_style> b2,
      py::array_t<int, py::array::c_style> e2,
      int nlag,
      py::array_t<int, py::array::c_style> lag1,
      py::array_t<int, py::array::c_style> lag2,
      int nd1,
      int nd2,
      py::array_t<float, py::array::c_style> aux,
      py::array_t<int, py::array::c_style> nf,
      py::array_t<float, py::array::c_style> flt,
      py::array_t<float, py::array::c_style> dat
      )
      {
        lvconv2df_adj(nb, b1.mutable_data(), e1.mutable_data(), b2.mutable_data(), e2.mutable_data(),
            nlag, lag1.mutable_data(), lag2.mutable_data(), nd1, nd2, aux.mutable_data(),
            nf.mutable_data(), flt.mutable_data(), dat.mutable_data());
      },
      py::arg("nb"), py::arg("b1"), py::arg("e1"), py::arg("b2"), py::arg("e2"),
      py::arg("nlag"), py::arg("lag1"), py::arg("lag2"),
      py::arg("nd1"), py::arg("nd2"), py::arg("aux"), py::arg("nf"), py::arg("flt"), py::arg("dat")
      );
}
