# Stock Price Prediction Using LSTM

## Project Overview

This project implements a deep learning model to predict stock prices using historical market data. The model uses a Long Short-Term Memory (LSTM) neural network to learn patterns from past stock prices and generate future price predictions.

The workflow includes data preprocessing, moving average analysis, normalization, sequence creation, model training, and prediction visualization.

---

## Objectives

The main objectives of this project are:

- Analyze historical stock price data
- Identify trends using moving averages
- Prepare sequential data for deep learning models
- Train an LSTM model for stock price prediction
- Compare predicted prices with actual prices

---

## Technologies Used

The project was implemented using the following technologies:

- Python
- NumPy
- Pandas
- Matplotlib
- Scikit-learn
- TensorFlow
- Keras

---

## Data Preprocessing

### Moving Average Analysis

Moving averages are calculated to identify trends in stock prices.

#### 100-Day Moving Average

The 100-day moving average helps smooth short-term fluctuations and identify general trends.

```python
ma_100_days = data.Close.rolling(100).mean()
```

A plot is generated to compare the moving average with the actual closing price.

#### 200-Day Moving Average

The 200-day moving average is used to observe long-term trends in stock prices.

```python
ma_200_days = data.Close.rolling(200).mean()
```

Both moving averages are plotted along with the stock's closing price.

---

## Data Splitting

The dataset is divided into training and testing sets.

- 80 percent of the data is used for training
- 20 percent of the data is used for testing

```python
data_train = pd.DataFrame(data.Close[0: int(len(data)*0.80)])
data_test = pd.DataFrame(data.Close[int(len(data)*0.80):len(data)])
```

Training samples: 2208  
Testing samples: 553

---

## Data Normalization

To improve model performance, the data is scaled between 0 and 1 using MinMaxScaler.

```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0,1))
data_train_scale = scaler.fit_transform(data_train)
```

Normalization ensures stable and efficient model training.

---

## Sequence Preparation

LSTM models require sequential input data. Therefore, sequences of the previous 100 days are used to predict the next day’s stock price.

```python
x = []
y = []

for i in range(100, data_train_scale.shape[0]):
    x.append(data_train_scale[i-100:i])
    y.append(data_train_scale[i,0])
```

The sequences are then converted into NumPy arrays.

```python
x, y = np.array(x), np.array(y)
```

---

## Model Architecture

The model is built using the Keras Sequential API with LSTM layers.

```python
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential
```

The architecture typically includes:

- LSTM layers for capturing temporal dependencies
- Dropout layers for reducing overfitting
- Dense layers for final prediction

---

## Prediction Visualization

The predicted stock prices are compared with the original prices using a line plot.

```python
plt.figure(figsize=(10,8))
plt.plot(y_predict,'r',label='Predicted Price')
plt.plot(y,'g',label = 'Original Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
```

This visualization helps evaluate how closely the model predictions follow the real stock price trend.

---

## Results

The model learns patterns from historical data and produces predicted price trends. By comparing predicted and actual prices, the effectiveness of the LSTM model can be visually assessed.

---


## Author

Palak Sahu  
Bachelor of Technology in Computer Science (AI and ML)

Interested in Machine Learning, Artificial Intelligence, Data Analytics, and Web Development.
