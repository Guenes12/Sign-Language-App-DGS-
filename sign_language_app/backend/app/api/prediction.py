import os
import tempfile
from fastapi import APIRouter, UploadFile, File
from app.services.prediction_service import PredictionService
from training.preprocessing.pipeline import PreprocessingPipeline
 
router = APIRouter()
service = PredictionService()
pipeline = PreprocessingPipeline()
 
 
@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    temp_path = None
    try:
        suffix = os.path.splitext(file.filename)[-1] or ".mp4"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
 
        sequence = pipeline.process_video(temp_path)
        result = service.predict(sequence)
        return result
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)