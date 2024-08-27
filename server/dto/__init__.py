from pydantic import BaseModel, Field
from typing import Literal, Optional

class InferenceHumanRequest(BaseModel):
    ########## input arguments ##########
    source: str = Field(..., descripition="path to the source portrait (human/animal) or video (human)"),
    driving: str = Field(..., descripition="path to driving video or template (.pkl format)"),

    ########## inference arguments ##########
    flag_use_half_precision: Optional[bool] = Field(default=True,  description="whether to use half precision (FP16). If black boxes appear, it might be due to GPU incompatibility; set to False.")
    flag_crop_driving_video: Optional[bool] = Field(default=False, description="whether to crop the driving video, if the given driving info is a video")
    flag_normalize_lip: Optional[bool] = Field(default=False, description="whether to let the lip to close state before animation, only take effect when flag_eye_retargeting and flag_lip_retargeting is False")
    flag_source_video_eye_retargeting: Optional[bool] = Field(default=False, description="when the input is a source video, whether to let the eye-open scalar of each frame to be the same as the first source frame before the animation, only take effect when flag_eye_retargeting and flag_lip_retargeting is False, may cause the Optional[int]er-frame jittering") 
    flag_video_editing_head_rotation: Optional[bool] = Field(default=False, description="when the input is a source video, whether to inherit the relative head rotation from the driving video")
    flag_eye_retargeting: Optional[bool] = Field(default=False, description="not recommend to be True, WIP; whether to transfer the eyes-open ratio of each driving frame to the source image or the corresponding source frame")
    flag_lip_retargeting: Optional[bool] = Field(default=False, description="not recommend to be True, WIP; whether to transfer the lip-open ratio of each driving frame to the source image or the corresponding source frame")
    flag_stitching: Optional[bool] = Field(default=True, description="recommend to True if head movement is small, False if head movement is large or the source image is an animal")
    flag_relative_motion: Optional[bool] = Field(default=True, description="whether to use relative motion")
    flag_pasteback: Optional[bool] = Field(default=True, description="whether to paste-back/stitch the animated face cropping from the face-cropping space to the original image space")
    flag_do_crop: Optional[bool] = Field(default=True, description="whether to crop the source portrait or video to the face-cropping space")
    driving_option: Optional[Literal["expression-friendly", "pose-friendly"]] = Field(default="expression-friendly", description="'expression-friendly' or 'pose-friendly'; 'expression-friendly' would adapt the driving motion with the global multiplier, and could be used when the source is a human image") 
    driving_multiplier: Optional[float] = Field(default=1.0, description="be used only when driving_option is 'expression-friendly'")
    driving_smooth_observation_variance: Optional[float] = Field(default=3e-7, description="smooth strength scalar for the animated video when the input is a source video, the larger the number, the smoother the animated video; too much smoothness would result in loss of motion accuracy")
    audio_priority: Optional[Literal['source', 'driving']] = Field(default='driving', description="whether to use the audio from source or driving video")
    ########## source crop arguments ##########
    det_thresh: Optional[float] = Field(default=0.15, description="detection threshold")
    scale: Optional[float] = Field(default=2.3, description="the ratio of face area is smaller if scale is larger")
    vx_ratio: Optional[float] = Field(default=0, description="the ratio to move the face to left or right in cropping space")
    vy_ratio: Optional[float] = Field(default=-0.125, description="the ratio to move the face to left or right in cropping space")
    flag_do_rot: Optional[bool] = Field(default=True, description="whether to conduct the rotation when flag_do_crop is True")
    source_max_dim: Optional[int] = Field(default=1280, description="the max dim of height and width of source image or video, you can change it to a larger number, e.g., 1920")
    source_division: Optional[int] = Field(default=2, description="make sure the height and width of source image or video can be divided by this number")

    ########## driving crop arguments ##########
    scale_crop_driving_video: Optional[float] = Field(default=2.2, description="scale factor for cropping driving video")
    vx_ratio_crop_driving_video: Optional[float] = Field(default=0., description="adjust y offset") 
    vy_ratio_crop_driving_video: Optional[float] = Field(default=-0.1, description="adjust x offset")

    flag_do_torch_compile: Optional[bool] = Field(default=False, description="whether to use torch.compile to accelerate generation")
    loop: Optional[bool] = Field(default=False, description="whether to make output video's duration same as source video's duration")