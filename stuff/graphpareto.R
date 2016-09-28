
# args = commandArgs(trailingOnly=TRUE)
# ref: https://www.r-bloggers.com/passing-arguments-to-an-r-script-from-command-lines/

# if (length(args) != 3) {
#    stop("invalid # of arguments, must include data and save file names") 
# }

# R --no-save --slave < graphpareto.R; open pix.png

df = read.delim("metapareto", sep=" ", header=FALSE,
        col.names=c("Factor", "basemin", "rmin",
                    "rmed","rmax","basemax"))

df[is.na(df)] = 0

library("dplyr")
library("ggplot2")

stepdf = mutate(df, rmin= ifelse(rmin<=0, basemin, basemax) -
    ifelse(rmin <= 0, -1, 1) * 0.5^(abs(rmin) + 1) * (basemax-basemin),
                    rmax= ifelse(rmax<=0, basemin, basemax) -
    ifelse(rmax <= 0, -1, 1) * 0.5^(abs(rmax) + 1) * (basemax-basemin),
                    rmed= ifelse(rmed<=0, basemin, basemax) -
    ifelse(rmed <= 0, -1, 1) * 0.5^(abs(rmed) + 1) * (basemax-basemin))

(ggplot(stepdf, aes(x=Factor, y=rmed, color=Factor)) +
  geom_point() + geom_linerange(aes(ymin=rmin, ymax=rmax)) +
  coord_cartesian(ylim=c(min(0,stepdf$rmin),max(1,stepdf$rmax))) +
  coord_polar(theta = "x"))


ggsave("pix.png")

print(stepdf)
# consider rewriting so it's bmin, bmax, min, max, med?
# needs to include factors, specially written
