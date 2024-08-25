from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from src.config.argument_config import ArgumentConfig
from src.config.inference_config import InferenceConfig
from src.config.crop_config import CropConfig
from src.live_portrait_pipeline import LivePortraitPipeline

from server.dto import InferenceHumanRequest

import os.path as osp
from src.utils.helper import basename

router = APIRouter()

def partial_fields(target_class, kwargs):
    return target_class(**{k: v for k, v in kwargs.items() if hasattr(target_class, k)})

def fast_check_args(args):
    if not osp.exists(args.source):
        raise HTTPException(status_code=404, detail=f"Source info not found: {args.source}")
    if not osp.exists(args.driving):
        raise HTTPException(status_code=404, detail=f"Driving info not found: {args.driving}")

@router.post("/human_inference/")
async def human_inference(req: InferenceHumanRequest) -> FileResponse:
    args = ArgumentConfig(**(req.dict()))
    
    fast_check_args(args)

    # specify configs for inference
    inference_cfg = partial_fields(InferenceConfig, args.__dict__)
    crop_cfg = partial_fields(CropConfig, args.__dict__)

    live_portrait_pipeline = LivePortraitPipeline(
        inference_cfg=inference_cfg,
        crop_cfg=crop_cfg
    )

    # run
    live_portrait_pipeline.execute(args)
    
    vid_path = osp.join(args.output_dir, f'{basename(args.source)}--{basename(args.driving)}.mp4')
        
    response = FileResponse(vid_path)

    return response