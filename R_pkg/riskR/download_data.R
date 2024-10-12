library(httr)

ap <- available.packages()

download_rate <- function(pack, period)
{
  f <- function(p)
  {
    resp <- GET(glue::glue(("https://cranlogs.r-pkg.org/downloads/total/{p}/{pack}")))
    data <- content(resp, "parsed") |> unlist()
    data.frame("Time" = p, "Package" = pack, Downlaod = data[3])
  }
  suppressWarnings(do.call(rbind, lapply(period, \(x) f(x))))
}

# download_rate("dplyr", c("last-month", "last-week"))

# tic <- Sys.time()
# do.call(rbind, lapply(ap[c(1:10), 1], \(x) download_rate(x, period = c("last-month", "last-week"))))
# toc <- Sys.time()

# toc - tic

for(p in ap[, 1])
{
  cat("Package: ", p, fill = TRUE)
  d <- download_rate(p, c("last-month", "last-week"))  
  write.table(d, file = "pack_download.csv", append = TRUE, col.names = FALSE)
}