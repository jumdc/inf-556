### INF563 (2015-2016)
### Copyright (C) 2015 by M. Carrière and S. Oudot

# retrieve data
data=read.table('matrix_d2_n10_height.dat')

# normalize data
M <- scale(data.matrix(data), scale=FALSE)

# compute l^\infty distance matrix
D <- matrix(,nrow = length(M[,1]), ncol = length(M[,1]))
for (i in 1:(length(M[,1])))
    for (j in 1:length(M[,1]))
        D[i,j] <- max(abs(M[i,]-M[j,])) # l^\infty distance

# perform MetricMDS
source("R/MetricMDS.R")
L <- MetricMDS(D)

M <- data.matrix(L[[1]]) # data after projection
V <- L[[2]] # new axes
S <- L[[3]] # spectrum


# plots

# spectrum plot
dev.new()
plot(S)

# data plot using first 2 intrinsic variables (check that result is the same as with PCA)
dev.new()
plot(M[,1], M[,2], col="blue", pch = 19, lty = "solid")
text(M[,1], M[,2], labels=rownames(data), pos=3)

# plot 3d
library(rgl)
open3d()
plot3d(M[,1], M[,2], M[,3], size=10, col=rbind(seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10)))
