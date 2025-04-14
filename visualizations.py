import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Optional, Dict, Any, List, Union

class Visualization:
    """
    Class for creating various types of visualizations
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with a pandas DataFrame
        
        Args:
            data: The input DataFrame to visualize
        """
        self.data = data.copy()
    
    def create_bar_chart(
        self, 
        x: str, 
        y: str, 
        color: Optional[str] = None, 
        title: str = "Bar Chart", 
        x_title: Optional[str] = None, 
        y_title: Optional[str] = None,
        orientation: str = "vertical",
        height: int = 500,
        width: int = 700
    ) -> go.Figure:
        """
        Create a bar chart
        
        Args:
            x: Column name for x-axis
            y: Column name for y-axis
            color: Column name for color grouping (optional)
            title: Chart title
            x_title: X-axis title (defaults to x column name)
            y_title: Y-axis title (defaults to y column name)
            orientation: "vertical" or "horizontal"
            height: Chart height in pixels
            width: Chart width in pixels
            
        Returns:
            Plotly Figure object
        """
        if orientation == "vertical":
            fig = px.bar(
                self.data, 
                x=x, 
                y=y, 
                color=color,
                title=title,
                labels={x: x_title or x, y: y_title or y},
                height=height,
                width=width
            )
        else:  # horizontal
            fig = px.bar(
                self.data, 
                x=y,  # Switch x and y for horizontal
                y=x, 
                color=color,
                title=title,
                labels={x: x_title or x, y: y_title or y},
                orientation='h',  # Horizontal orientation
                height=height,
                width=width
            )
        
        fig.update_layout(
            title={
                'text': title,
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        
        return fig
    
    def create_line_chart(
        self, 
        x: str, 
        y: str, 
        color: Optional[str] = None, 
        title: str = "Line Chart", 
        x_title: Optional[str] = None, 
        y_title: Optional[str] = None,
        height: int = 500,
        width: int = 700
    ) -> go.Figure:
        """
        Create a line chart
        
        Args:
            x: Column name for x-axis
            y: Column name for y-axis
            color: Column name for color grouping (optional)
            title: Chart title
            x_title: X-axis title (defaults to x column name)
            y_title: Y-axis title (defaults to y column name)
            height: Chart height in pixels
            width: Chart width in pixels
            
        Returns:
            Plotly Figure object
        """
        fig = px.line(
            self.data, 
            x=x, 
            y=y, 
            color=color,
            title=title,
            labels={x: x_title or x, y: y_title or y},
            height=height,
            width=width
        )
        
        fig.update_layout(
            title={
                'text': title,
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        
        return fig
    
    def create_scatter_plot(
        self, 
        x: str, 
        y: str, 
        size: Optional[str] = None,
        color: Optional[str] = None, 
        title: str = "Scatter Plot", 
        x_title: Optional[str] = None, 
        y_title: Optional[str] = None,
        height: int = 500,
        width: int = 700
    ) -> go.Figure:
        """
        Create a scatter plot
        
        Args:
            x: Column name for x-axis
            y: Column name for y-axis
            size: Column name for point size (optional)
            color: Column name for color grouping (optional)
            title: Chart title
            x_title: X-axis title (defaults to x column name)
            y_title: Y-axis title (defaults to y column name)
            height: Chart height in pixels
            width: Chart width in pixels
            
        Returns:
            Plotly Figure object
        """
        fig = px.scatter(
            self.data, 
            x=x, 
            y=y, 
            size=size,
            color=color,
            title=title,
            labels={x: x_title or x, y: y_title or y},
            height=height,
            width=width
        )
        
        fig.update_layout(
            title={
                'text': title,
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        
        return fig
    
    def create_pie_chart(
        self, 
        labels: str, 
        values: str, 
        title: str = "Pie Chart",
        height: int = 500,
        width: int = 700
    ) -> go.Figure:
        """
        Create a pie chart
        
        Args:
            labels: Column name for slice labels
            values: Column name for slice values
            title: Chart title
            height: Chart height in pixels
            width: Chart width in pixels
            
        Returns:
            Plotly Figure object
        """
        fig = px.pie(
            self.data, 
            names=labels, 
            values=values,
            title=title,
            height=height,
            width=width
        )
        
        fig.update_layout(
            title={
                'text': title,
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        
        return fig
    
    def create_histogram(
        self, 
        x: str, 
        bins: int = 20,
        title: str = "Histogram", 
        x_title: Optional[str] = None,
        height: int = 500,
        width: int = 700
    ) -> go.Figure:
        """
        Create a histogram
        
        Args:
            x: Column name for data
            bins: Number of bins
            title: Chart title
            x_title: X-axis title (defaults to x column name)
            height: Chart height in pixels
            width: Chart width in pixels
            
        Returns:
            Plotly Figure object
        """
        fig = px.histogram(
            self.data, 
            x=x,
            nbins=bins,
            title=title,
            labels={x: x_title or x},
            height=height,
            width=width
        )
        
        fig.update_layout(
            title={
                'text': title,
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        
        return fig
    
    def create_box_plot(
        self, 
        x: str, 
        y: str, 
        color: Optional[str] = None, 
        title: str = "Box Plot", 
        x_title: Optional[str] = None, 
        y_title: Optional[str] = None,
        height: int = 500,
        width: int = 700
    ) -> go.Figure:
        """
        Create a box plot
        
        Args:
            x: Column name for x-axis (categories)
            y: Column name for y-axis (values)
            color: Column name for color grouping (optional)
            title: Chart title
            x_title: X-axis title (defaults to x column name)
            y_title: Y-axis title (defaults to y column name)
            height: Chart height in pixels
            width: Chart width in pixels
            
        Returns:
            Plotly Figure object
        """
        fig = px.box(
            self.data, 
            x=x, 
            y=y, 
            color=color,
            title=title,
            labels={x: x_title or x, y: y_title or y},
            height=height,
            width=width
        )
        
        fig.update_layout(
            title={
                'text': title,
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        
        return fig
    
    def create_heatmap(
        self, 
        corr_method: str = "pearson",
        title: str = "Correlation Heatmap",
        height: int = 600,
        width: int = 700
    ) -> go.Figure:
        """
        Create a correlation heatmap
        
        Args:
            corr_method: Correlation method ('pearson', 'kendall', 'spearman')
            title: Chart title
            height: Chart height in pixels
            width: Chart width in pixels
            
        Returns:
            Plotly Figure object
        """
        # Only use numeric columns
        numeric_df = self.data.select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] < 2:
            raise ValueError("Need at least 2 numeric columns to create a correlation heatmap")
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr(method=corr_method)
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='RdBu_r',
            zmin=-1,
            zmax=1,
            colorbar=dict(title='Correlation')
        ))
        
        fig.update_layout(
            title={
                'text': title,
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            height=height,
            width=width
        )
        
        return fig
