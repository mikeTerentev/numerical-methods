library(ggplot2)
library(gganimate)
library(dplyr)

f <- function(x) x^7 - 5 * x^6 - 12 * x^5 + sqrt(2) * x^2 - 4

boundaries <- tibble(left = c(-1.9, -1.5, 6.4), right = c(-1.5, -0.5, 7.1))

for (root_num in 2:2) {
  animatedData <- read.csv(file.path("task1", paste0("out", root_num, ".csv"))) %>% mutate(Legend = "Tangent")
  xs <- seq(boundaries[["left"]][root_num], boundaries[["right"]][root_num], by = 0.00001)
  staticData <- tibble(x = xs, y = f(x), Legend = "Function")

  p <- ggplot(animatedData, aes(x, y, color = Legend)) +
    geom_point() +
    geom_line(data = staticData, aes(x, y, color = Legend)) +
    geom_abline(aes(slope = a, intercept = b, color = Legend)) +
    labs(title = "Iteration: {frame_time}", x = "X", y = "Y") +
    scale_colour_manual(values = c("blue", "red")) +
    theme(legend.position = "top") +
    transition_time(iteration)

  anim_save(paste0("result_animation_", root_num, ".gif"), p, path = "./task1", fps = 16)
}