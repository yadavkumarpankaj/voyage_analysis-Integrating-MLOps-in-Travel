import pandas as pd

class DataTransformer:  
    def __init__(self, data):  
        self.data = data  

    def transform(self):  
        """
        Transform the flight data for model training.
        Returns X (features) and Y (target) as separate DataFrames/Series.
        """
        df = self.data.copy()
        
        # Drop any rows with missing values
        df = df.dropna()
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Extract date features
        df['week_day'] = df['date'].dt.weekday
        df['month'] = df['date'].dt.month
        df['week_no'] = df['date'].dt.isocalendar().week
        df['year'] = df['date'].dt.year
        df['day'] = df['date'].dt.day
        
        # Rename 'to' column to 'destination'
        df.rename(columns={"to": "destination"}, inplace=True)
        
        # Create flight speed feature
        df['flight_speed'] = round(df['distance'] / df['time'], 2)
        
        # One-hot encode categorical variables
        df = pd.get_dummies(df, columns=['from', 'destination', 'flightType', 'agency'])
        
        # Drop irrelevant features
        df.drop(columns=['time', 'flight_speed', 'month', 'year', 'distance', 'date'], axis=1, inplace=True)
        
        # Rename columns with spaces to use underscores
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.replace('(', '')
        df.columns = df.columns.str.replace(')', '')
        
        # Separate features (X) and target variable (Y)
        X = df.drop('price', axis=1)  # Features
        Y = df['price']               # Target variable
        
        return X, Y
