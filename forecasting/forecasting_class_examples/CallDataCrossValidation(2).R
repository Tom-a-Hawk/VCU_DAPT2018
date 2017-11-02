library("forecast")

Call.data <- read.csv("C:\\Users\\jrmerric\\Dropbox\\Teaching\\Exec Ed\\Decision Analytics\\Forecasting\\2017\\Call Volumes vs Nos Accounts.csv")

CVProd1.ts <- ts(Call.data$CallVolProd1, 
                 start = c(2009,45), end = c(2011, 12), freq = 52)
Accts1Week.ts <- ts(Call.data$NosAccts1WeeksOld, 
                    start = c(2009,45), end = c(2011, 12), freq = 52)
Accts4Weeks.ts <- ts(Call.data$NosAccts4WeeksOld, 
                    start = c(2009,45), end = c(2011, 12), freq = 52)
Accts8Weeks.ts <- ts(Call.data$NosAccts8WeeksOld, 
                     start = c(2009,45), end = c(2011, 12), freq = 52)

par(mfrow = c(2, 3))

n <- length(CVProd1.ts)
nValid <- 26
nTrain <- n - nValid

trainY.ts <- window(CVProd1.ts, 
                   start = c(2009, 45), end = c(2009, 45 + nTrain - 1))
validY.ts <- window(CVProd1.ts, 
                   start = c(2009, 45 + nTrain), end = c(2009, 45 + n - 1))

fitwithoutX <- auto.arima(trainY.ts)
ForecastwithoutX <- forecast(fitwithoutX, level=c(80,95), h=nValid)

plot(ForecastwithoutX, xlim = c(2009+45/52,2011+12/52), main = "Call volume forecast with no regressors")
lines(validY.ts)

hist(ForecastwithoutX$residuals, ylab = "Frequency", xlab = "Fit Error", bty = "l", main = "")
hist(validY.ts - ForecastwithoutX$mean, ylab = "Frequency", xlab = "Forecast Error", bty = "l", main = "")

lag = 4

trainY.ts <- window(CVProd1.ts, 
                    start = c(2009, 45 + lag), end = c(2009, 45 + nTrain))
validY.ts <- window(CVProd1.ts, 
                    start = c(2009, 45 + nTrain + 1), end = c(2009, 45 + n - 1))

trainX1.ts <- window(Accts1Week.ts, 
                    start = c(2009, 45), end = c(2009, 45 + nTrain - lag))
validX1.ts <- window(Accts1Week.ts, 
                    start = c(2009, 45 + nTrain + 1 - lag), end = c(2009, 45 + n - lag - 1))

trainX2.ts <- window(Accts4Weeks.ts, 
                     start = c(2009, 45), end = c(2009, 45 + nTrain - lag))
validX2.ts <- window(Accts4Weeks.ts, 
                     start = c(2009, 45 + nTrain + 1 - lag), end = c(2009, 45 + n - lag - 1))

trainX3.ts <- window(Accts8Weeks.ts, 
                     start = c(2009, 45), end = c(2009, 45 + nTrain - lag))
validX3.ts <- window(Accts8Weeks.ts, 
                     start = c(2009, 45 + nTrain + 1 - lag), end = c(2009, 45 + n - lag - 1))

fitwithX <- auto.arima(trainY.ts, xreg= cbind(trainX1.ts, trainX2.ts, trainX3.ts))
ForecastwithX <- forecast(fitwithX, xreg = cbind(validX1.ts, validX2.ts, validX3.ts), level=c(80,95))

plot(ForecastwithX, xlim = c(2009+45/52,2011+12/52), main = "Call volume forecast with regressors")
lines(validY.ts)

hist(ForecastwithX$residuals, ylab = "Frequency", xlab = "Fit Error", bty = "l", main = "")
hist(validY.ts - ForecastwithX$mean, ylab = "Frequency", xlab = "Forecast Error", bty = "l", main = "")

accuracy(ForecastwithoutX$mean, validY.ts)
accuracy(ForecastwithX$mean, validY.ts)

