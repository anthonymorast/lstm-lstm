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

+ If the multiple LSTM model is worse, try with a really weak neural network as the first model (linear NN [no activation]?)

+ Can an LSTM-LSTM model predict further out than an ARIMA-ANN before needing to be retrained? Is it far enough out to justify longer training times?
  + What's the turning point where ARIMA is as fast as the LSTM-LSTM? What is the accuracy there? How frequently is retraining necessary here?
  + Answer the questions: how accurate are they? how often must they be trained? how fast is it to train them? how many timesteps out can each predict while maintaining accuracy?

+ Does the representation need to be changed? Data preprocessing?

# TODO
+ Thread PBT
  + Can't (effectively) run multiple sessions of TF on one GPU
  + PBT eats up too much memory as it stands
  + Run each population training run in its own thread and pass back the best error and corresponding hyperparams
  + Update best and explore/exploit in main thread

+ Train LSTMs similar to ARIMA for complex financial data. That is, predict a few terms, replace some training data with examples from test set (that we just tried to predict), and re-fit. Kind of like a sliding window with training.
  + Can we more accurately predict using the LSTMs over a longer time period? That is, maybe we go out 10 time steps with ARIMA before things get bad, can we go out 10, 20, 30+ time steps with the LSTM and still get reasonable predictions?
  
+ Multivariate data sets

+ Non-financial data sets (stationary datasets)
  + A machine learning method learns a function. With non-stationary financial data the function changes over time as the statistical properties of the data change (rules of the game change) so new functions now produce the data, thus model needs re-trained. 
