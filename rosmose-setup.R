knitr::opts_chunk$set(echo = F)
if (!requireNamespace("devtools"))
  install.packages('devtools')
if (!require("ipesedisplay"))
  devtools::install_git("https://gitlab:x9hrpufByd9LA8-SnLCi@gitlab.epfl.ch/ipese/r/ipese-packages/ipesedisplay.git")
if (!require("reticulate"))
  install.packages("reticulate")
if (!require("DiagrammeRsvg"))
  install.packages('DiagrammeRsvg')
if(!require('dplyr'))
  install.packages("dplyr", dependencies = T)
if(!require('plotly'))
  install.packages("plotly", dependencies = T)
if(!require('knitr'))
  install.packages("knitr", dependencies = T)
if(!require('ggplot2'))
  install.packages("ggplot2", dependencies = T)
if(!require('tidyr'))
  install.packages("tidyr", dependencies = T)
if(!require('tibble'))
  install.packages("tibble", dependencies = T)
if(!require('DT'))
  install.packages("DT")
if(!require('formatR'))
  install.packages("formatR")

library(ipesedisplay)
library(reticulate)
library(DiagrammeR)
library(DiagrammeRsvg)
library(jsonlite)
library(dplyr)
library(plotly)
library(knitr)
library(ggplot2)
library(tidyr)
library(tibble)
library(purrr)

venv <- NULL
if (length(rmarkdown::metadata$venv) > 0) {venv <- rmarkdown::metadata$venv} else {venv <- "./venv"}


virtualenv_create(venv)
virtualenv_install(venv, "pyxosmose==1.14.0", pip_options = "--trusted-host=ipese-internal.epfl.ch --extra-index-url=https://ipese-internal.epfl.ch/registry/pypi/")
use_virtualenv(venv, required = T)

data <- NULL

knitr::opts_chunk$set(echo=T)
knitr::opts_chunk$set(error=F)
knitr::opts_chunk$set(message=F)
knitr::opts_chunk$set(warning=F)

def.chunk.hook  <- knitr::knit_hooks$get("chunk")
knitr::knit_hooks$set(chunk = function(x, options) {
  x <- def.chunk.hook(x, options)
  ifelse(options$size != "normalsize", paste0("\n \\", options$size,"\n\n", x, "\n\n \\normalsize"), x)
})

py_run_string("from pyxosmose.rosmose import Rosmose")

ro <- py$Rosmose()

options("scipen"=100, "digits"=4)
knitr::knit_engines$set(rosmose = function(options) {
  code <- paste(options$code, collapse = "\n")
  file_name <- knitr::current_input()
  result <- ro$retrieve_type(code, file_name)
  if(result[[1]] == T) {
    if(result[[2]] == 'custom_view'){
      result[[3]]
    } else if(result[[2]] == 'display_et'){
      options$engine <- "r"
      print(getwd())
      knitr::engine_output(options, out = list(display_graph(result[[3]], paste0(getwd(), "/images/", result[[4]], ".svg"))))
    } else if(result[[2]] == 'osmose_solve' || result[[2]] == 'osmose_load_result'){
      data <<- fromJSON(result[[3]], flatten=FALSE)
      data
    }
    else {
      code
    }
  } else {
    if(length(result) > 1) {
      if(result[[2]] == 'osmose_solve' || result[[2]] == 'osmose_load_result'){
        data <<- fromJSON(result[[3]], flatten=FALSE)
        ""
      }
    }
  }
})

tag <- function(tag) {
  for (el in ro.tags_manager.tags){
    if(el$name == tag){
      return(as.double(el$value))
    }
  }
}

readbibdata <- function(pattern) {
  bib_path <- rmarkdown::metadata$bibliography
  file_name <- knitr::current_input()
  return(ro$read_bib_data(file_name, bib_path, pattern))
}

get_output_format_for_kable <- function () {
  if (knitr::opts_knit$get("rmarkdown.pandoc.to") == "html") {
    return("html")
  } else {
    return("markdown")
  }
}


display_gcc <- function(time=1){
  graphs <- data$results$graph[[1]]
  graph <- graphs[[time]]
  graph <- graph[graph$plot_type == "gcc",]$data[[1]]
  gcc <- graph$curve[[1]]

  if (!is_empty(gcc)){
    plot_ly() %>%

      add_trace(x=gcc$Q, y=gcc$T-273.15, mode = 'lines', line=list(color='blue'), name='GCC') %>%
      add_trace(x=gcc$Q, y=1-298.15/gcc$T, mode = 'lines', line=list(color='blue'), yaxis = "y2", type = 'scatter', showlegend = FALSE) %>%
      layout(xaxis= list(title = "Heat load [kW]"),
             yaxis= list(title = "Corrected Temperatures [°C]"),
             yaxis2 = list(overlaying = "y", side = "right", title = 'Carnot factor 1-To/T [-]'),
             margin= list(l=50, r=50, b=40, t=40),
             title = "Grand Composite Curve"
            )
  } else {
    print(paste("There is no GCC for timestep", time))
  }
}

display_cc <- function(time=1){
  graphs <- data$results$graph[[1]]
  graph <- graphs[[time]]
  graph <- graph[graph$plot_type == "cc",]$data[[1]]
  hcc <- graph[graph$title == "Hot streams",]$curve[[1]]
  ccc <- graph[graph$title == "Cold streams",]$curve[[1]]

  if (!is_empty(hcc) && !is_empty(ccc)){
    plot_ly() %>%
            add_trace(x=hcc$Q, y=hcc$T-273.15, mode = 'lines', line=list(color='red'),  name='Hot Stream') %>%
            add_trace(x=hcc$Q, y=1-298.15/(hcc$T), line=list(color='red'),  yaxis = "y2", type = 'scatter', showlegend = FALSE) %>%
            add_trace(x=ccc$Q, y=ccc$T-273.15, mode = 'lines', line=list(color='blue'), name='Cold Streams') %>%
            layout(xaxis= list(title = "Heat load [kW]"),
                   yaxis= list(title = "Corrected Temperatures [°C]"),
                   yaxis2 = list(overlaying = "y", side = "right", title = 'Carnot factor 1-To/T [-]'),
                   margin= list(l=50, r=0, b=40, t=40),
                   title = "Composite Curve"
            )


  } else {
    print(paste("There is no CC for timestep", time))
  }
}

display_icc <- function(time=1){
  graphs <- data$results$graph[[1]]
  graph <- graphs[[time]]
  graph <- graph[graph$plot_type == "icc.utilities",]$data[[1]]
  base <- graph[graph$title == "base",]$curve[[1]]
  utilities <- graph[graph$title == "utilities",]$curve[[1]]

  if (!is_empty(base) && !is_empty(utilities)){
    plot_ly() %>%
            add_trace(x=base$Q, y=base$T-273.15, mode = 'lines', line=list(color='red'),  name='base') %>%
            add_trace(x=utilities$Q, y=utilities$T-273.15, mode = 'lines', line=list(color='blue'), name='utilities') %>%
            #add_trace(x=utilities$Q, y=1-298.15/(utilities$T), line=list(color='blue'), marker=list(color='blue'), yaxis = "y2", type = 'scatter', showlegend = FALSE) %>%
            layout(xaxis= list(title = "Heat load [kW]"),
                   yaxis= list(title = "Corrected Temperatures [C]"),
                   margin= list(l=50, r=20, b=40, t=40),
                   yaxis2 = list(overlaying = "y", side = "right", title = 'Carnot factor 1-To/T [-]'),
                   title = "Integrated Composite Curve"
            )

  } else {
    print(paste("There is no ICC for timestep", time))
  }
}

display_carnot <- function(time=1){
  graphs <- data$results$graph[[1]]
  graph <- graphs[[time]]
  graph <- graph[graph$plot_type == "carnot.utilities",]$data[[1]]
  base <- graph[graph$title == "base",]$curve[[1]]
  utilities <- graph[graph$title == "utilities",]$curve[[1]]

  if (!is_empty(base) && !is_empty(utilities)){
    plot_ly() %>%
            add_trace(x=base$Q, y=base$T, mode = 'lines', line=list(color='red'), name='base') %>%
            add_trace(x=utilities$Q, y=utilities$T, mode = 'lines', line=list(color='blue'), name='utilities') %>%
            layout(xaxis= list(title = "Heat load [kW]"),
                   yaxis= list(title = "Carnot factor 1-To/T [-]"),
                   margin= list(l=50, r=20, b=40, t=40),
                   title = "Carnot"
            )

  } else {
    print(paste("There is no Carnot for timestep", time))
  }
}


get_HEN <- function () {
  spag_area <- data$results$spaghetti[[1]]$Clu.DefaultHeatCascade.area_total
  min_number_HEX <- data$results$spaghetti[[1]]$Clu.DefaultHeatCascade.HEs
  hex_area <- spag_area / min_number_HEX
  an_factor <- 0.10
  c_hen <- (8500 + 409 * hex_area^(0.85)) * min_number_HEX * 603.1/402 * an_factor
  return(list("hex_area" = hex_area, "an_factor" = an_factor, "c_hen"= c_hen))
}


