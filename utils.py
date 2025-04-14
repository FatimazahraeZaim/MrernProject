import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import io
import base64
import json

def df_to_csv(df: pd.DataFrame) -> str:
    """
    Convert DataFrame to CSV string
    
    Args:
        df: Input DataFrame
        
    Returns:
        CSV string
    """
    return df.to_csv(index=False)

def df_to_excel(df: pd.DataFrame) -> bytes:
    """
    Convert DataFrame to Excel bytes
    
    Args:
        df: Input DataFrame
        
    Returns:
        Excel file as bytes
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Data', index=False)
    
    output.seek(0)
    return output.getvalue()

def df_to_json(df: pd.DataFrame) -> str:
    """
    Convert DataFrame to JSON string
    
    Args:
        df: Input DataFrame
        
    Returns:
        JSON string
    """
    return df.to_json(orient="records")

def fig_to_png(fig: go.Figure) -> bytes:
    """
    Convert Plotly figure to PNG bytes
    
    Args:
        fig: Plotly figure
        
    Returns:
        PNG image as bytes
    """
    return pio.to_image(fig, format="png")

def fig_to_svg(fig: go.Figure) -> bytes:
    """
    Convert Plotly figure to SVG bytes
    
    Args:
        fig: Plotly figure
        
    Returns:
        SVG image as bytes
    """
    return pio.to_image(fig, format="svg")

def fig_to_html(fig: go.Figure) -> str:
    """
    Convert Plotly figure to HTML string
    
    Args:
        fig: Plotly figure
        
    Returns:
        HTML string
    """
    return fig.to_html(include_plotlyjs='cdn', full_html=True)

def fig_to_json(fig: go.Figure) -> str:
    """
    Convert Plotly figure to JSON string
    
    Args:
        fig: Plotly figure
        
    Returns:
        JSON string
    """
    return json.dumps(fig.to_dict())

def get_embed_code(fig: go.Figure) -> str:
    """
    Generate HTML embed code for a Plotly figure
    
    Args:
        fig: Plotly figure
        
    Returns:
        HTML embed code
    """
    html = fig.to_html(include_plotlyjs='cdn', full_html=False)
    
    embed_code = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Embedded Visualization</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <div id="visualization">
        {html}
    </div>
</body>
</html>
"""
    
    return embed_code
