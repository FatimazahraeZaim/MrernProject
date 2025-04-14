from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import json
import plotly.io as pio
from typing import Optional, List, Dict, Any
import uvicorn

app = FastAPI(title="PM Data Analytics API", description="API for product managers data analytics tool")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state (in a production environment, this would be stored in a database)
_data = None
_visualizations = []
_dashboard_items = []

@app.get("/api/data", response_class=JSONResponse)
async def get_data(format: str = Query("json", regex=r"^(json|csv)$")):
    """
    Get the processed dataset
    
    Args:
        format: Output format (json or csv)
        
    Returns:
        Dataset in the requested format
    """
    global _data
    
    if _data is None:
        raise HTTPException(status_code=404, detail="No data available. Please upload data first.")
    
    if format == "json":
        # Convert to JSON
        return JSONResponse(content=json.loads(_data.to_json(orient="records")))
    else:  # csv
        # Convert to CSV
        csv_data = _data.to_csv(index=False)
        return Response(content=csv_data, media_type="text/csv")

@app.post("/api/data/upload")
async def upload_data(file: UploadFile = File(...)):
    """
    Upload a new dataset
    
    Args:
        file: Uploaded file (CSV, Excel, or JSON)
        
    Returns:
        Success message and data preview
    """
    global _data
    
    try:
        content = await file.read()
        file_extension = file.filename.split('.')[-1].lower()
        
        if file_extension == 'csv':
            _data = pd.read_csv(io.BytesIO(content))
        elif file_extension in ['xlsx', 'xls']:
            _data = pd.read_excel(io.BytesIO(content))
        elif file_extension == 'json':
            _data = pd.read_json(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file format: {file_extension}")
        
        return {
            "message": f"Successfully uploaded data with {_data.shape[0]} rows and {_data.shape[1]} columns",
            "preview": json.loads(_data.head().to_json(orient="records"))
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading data: {str(e)}")

@app.get("/api/visualizations", response_class=JSONResponse)
async def get_visualizations():
    """
    Get a list of all available visualizations
    
    Returns:
        List of visualization metadata
    """
    viz_metadata = []
    
    for i, viz in enumerate(_visualizations):
        viz_metadata.append({
            "id": i,
            "name": viz["name"],
            "type": viz["type"],
            "config": viz["config"]
        })
    
    return viz_metadata

@app.get("/api/visualizations/{viz_id}", response_class=JSONResponse)
async def get_visualization(viz_id: int):
    """
    Get a specific visualization configuration
    
    Args:
        viz_id: Visualization ID
        
    Returns:
        Visualization configuration
    """
    if viz_id < 0 or viz_id >= len(_visualizations):
        raise HTTPException(status_code=404, detail=f"Visualization with ID {viz_id} not found")
    
    viz = _visualizations[viz_id]
    
    return {
        "id": viz_id,
        "name": viz["name"],
        "type": viz["type"],
        "config": viz["config"]
    }

@app.get("/api/visualizations/{viz_id}/image")
async def get_visualization_image(viz_id: int, format: str = Query("png", regex=r"^(png|svg)$")):
    """
    Get a visualization as an image
    
    Args:
        viz_id: Visualization ID
        format: Image format (png or svg)
        
    Returns:
        Visualization image
    """
    if viz_id < 0 or viz_id >= len(_visualizations):
        raise HTTPException(status_code=404, detail=f"Visualization with ID {viz_id} not found")
    
    viz = _visualizations[viz_id]
    fig = viz["fig"]
    
    if format == "png":
        img_bytes = pio.to_image(fig, format="png")
        return Response(content=img_bytes, media_type="image/png")
    else:  # svg
        img_bytes = pio.to_image(fig, format="svg")
        return Response(content=img_bytes, media_type="image/svg+xml")

@app.get("/api/dashboard", response_class=JSONResponse)
async def get_dashboard():
    """
    Get the dashboard configuration
    
    Returns:
        Dashboard configuration
    """
    dashboard_data = []
    
    for i, item in enumerate(_dashboard_items):
        dashboard_data.append({
            "id": i,
            "name": item["name"],
            "type": item["type"],
            "config": item["config"]
        })
    
    return {
        "items": dashboard_data
    }

@app.post("/api/visualizations", response_class=JSONResponse)
async def create_visualization(visualization_data: Dict[str, Any]):
    """
    Create a new visualization (Note: This is a simplified version,
    in a real implementation this would create a new visualization based on
    the provided configuration)
    
    Args:
        visualization_data: Visualization configuration
        
    Returns:
        Created visualization metadata
    """
    # This is a placeholder - in a real implementation, we would:
    # 1. Validate the visualization data
    # 2. Create the visualization
    # 3. Store it in the list or database
    
    return {
        "message": "Visualization creation from API is not implemented in this demo",
        "received_data": visualization_data
    }

# Run the API server when this module is executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
