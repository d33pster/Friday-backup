use pyo3::prelude::*;
// use pyo3::wrap_pymodule;

mod tts;

// add the module
#[pymodule]
#[pyo3(name = "rust")]
fn rust(py: Python<'_> ,m: &Bound<'_, PyModule>) -> PyResult<()> {
    let tts = PyModule::new_bound(py, "tts")?;
    tts.add_class::<tts::Voice>()?;
    m.add_submodule(&tts)?;
    Ok(())
}

// ------------------------------------------------------------------
