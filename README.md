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

## Conclusion
My model predicted the future prices for stocks in a very general sense, strongly. I believe this is not because of the model itself, but because of the market performence during and after the provided data. My model was mostly unsuccessful in ignoring the noise, even with my best efforts to stationize the data. This noise lead the agent to believe the market only goes up, and that is easily observed through the forecasted prices: up and to the right almost all the time. 
#### What could be improved 
As previously stated in my conclusion, the data I provided allows the agent to learn a false positive about the market; it only goes up. To improve this one could collect more data that encompasses a severe market correction.
## Licence
MIT © Dylan Snyder
