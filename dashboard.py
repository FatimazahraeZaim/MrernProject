import pandas as pd
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional

class Dashboard:
    """
    Class for creating and managing dashboards
    """
    
    @staticmethod
    def export_dashboard_html(
        title: str,
        visualizations: List[Dict[str, Any]],
        layout: str = "2 Columns"
    ) -> str:
        """
        Export dashboard as HTML
        
        Args:
            title: Dashboard title
            visualizations: List of visualization items
            layout: Layout style ("1 Column", "2 Columns", "3 Columns")
            
        Returns:
            HTML string
        """
        # Start HTML document
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f8f9fa;
                }}
                .dashboard-title {{
                    text-align: center;
                    margin-bottom: 30px;
                    color: #333;
                }}
                .dashboard-container {{
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: space-around;
                }}
                .viz-container {{
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                    padding: 15px;
                }}
                .viz-title {{
                    text-align: center;
                    margin-top: 0;
                    margin-bottom: 15px;
                    color: #555;
                }}
            </style>
        </head>
        <body>
            <h1 class="dashboard-title">{title}</h1>
            <div class="dashboard-container">
        """
        
        # Determine column width based on layout
        if layout == "1 Column":
            col_width = "100%"
        elif layout == "2 Columns":
            col_width = "48%"
        else:  # 3 Columns
            col_width = "31%"
        
        # Add each visualization
        for i, viz in enumerate(visualizations):
            # Convert Plotly figure to HTML div
            fig_html = viz["fig"].to_html(full_html=False, include_plotlyjs=False)
            
            html += f"""
            <div class="viz-container" style="width: {col_width};">
                <h3 class="viz-title">{viz["name"]}</h3>
                {fig_html}
            </div>
            """
        
        # Close HTML document
        html += """
            </div>
        </body>
        </html>
        """
        
        return html
