// tts lib for Friday - rust class 1

// use pyo3 to convert to python class
use pyo3::prelude::*;

// use crate::rust::_PYO3_DEF;

// use tts_rust lib for text to speech conversion
use tts_rust::languages::Languages;
use tts_rust::tts::GTTSClient;

// define class
#[pyclass]
pub struct Voice {
    narrator: GTTSClient,
}

// define class methods
#[pymethods]
impl Voice {
    // __init__ function
    #[new]
    pub fn new(volume: f32) -> PyResult<Self> {
        Ok(Voice {
            narrator: GTTSClient {
                volume,
                language: Languages::English,
                tld: "co.in",
            }
        })
    }

    // speak function
    pub fn speak(&mut self, text: &str) -> PyResult<()> {
        self.narrator.speak(text).map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;
        Ok(())
    }

    // save function
    pub fn save(&mut self, text: &str, path: &str) -> PyResult<()> {
        self.narrator.save_to_file(text, path).map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;
        Ok(())
    }
}

#[pymodule]
pub fn tts(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Voice>()?;
    Ok(())
}