import streamlit as st
import pandas as pd
import json
import io
from data_processor import DataProcessor
from visualizations import Visualization
from dashboard import Dashboard
import api
import utils

st.set_page_config(
    page_title="PM Data Analytics Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if 'data' not in st.session_state:
    st.session_state.data = None
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'visualizations' not in st.session_state:
    st.session_state.visualizations = []
if 'dashboard_items' not in st.session_state:
    st.session_state.dashboard_items = []

# Main title and description
st.title("Product Manager Data Analytics Tool")
st.markdown("""
This tool helps product managers analyze data and create shareable visualizations.
Technical teams can also integrate with the data through API endpoints.
""")

# Sidebar for navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox(
    "Choose a mode",
    ["Data Import", "Data Processing", "Visualizations", "Dashboard", "Sharing", "API Integration"]
)

# Data Import
if app_mode == "Data Import":
    st.header("Import Your Data")
    
    # File upload
    uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx", "json"])
    
    if uploaded_file is not None:
        try:
            file_extension = uploaded_file.name.split('.')[-1]
            
            if file_extension == 'csv':
                df = pd.read_csv(uploaded_file)
            elif file_extension == 'xlsx':
                df = pd.read_excel(uploaded_file)
            elif file_extension == 'json':
                df = pd.read_json(uploaded_file)
            
            st.session_state.data = df
            st.session_state.processed_data = df.copy()
            
            st.success(f"Successfully loaded data with {df.shape[0]} rows and {df.shape[1]} columns")
            
            # Display data preview
            st.subheader("Data Preview")
            st.dataframe(df.head())
            
            # Display data info
            st.subheader("Data Information")
            buffer = io.StringIO()
            df.info(buf=buffer)
            info_str = buffer.getvalue()
            st.text(info_str)
            
            # Display data statistics
            st.subheader("Data Statistics")
            st.dataframe(df.describe())
            
        except Exception as e:
            st.error(f"Error loading data: {e}")

# Data Processing
elif app_mode == "Data Processing":
    st.header("Process Your Data")
    
    if st.session_state.data is None:
        st.warning("Please import data first from the Data Import section")
    else:
        data_processor = DataProcessor(st.session_state.data)
        
        st.subheader("Data Cleaning")
        
        # Handle missing values
        st.markdown("### Handle Missing Values")
        missing_cols = data_processor.get_columns_with_missing_values()
        
        if not missing_cols:
            st.info("No missing values found in the dataset")
        else:
            st.write("Columns with missing values:")
            st.write(missing_cols)
            
            for col in missing_cols:
                st.markdown(f"**Column: {col}**")
                missing_action = st.selectbox(
                    f"Action for missing values in {col}",
                    ["Drop rows", "Fill with mean", "Fill with median", "Fill with mode", "Fill with value"],
                    key=f"missing_{col}"
                )
                
                if missing_action == "Fill with value":
                    fill_value = st.text_input(f"Value to fill {col}", key=f"fill_value_{col}")
                    if st.button(f"Apply for {col}", key=f"apply_missing_{col}"):
                        st.session_state.processed_data = data_processor.handle_missing_values(
                            col, missing_action, fill_value, st.session_state.processed_data
                        )
                        st.success(f"Applied {missing_action} to column {col}")
                elif st.button(f"Apply for {col}", key=f"apply_missing_{col}"):
                    st.session_state.processed_data = data_processor.handle_missing_values(
                        col, missing_action, None, st.session_state.processed_data
                    )
                    st.success(f"Applied {missing_action} to column {col}")
        
        # Filter data
        st.markdown("### Filter Data")
        columns = st.session_state.processed_data.columns.tolist()
        filter_col = st.selectbox("Select column to filter", columns, key="filter_col")
        
        col_type = st.session_state.processed_data[filter_col].dtype
        
        if pd.api.types.is_numeric_dtype(col_type):
            min_val = float(st.session_state.processed_data[filter_col].min())
            max_val = float(st.session_state.processed_data[filter_col].max())
            
            filter_range = st.slider(
                f"Range for {filter_col}",
                min_val,
                max_val,
                (min_val, max_val),
                key="filter_range"
            )
            
            if st.button("Apply Filter", key="apply_filter"):
                st.session_state.processed_data = data_processor.filter_numeric_data(
                    filter_col, filter_range[0], filter_range[1], st.session_state.processed_data
                )
                st.success(f"Filtered {filter_col} between {filter_range[0]} and {filter_range[1]}")
        else:
            unique_vals = st.session_state.processed_data[filter_col].unique().tolist()
            selected_vals = st.multiselect(
                f"Select values for {filter_col}",
                unique_vals,
                default=unique_vals,
                key="filter_vals"
            )
            
            if st.button("Apply Filter", key="apply_filter"):
                st.session_state.processed_data = data_processor.filter_categorical_data(
                    filter_col, selected_vals, st.session_state.processed_data
                )
                st.success(f"Filtered {filter_col} to include {', '.join(map(str, selected_vals))}")
        
        # Transform data
        st.markdown("### Transform Data")
        transform_col = st.selectbox("Select column to transform", columns, key="transform_col")
        
        transform_col_type = st.session_state.processed_data[transform_col].dtype
        
        if pd.api.types.is_numeric_dtype(transform_col_type):
            transform_action = st.selectbox(
                f"Transformation for {transform_col}",
                ["None", "Log", "Square Root", "Square", "Z-Score Normalization", "Min-Max Scaling"],
                key="transform_action"
            )
            
            if st.button("Apply Transformation", key="apply_transform"):
                if transform_action != "None":
                    st.session_state.processed_data = data_processor.transform_numeric_column(
                        transform_col, transform_action, st.session_state.processed_data
                    )
                    st.success(f"Applied {transform_action} transformation to {transform_col}")
        else:
            transform_action = st.selectbox(
                f"Transformation for {transform_col}",
                ["None", "One-Hot Encoding"],
                key="transform_action"
            )
            
            if st.button("Apply Transformation", key="apply_transform"):
                if transform_action != "None":
                    st.session_state.processed_data = data_processor.transform_categorical_column(
                        transform_col, transform_action, st.session_state.processed_data
                    )
                    st.success(f"Applied {transform_action} to {transform_col}")
        
        # Display processed data
        st.subheader("Processed Data Preview")
        st.dataframe(st.session_state.processed_data.head())
        
        # Reset processed data option
        if st.button("Reset to Original Data"):
            st.session_state.processed_data = st.session_state.data.copy()
            st.success("Reset to original data")

# Visualizations
elif app_mode == "Visualizations":
    st.header("Create Visualizations")
    
    if st.session_state.processed_data is None:
        st.warning("Please import and process data first")
    else:
        viz = Visualization(st.session_state.processed_data)
        
        # Create visualization form
        with st.form("visualization_form"):
            st.subheader("Create a New Visualization")
            
            viz_name = st.text_input("Visualization Name", "My Visualization")
            
            viz_type = st.selectbox(
                "Visualization Type",
                ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram", "Box Plot", "Heatmap"]
            )
            
            columns = st.session_state.processed_data.columns.tolist()
            
            # Different options based on visualization type
            if viz_type in ["Bar Chart", "Line Chart", "Box Plot"]:
                x_col = st.selectbox("X-axis Column", columns, key="x_col")
                y_col = st.selectbox("Y-axis Column", [c for c in columns if c != x_col], key="y_col")
                color_col = st.selectbox("Color Column (optional)", ["None"] + [c for c in columns if c != x_col and c != y_col], key="color_col")
                
                # Additional options for specific chart types
                if viz_type == "Bar Chart":
                    orientation = st.selectbox("Orientation", ["vertical", "horizontal"])
                else:
                    orientation = "vertical"
            
            elif viz_type == "Scatter Plot":
                x_col = st.selectbox("X-axis Column", columns, key="x_col")
                y_col = st.selectbox("Y-axis Column", [c for c in columns if c != x_col], key="y_col")
                size_col = st.selectbox("Size Column (optional)", ["None"] + [c for c in columns if c != x_col and c != y_col], key="size_col")
                color_col = st.selectbox("Color Column (optional)", ["None"] + [c for c in columns if c != x_col and c != y_col and c != size_col], key="color_col")
                orientation = "vertical"
            
            elif viz_type == "Pie Chart":
                label_col = st.selectbox("Label Column", columns, key="label_col")
                value_col = st.selectbox("Value Column", [c for c in columns if c != label_col], key="value_col")
                x_col = label_col
                y_col = value_col
                color_col = "None"
                orientation = "vertical"
            
            elif viz_type == "Histogram":
                x_col = st.selectbox("Column", columns, key="x_col")
                bins = st.slider("Number of Bins", 5, 100, 20)
                y_col = None
                color_col = "None"
                orientation = "vertical"
            
            elif viz_type == "Heatmap":
                corr_method = st.selectbox("Correlation Method", ["pearson", "kendall", "spearman"])
                x_col = "index"
                y_col = "columns"
                color_col = "None"
                orientation = "vertical"
            
            # General customization options
            st.subheader("Customize Appearance")
            
            title = st.text_input("Chart Title", viz_name)
            x_axis_title = st.text_input("X-axis Title", x_col if x_col else "")
            y_axis_title = st.text_input("Y-axis Title", y_col if y_col else "")
            
            height = st.slider("Chart Height", 300, 1000, 500)
            width = st.slider("Chart Width", 400, 1200, 700)
            
            # Submit button
            submit_button = st.form_submit_button("Create Visualization")
            
            if submit_button:
                if viz_type == "Bar Chart":
                    fig = viz.create_bar_chart(x_col, y_col, color_col if color_col != "None" else None, title, x_axis_title, y_axis_title, orientation, height, width)
                
                elif viz_type == "Line Chart":
                    fig = viz.create_line_chart(x_col, y_col, color_col if color_col != "None" else None, title, x_axis_title, y_axis_title, height, width)
                
                elif viz_type == "Scatter Plot":
                    fig = viz.create_scatter_plot(x_col, y_col, size_col if size_col != "None" else None, color_col if color_col != "None" else None, title, x_axis_title, y_axis_title, height, width)
                
                elif viz_type == "Pie Chart":
                    fig = viz.create_pie_chart(label_col, value_col, title, height, width)
                
                elif viz_type == "Histogram":
                    fig = viz.create_histogram(x_col, bins, title, x_axis_title, height, width)
                
                elif viz_type == "Box Plot":
                    fig = viz.create_box_plot(x_col, y_col, color_col if color_col != "None" else None, title, x_axis_title, y_axis_title, height, width)
                
                elif viz_type == "Heatmap":
                    fig = viz.create_heatmap(corr_method, title, height, width)
                
                # Store visualization
                viz_data = {
                    "name": viz_name,
                    "type": viz_type,
                    "fig": fig,
                    "config": {
                        "x_col": x_col,
                        "y_col": y_col,
                        "color_col": color_col,
                        "title": title,
                        "x_axis_title": x_axis_title,
                        "y_axis_title": y_axis_title,
                        "height": height,
                        "width": width
                    }
                }
                
                # Add specific config parameters based on chart type
                if viz_type == "Bar Chart":
                    viz_data["config"]["orientation"] = orientation
                elif viz_type == "Scatter Plot":
                    viz_data["config"]["size_col"] = size_col
                elif viz_type == "Histogram":
                    viz_data["config"]["bins"] = bins
                elif viz_type == "Heatmap":
                    viz_data["config"]["corr_method"] = corr_method
                
                st.session_state.visualizations.append(viz_data)
                st.success(f"Created {viz_type}: {viz_name}")
        
        # Display existing visualizations
        st.header("Your Visualizations")
        
        if not st.session_state.visualizations:
            st.info("No visualizations created yet. Use the form above to create one.")
        else:
            for i, viz_item in enumerate(st.session_state.visualizations):
                with st.expander(f"{viz_item['name']} ({viz_item['type']})", expanded=i == len(st.session_state.visualizations) - 1):
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        st.plotly_chart(viz_item["fig"], use_container_width=True)
                    
                    with col2:
                        st.markdown("### Actions")
                        
                        if st.button("Add to Dashboard", key=f"add_dashboard_{i}"):
                            if viz_item not in st.session_state.dashboard_items:
                                st.session_state.dashboard_items.append(viz_item)
                                st.success(f"Added {viz_item['name']} to dashboard")
                            else:
                                st.info("This visualization is already in the dashboard")
                        
                        if st.button("Delete", key=f"delete_{i}"):
                            st.session_state.visualizations.pop(i)
                            st.success("Deleted visualization")
                            st.rerun()
                        
                        export_format = st.selectbox("Export as", ["PNG", "HTML", "JSON"], key=f"export_format_{i}")
                        
                        if st.button("Export", key=f"export_{i}"):
                            if export_format == "PNG":
                                st.download_button(
                                    label="Download PNG",
                                    data=utils.fig_to_png(viz_item["fig"]),
                                    file_name=f"{viz_item['name'].replace(' ', '_')}.png",
                                    mime="image/png"
                                )
                            elif export_format == "HTML":
                                st.download_button(
                                    label="Download HTML",
                                    data=utils.fig_to_html(viz_item["fig"]),
                                    file_name=f"{viz_item['name'].replace(' ', '_')}.html",
                                    mime="text/html"
                                )
                            elif export_format == "JSON":
                                st.download_button(
                                    label="Download JSON",
                                    data=utils.fig_to_json(viz_item["fig"]),
                                    file_name=f"{viz_item['name'].replace(' ', '_')}.json",
                                    mime="application/json"
                                )

# Dashboard
elif app_mode == "Dashboard":
    st.header("Your Dashboard")
    
    if not st.session_state.dashboard_items:
        st.info("No items in the dashboard yet. Add visualizations from the Visualizations section.")
    else:
        # Dashboard title
        dashboard_title = st.text_input("Dashboard Title", "My Data Dashboard")
        
        # Dashboard layout options
        layout = st.selectbox("Layout", ["1 Column", "2 Columns", "3 Columns"])
        
        # Save current dashboard configuration
        if st.button("Save Dashboard Layout"):
            st.success("Dashboard layout saved")
        
        # Display dashboard
        st.subheader(dashboard_title)
        
        if layout == "1 Column":
            for i, item in enumerate(st.session_state.dashboard_items):
                with st.container():
                    st.plotly_chart(item["fig"], use_container_width=True)
                    
                    cols = st.columns([1, 1, 1])
                    with cols[0]:
                        if st.button("Remove", key=f"remove_{i}"):
                            st.session_state.dashboard_items.pop(i)
                            st.success("Removed from dashboard")
                            st.rerun()
                    
                    with cols[2]:
                        if i > 0 and st.button("Move Up", key=f"up_{i}"):
                            st.session_state.dashboard_items[i], st.session_state.dashboard_items[i-1] = st.session_state.dashboard_items[i-1], st.session_state.dashboard_items[i]
                            st.rerun()
        
        elif layout == "2 Columns":
            for i in range(0, len(st.session_state.dashboard_items), 2):
                cols = st.columns(2)
                
                with cols[0]:
                    if i < len(st.session_state.dashboard_items):
                        st.plotly_chart(st.session_state.dashboard_items[i]["fig"], use_container_width=True)
                        
                        action_cols = st.columns([1, 1, 1])
                        with action_cols[0]:
                            if st.button("Remove", key=f"remove_{i}"):
                                st.session_state.dashboard_items.pop(i)
                                st.success("Removed from dashboard")
                                st.rerun()
                        
                        with action_cols[2]:
                            if i > 0 and st.button("Move Up", key=f"up_{i}"):
                                st.session_state.dashboard_items[i], st.session_state.dashboard_items[i-1] = st.session_state.dashboard_items[i-1], st.session_state.dashboard_items[i]
                                st.rerun()
                
                with cols[1]:
                    if i+1 < len(st.session_state.dashboard_items):
                        st.plotly_chart(st.session_state.dashboard_items[i+1]["fig"], use_container_width=True)
                        
                        action_cols = st.columns([1, 1, 1])
                        with action_cols[0]:
                            if st.button("Remove", key=f"remove_{i+1}"):
                                st.session_state.dashboard_items.pop(i+1)
                                st.success("Removed from dashboard")
                                st.rerun()
                        
                        with action_cols[2]:
                            if i+1 > 0 and st.button("Move Up", key=f"up_{i+1}"):
                                st.session_state.dashboard_items[i+1], st.session_state.dashboard_items[i] = st.session_state.dashboard_items[i], st.session_state.dashboard_items[i+1]
                                st.rerun()
        
        else:  # 3 Columns
            for i in range(0, len(st.session_state.dashboard_items), 3):
                cols = st.columns(3)
                
                for j in range(3):
                    with cols[j]:
                        if i+j < len(st.session_state.dashboard_items):
                            st.plotly_chart(st.session_state.dashboard_items[i+j]["fig"], use_container_width=True)
                            
                            action_cols = st.columns([1, 1])
                            with action_cols[0]:
                                if st.button("Remove", key=f"remove_{i+j}"):
                                    st.session_state.dashboard_items.pop(i+j)
                                    st.success("Removed from dashboard")
                                    st.rerun()
                            
                            with action_cols[1]:
                                if i+j > 0 and st.button("Move Up", key=f"up_{i+j}"):
                                    idx = i+j
                                    st.session_state.dashboard_items[idx], st.session_state.dashboard_items[idx-1] = st.session_state.dashboard_items[idx-1], st.session_state.dashboard_items[idx]
                                    st.rerun()
        
        # Export dashboard
        st.subheader("Export Dashboard")
        
        export_format = st.selectbox("Export Dashboard as", ["HTML", "PDF"])
        
        if st.button("Export Dashboard"):
            if export_format == "HTML":
                dashboard_html = Dashboard.export_dashboard_html(dashboard_title, st.session_state.dashboard_items, layout)
                st.download_button(
                    label="Download HTML Dashboard",
                    data=dashboard_html,
                    file_name=f"{dashboard_title.replace(' ', '_')}_dashboard.html",
                    mime="text/html"
                )
            else:
                st.warning("PDF export functionality is still in development.")

# Sharing Options
elif app_mode == "Sharing":
    st.header("Share Your Analysis")
    
    st.subheader("Export Data")
    if st.session_state.processed_data is not None:
        export_data_format = st.selectbox("Export Processed Data as", ["CSV", "Excel", "JSON"])
        
        if st.button("Export Processed Data"):
            if export_data_format == "CSV":
                csv = utils.df_to_csv(st.session_state.processed_data)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="processed_data.csv",
                    mime="text/csv"
                )
            elif export_data_format == "Excel":
                excel = utils.df_to_excel(st.session_state.processed_data)
                st.download_button(
                    label="Download Excel",
                    data=excel,
                    file_name="processed_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            elif export_data_format == "JSON":
                json_str = utils.df_to_json(st.session_state.processed_data)
                st.download_button(
                    label="Download JSON",
                    data=json_str,
                    file_name="processed_data.json",
                    mime="application/json"
                )
    else:
        st.warning("No processed data available. Import and process data first.")
    
    st.subheader("Share Visualizations")
    if st.session_state.visualizations:
        selected_viz = st.selectbox(
            "Select Visualization to Share",
            [viz["name"] for viz in st.session_state.visualizations]
        )
        
        viz_index = next((i for i, viz in enumerate(st.session_state.visualizations) if viz["name"] == selected_viz), 0)
        viz_to_share = st.session_state.visualizations[viz_index]
        
        st.plotly_chart(viz_to_share["fig"], use_container_width=True)
        
        sharing_format = st.selectbox("Share as", ["Link", "Embed Code", "Export File"])
        
        if sharing_format == "Link":
            st.info("This feature would generate a shareable link to your visualization in a production environment.")
            st.text("https://example.com/share/visualization/abc123")
        
        elif sharing_format == "Embed Code":
            embed_code = utils.get_embed_code(viz_to_share["fig"])
            st.code(embed_code, language="html")
            st.info("Copy this code to embed the visualization in your website or document.")
        
        elif sharing_format == "Export File":
            export_viz_format = st.selectbox("Export File Format", ["PNG", "SVG", "HTML", "JSON"])
            
            if st.button("Export Visualization"):
                if export_viz_format == "PNG":
                    st.download_button(
                        label="Download PNG",
                        data=utils.fig_to_png(viz_to_share["fig"]),
                        file_name=f"{selected_viz.replace(' ', '_')}.png",
                        mime="image/png"
                    )
                elif export_viz_format == "SVG":
                    st.download_button(
                        label="Download SVG",
                        data=utils.fig_to_svg(viz_to_share["fig"]),
                        file_name=f"{selected_viz.replace(' ', '_')}.svg",
                        mime="image/svg+xml"
                    )
                elif export_viz_format == "HTML":
                    st.download_button(
                        label="Download HTML",
                        data=utils.fig_to_html(viz_to_share["fig"]),
                        file_name=f"{selected_viz.replace(' ', '_')}.html",
                        mime="text/html"
                    )
                elif export_viz_format == "JSON":
                    st.download_button(
                        label="Download JSON",
                        data=utils.fig_to_json(viz_to_share["fig"]),
                        file_name=f"{selected_viz.replace(' ', '_')}.json",
                        mime="application/json"
                    )
    else:
        st.warning("No visualizations available. Create visualizations first.")
    
    st.subheader("Share Dashboard")
    if st.session_state.dashboard_items:
        dashboard_title = st.text_input("Dashboard Title for Sharing", "My Data Dashboard")
        
        dashboard_format = st.selectbox("Share Dashboard as", ["HTML", "Link"])
        
        if dashboard_format == "HTML":
            if st.button("Export Dashboard as HTML"):
                dashboard_html = Dashboard.export_dashboard_html(dashboard_title, st.session_state.dashboard_items, "2 Columns")
                st.download_button(
                    label="Download HTML Dashboard",
                    data=dashboard_html,
                    file_name=f"{dashboard_title.replace(' ', '_')}_dashboard.html",
                    mime="text/html"
                )
        
        elif dashboard_format == "Link":
            st.info("This feature would generate a shareable link to your dashboard in a production environment.")
            st.text("https://example.com/share/dashboard/xyz789")
    else:
        st.warning("No dashboard items available. Add visualizations to your dashboard first.")

# API Integration
elif app_mode == "API Integration":
    st.header("API Integration for Technical Teams")
    
    st.markdown("""
    This section provides information for technical teams to integrate with the data and visualizations 
    through API endpoints. The API is built with FastAPI and provides endpoints to:

    1. Retrieve data in various formats
    2. Get visualization configurations
    3. Generate visualization images
    4. Access dashboard configurations
    """)
    
    st.subheader("API Base URL")
    st.code("http://localhost:8000", language="bash")
    
    st.subheader("API Documentation")
    st.markdown("""
    When the API server is running, you can access the interactive documentation at:
    - Swagger UI: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc
    """)
    
    st.subheader("Available Endpoints")
    
    endpoints = [
        {
            "method": "GET",
            "path": "/api/data",
            "description": "Get the processed dataset in JSON format",
            "query_params": "format=[json|csv]",
            "example": "GET /api/data?format=json"
        },
        {
            "method": "GET",
            "path": "/api/visualizations",
            "description": "Get a list of all available visualizations",
            "example": "GET /api/visualizations"
        },
        {
            "method": "GET",
            "path": "/api/visualizations/{viz_id}",
            "description": "Get a specific visualization configuration",
            "example": "GET /api/visualizations/1"
        },
        {
            "method": "GET",
            "path": "/api/visualizations/{viz_id}/image",
            "description": "Get a visualization as an image",
            "query_params": "format=[png|svg]",
            "example": "GET /api/visualizations/1/image?format=png"
        },
        {
            "method": "GET",
            "path": "/api/dashboard",
            "description": "Get the dashboard configuration",
            "example": "GET /api/dashboard"
        },
        {
            "method": "POST",
            "path": "/api/data/upload",
            "description": "Upload a new dataset (CSV, Excel, or JSON)",
            "example": "POST /api/data/upload with form data containing the file"
        }
    ]
    
    for endpoint in endpoints:
        with st.expander(f"{endpoint['method']} {endpoint['path']}"):
            st.markdown(f"**Description:** {endpoint['description']}")
            if "query_params" in endpoint:
                st.markdown(f"**Query Parameters:** {endpoint['query_params']}")
            st.markdown(f"**Example:** `{endpoint['example']}`")
            
            if endpoint['method'] == "GET":
                st.code(f"curl -X GET \"http://localhost:8000{endpoint['path'].split('{')[0]}1" + 
                       (f"?{endpoint['query_params'].split('=')[0]}={endpoint['query_params'].split('=')[1].split('|')[0]}" 
                        if "query_params" in endpoint else "") + 
                       "\"", language="bash")
    
    st.subheader("API Server Status")
    
    if st.button("Check API Server Status"):
        try:
            # This is just a placeholder - in a real environment we would actually check the API
            st.success("API server is running and accessible at http://localhost:8000")
        except:
            st.error("API server is not running. Technical team needs to start the server.")
    
    st.subheader("Run API Server")
    st.markdown("""
    To run the API server, execute the following command in the terminal:
    ```
    uvicorn api:app --host 0.0.0.0 --port 8000 --reload
    ```
    """)
    
    st.subheader("Python Integration Example")
    st.code("""
import requests
import pandas as pd
import json

# Get the processed data as JSON
response = requests.get("http://localhost:8000/api/data?format=json")
data = response.json()
df = pd.DataFrame(data)

# Get available visualizations
response = requests.get("http://localhost:8000/api/visualizations")
visualizations = response.json()
print(f"Available visualizations: {visualizations}")

# Get a specific visualization configuration
viz_id = 1  # Replace with the actual visualization ID
response = requests.get(f"http://localhost:8000/api/visualizations/{viz_id}")
viz_config = response.json()
print(f"Visualization config: {viz_config}")

# Download a visualization as an image
response = requests.get(f"http://localhost:8000/api/visualizations/{viz_id}/image?format=png")
with open(f"visualization_{viz_id}.png", "wb") as f:
    f.write(response.content)
print(f"Saved visualization_{viz_id}.png")
    """, language="python")
    
    st.subheader("JavaScript Integration Example")
    st.code("""
// Get the processed data as JSON
fetch('http://localhost:8000/api/data?format=json')
  .then(response => response.json())
  .then(data => {
    console.log('Data:', data);
    // Process the data...
  });

// Get available visualizations
fetch('http://localhost:8000/api/visualizations')
  .then(response => response.json())
  .then(visualizations => {
    console.log('Available visualizations:', visualizations);
    // Use the visualizations...
  });

// Get a specific visualization configuration
const vizId = 1;  // Replace with the actual visualization ID
fetch(`http://localhost:8000/api/visualizations/${vizId}`)
  .then(response => response.json())
  .then(vizConfig => {
    console.log('Visualization config:', vizConfig);
    // Use the visualization config...
  });

// Display a visualization image
const displayImage = (vizId) => {
  const imgElement = document.createElement('img');
  imgElement.src = `http://localhost:8000/api/visualizations/${vizId}/image?format=png`;
  document.body.appendChild(imgElement);
};

displayImage(1);  // Replace with the actual visualization ID
    """, language="javascript")
