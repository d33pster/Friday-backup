use pyo3::prelude::*;
// use pyo3::wrap_pymodule;

mod tts;
mod dependencies;

// add the module
#[pymodule]
#[pyo3(name = "rust")]
fn rust(py: Python<'_> ,m: &Bound<'_, PyModule>) -> PyResult<()> {
    // add tts
    let tts = PyModule::new_bound(py, "tts")?;
    tts.add_class::<tts::Voice>()?;
    m.add_submodule(&tts)?;

    // add dependencies
    let dependencies = PyModule::new_bound(py, "dependencies")?;
    dependencies.add_class::<dependencies::Install>()?;
    m.add_submodule(&dependencies)?;
    Ok(())
}

// ------------------------------------------------------------------
