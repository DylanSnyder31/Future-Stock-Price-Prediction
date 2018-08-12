# Stock Price Forecasting
Using Autoregressive Integrated Moving Average (ARIMA), this projects forecasts future stock prices based on the past data alone. 

## Getting Started

### Dependencies
```
pip install -r requirements.txt
```
#### Training 
To find the optimal values model run:
```
python train_agent.py --choice [ENTER A STOCK HERE]
```
To display a list of the available stocks run:
```
python train_agent.py --list show
```

#### Visualize 
To visualize the data run:
```
python visualize_main.py --choice [ENTER STOCK HERE] --data_display [simple OR forecast]
```
###### --data_display simple
This visualizes the past stock price history, without the forecasted price

###### --data_display forecast
This displays the past data along with the forecasted price history of the stock

## Images
{ENTER IMAGES}
## Licence
MIT © Dylan Snyder
