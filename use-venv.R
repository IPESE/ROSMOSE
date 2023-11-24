library(reticulate)
if (length(rmarkdown::metadata$venv) > 0) {venv <- rmarkdown::metadata$venv} else {venv <- "./venv"}
use_virtualenv(venv, required = T)