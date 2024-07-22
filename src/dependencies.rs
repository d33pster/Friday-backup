use std::{fs::File, io::copy};

// import pyo3 for defining python modules, functions
// and as such
use pyo3::prelude::*;

// import tokio's runtime struct
use tokio::runtime::Runtime;


// define a class Install
#[pyclass]
pub struct Install {
    file: String,
}

// define class methods
#[pymethods]
impl Install {
    // define __init__
    #[new]
    pub fn new(file: &str) -> Self {
        Self {
            file: file.to_string(),
        }
    }

    // download file
    pub fn download_and_place(&self) -> PyResult<()> {
        let runtime = Runtime::new().unwrap();
        
        runtime.block_on(async {
            match download_file_from_latest_release(&self.file).await {
                Ok(_) => Ok(()),
                Err(e) => Err(pyo3::exceptions::PyIOError::new_err(e.to_string())),
            }
        })
    }

}

async fn download_file_from_latest_release(filename: &str) -> Result<(), Box<dyn std::error::Error>> {
    let api_url = "https://ap.github.com/repos/d33pster/Friday/releases/latest";

    let client = reqwest::Client::new();
    let resp = client.get(api_url)
        .header("User-Agent", "reqwest")
        .send()
        .await?
        .json::<serde_json::Value>()
        .await?;

    if let Some(assets) = resp["assets"].as_array() {
        for asset in assets {
            if let Some(name) = asset["name"].as_str() {
                if name == filename {
                    if let Some(download_url) = asset["browser_download_url"].as_str() {
                        let response = client.get(download_url).send().await?;
                        let mut file = File::create(filename)?;
                        let content = response.bytes().await?;
                        copy(&mut content.as_ref(), &mut file)?;
                        return Ok(());
                    }
                }
            }
        }
    }

    Err(Box::new(std::io::Error::new(std::io::ErrorKind::NotFound, "File not found!")))
}

#[pymodule]
pub fn dependencies(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Install>()?;
    Ok(())
}