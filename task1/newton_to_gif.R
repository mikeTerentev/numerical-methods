library(ggplot2)
library(gganimate)
library(dplyr)

f <- function(x) x^7 - 5 * x^6 - 12 * x^5 + sqrt(2) * x^2 - 4

animatedData <- read.csv("task1/out.csv") %>% mutate(Legend = "Tangent")
staticData <- tibble(x = seq(from = 6.4, to = 7.1, by = 0.00001), y = f(x), Legend = "Function")

p <- ggplot(animatedData, aes(x, y, color = Legend)) +
  geom_point() +
  geom_line(data = staticData, aes(x, y, color = Legend)) +
  geom_abline(aes(slope = a, intercept = b, color = Legend)) +
  labs(title = "Iteration: {frame_time}", x = "X", y = "Y") +
  scale_colour_manual(values = c("blue", "red")) +
  theme(legend.position = "top") +
  transition_time(iteration)

anim_save("resultAnimation.gif", p)