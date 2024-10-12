library(dplyr)
library(ggplot2)

dat <- read.table("data/pack_download_11OCT2024.csv")
dat <- dat[2:4]

names(dat) <- c("Period", "Package", "Download")

dat |> 
  filter(Period == "last-month") |> 
  summarise(mean = mean(Download),
            sd = sd(Download), 
            max = max(Download))

mon <- dat |> filter(Period == "last-month")

sort(mon$Download, decreasing = TRUE)
sum(mon$Download > 10000)

quantile(mon$Download, seq(0.05, 0.95, by = 0.05))
