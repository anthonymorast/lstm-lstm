# lstm-lstm
LSTM-LSTM Hybrid Approach to Time Series Forecasting with Applications to Foreign Exchange Rate Data

# Thesis
https://www.overleaf.com/read/zvcrmfdqmmky

# GitLab

Must have access to SDSMT VPN!

https://gitlab.mcs.sdsmt.edu/1976379/autotrade

# Research Objectives

+ Error corrected model

+ Nest the error corrected model, that is predict errors of base model with LSTM, predict errors of base model + LSTM with LSTM, predict errors of base model + LSTM + LSTM with LSTM, etc. Will this work?

+ Train single LSTM for hybrid (shares weights/biases): one LSTM, two outputs viz. value and error

+ Train error model using errors, time series values, and both to see which produces the best results. 

# TODO
+ Thread PBT
  + Can't (effectively) run multiple sessions of TF on one GPU
  + PBT eats up too much memory as it stands
  + Run each population training run in its own thread and pass back the best error and corresponding hyperparams
  + Update best and explore/exploit in main thread
