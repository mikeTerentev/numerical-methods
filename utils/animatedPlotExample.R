library(ggplot2)
library(gganimate) # Package for animation
library(dplyr)     # Or data.table or just data.frame, as you wish

# Just function for example
f <- function(x) x^2 - 1

# Table of data which is used for animation
# "Legend" it's legend title and "Function" it's name of this data in legend
# I don't know how to make this piece of shit any other way
animatedData <- tibble(x = seq(from = -5.0, to = 5.0, by = 0.1), y = f(x), Legend = "Function")

# If you want some static background, table for static plot shoudn't
# contains column, by which you will animate (in this example column x)
staticData <- animatedData %>% rename(x2 = x)

p <- ggplot(animatedData, aes(x, y, colour = Legend)) +
  geom_point() +                                                   # Animation is moving dot
  geom_line(data = staticData,                                     # Add static line
            aes(x = x2, y = y, colour = Legend)) +
  geom_point(data = tibble(x2 = c(-1.0, 1.0),                      # Add static points
                           y = 0.0, Legend = "Root"),
             aes(x = x2, y = y, colour = Legend)) +
  labs(x = "X", y = "Y") +                                         # Asix names
  scale_colour_manual(values = c("blue", "red")) +                 # Plots colors
  theme(legend.position = "top") +                                 # Move legend on top
  transition_time(x)                                               # Use column x for animation like time

# Save to gif
anim_save("resultAnimation.gif", p)