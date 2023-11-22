### INF563 (2015-2016)
### Copyright (C) 2015 by M. Carrière and S. Oudot

# retrieve data
data=read.table('matrix_d2_n10_height.dat')

# perform PCA with(out) data normalization
source("R/PCA.R")
L <- PCA(data, FALSE)

M <- data.matrix(L[[1]]) # data after projection
V <- L[[2]] # new axes (correlations between old and new variables)
Var <- L[[3]] # cumulative variance
S <- L[[4]] # spectrum


# plots
library(rgl)

# spectrum plot
#dev.new()
#plot(S)

# cumulative variance plot
#dev.new()
#plot(Var)

# data plot using first 2 intrinsic variables
dev.new()
plot(M[1,], M[2,], col="blue", pch = 19, lty = "solid")
text(M[1,], M[2,], labels=rownames(data), pos=3)

# correlation circles (intrinsic variables w.r.t. input variables)
dev.new()
plot(t(V)[1,], t(V)[2,], col="blue", pch = 19, lty = "solid", asp = 1, xlim = c(-1, 1), ylim = c(-1, 1))
text(t(V)[1,], t(V)[2,], labels=colnames(data), pos=3)
library("plotrix")
draw.circle(0, 0, 1, nv=100, border=NULL, col=NA, lty=1, lwd=1)

# plot 3d
library(rgl)
open3d()
plot3d(M[1,], M[2,], M[3,], size=10, col=rainbow(10)[cbind(seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10))])
#plot3d(M[1,], M[2,], M[3,], size=10, col=rainbow(10)[rbind(seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10),seq(1:10))])

