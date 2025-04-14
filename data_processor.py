import pandas as pd
import numpy as np
from typing import List, Dict, Union, Optional

class DataProcessor:
    """
    Class for processing and transforming data
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with a pandas DataFrame
        
        Args:
            data: The input DataFrame to process
        """
        self.data = data.copy()
    
    def get_columns_with_missing_values(self) -> Dict[str, int]:
        """
        Get columns with missing values and their counts
        
        Returns:
            Dictionary of column names and count of missing values
        """
        missing_columns = {}
        for col in self.data.columns:
            missing_count = self.data[col].isna().sum()
            if missing_count > 0:
                missing_columns[col] = missing_count
        
        return missing_columns
    
    def handle_missing_values(self, column: str, action: str, fill_value: Optional[str] = None, 
                             df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Handle missing values in a specific column
        
        Args:
            column: Column name to process
            action: Action to take ('Drop rows', 'Fill with mean', 'Fill with median', 
                    'Fill with mode', 'Fill with value')
            fill_value: Value to fill with if action is 'Fill with value'
            df: DataFrame to process (if None, use self.data)
            
        Returns:
            Processed DataFrame
        """
        if df is None:
            df = self.data.copy()
        else:
            df = df.copy()
        
        if action == "Drop rows":
            df = df.dropna(subset=[column])
        
        elif action == "Fill with mean":
            if pd.api.types.is_numeric_dtype(df[column]):
                df[column] = df[column].fillna(df[column].mean())
            else:
                raise ValueError(f"Cannot calculate mean for non-numeric column {column}")
        
        elif action == "Fill with median":
            if pd.api.types.is_numeric_dtype(df[column]):
                df[column] = df[column].fillna(df[column].median())
            else:
                raise ValueError(f"Cannot calculate median for non-numeric column {column}")
        
        elif action == "Fill with mode":
            mode_value = df[column].mode()[0]
            df[column] = df[column].fillna(mode_value)
        
        elif action == "Fill with value":
            if fill_value is not None:
                # Convert fill_value to the appropriate type based on column dtype
                if pd.api.types.is_numeric_dtype(df[column]):
                    try:
                        fill_value_converted = float(fill_value)
                    except ValueError:
                        raise ValueError(f"Cannot convert '{fill_value}' to numeric for column {column}")
                    df[column] = df[column].fillna(fill_value_converted)
                else:
                    df[column] = df[column].fillna(fill_value)
            else:
                raise ValueError("Fill value is required for 'Fill with value' action")
        
        return df
    
    def filter_numeric_data(self, column: str, min_val: float, max_val: float, 
                           df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Filter numeric data based on min and max values
        
        Args:
            column: Column name to filter
            min_val: Minimum value to include
            max_val: Maximum value to include
            df: DataFrame to process (if None, use self.data)
            
        Returns:
            Filtered DataFrame
        """
        if df is None:
            df = self.data.copy()
        else:
            df = df.copy()
        
        if not pd.api.types.is_numeric_dtype(df[column]):
            raise ValueError(f"Column {column} is not numeric")
        
        return df[(df[column] >= min_val) & (df[column] <= max_val)]
    
    def filter_categorical_data(self, column: str, values: List, 
                               df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Filter categorical data to include only specified values
        
        Args:
            column: Column name to filter
            values: List of values to include
            df: DataFrame to process (if None, use self.data)
            
        Returns:
            Filtered DataFrame
        """
        if df is None:
            df = self.data.copy()
        else:
            df = df.copy()
        
        return df[df[column].isin(values)]
    
    def transform_numeric_column(self, column: str, transformation: str, 
                                df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Apply transformation to a numeric column
        
        Args:
            column: Column name to transform
            transformation: Transformation to apply ('Log', 'Square Root', 'Square', 
                           'Z-Score Normalization', 'Min-Max Scaling')
            df: DataFrame to process (if None, use self.data)
            
        Returns:
            DataFrame with transformed column
        """
        if df is None:
            df = self.data.copy()
        else:
            df = df.copy()
        
        if not pd.api.types.is_numeric_dtype(df[column]):
            raise ValueError(f"Column {column} is not numeric")
        
        if transformation == "Log":
            # Handle zeros and negative values
            min_val = df[column].min()
            if min_val <= 0:
                offset = abs(min_val) + 1  # Add 1 to ensure all values are positive
                df[f"{column}_log"] = np.log(df[column] + offset)
            else:
                df[f"{column}_log"] = np.log(df[column])
        
        elif transformation == "Square Root":
            # Handle negative values
            min_val = df[column].min()
            if min_val < 0:
                offset = abs(min_val)
                df[f"{column}_sqrt"] = np.sqrt(df[column] + offset)
            else:
                df[f"{column}_sqrt"] = np.sqrt(df[column])
        
        elif transformation == "Square":
            df[f"{column}_squared"] = df[column] ** 2
        
        elif transformation == "Z-Score Normalization":
            df[f"{column}_zscore"] = (df[column] - df[column].mean()) / df[column].std()
        
        elif transformation == "Min-Max Scaling":
            min_val = df[column].min()
            max_val = df[column].max()
            df[f"{column}_scaled"] = (df[column] - min_val) / (max_val - min_val)
        
        return df
    
    def transform_categorical_column(self, column: str, transformation: str, 
                                    df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Apply transformation to a categorical column
        
        Args:
            column: Column name to transform
            transformation: Transformation to apply ('One-Hot Encoding')
            df: DataFrame to process (if None, use self.data)
            
        Returns:
            DataFrame with transformed column
        """
        if df is None:
            df = self.data.copy()
        else:
            df = df.copy()
        
        if transformation == "One-Hot Encoding":
            # Create one-hot encoded columns
            one_hot = pd.get_dummies(df[column], prefix=column)
            
            # Drop the original column and join the one-hot encoded columns
            df = df.drop(column, axis=1)
            df = df.join(one_hot)
        
        return df
