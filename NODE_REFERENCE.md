
# ComfyUI-WanAnimalPreprocessor — Node Reference

This pack registers **5 nodes**.  Each section lists the node's category, return types and every input widget exposed in ComfyUI.


## `AnimalPoseAndDetection` — Animal Pose and Detection

> Detects animal poses from images using ViTPose (AP10k/APT36k) and YOLO. Optionally retargets poses based on a reference image.

- **Category:** `WanAnimalPreprocess`
- **Returns:** `POSEDATA, STRING, BBOX` → `pose_data, key_frame_body_points, bboxes`

**Required inputs**

| Name | Type | Default (range) | Description |
|------|------|-----------------|-------------|
| `model` | POSEMODEL | `""`  | From ONNX Animal Detection Model Loader. |
| `images` | IMAGE | `""`  | Input video frames as IMAGE batch. |
| `width` | INT | `832` (min 64, max 2048, step 1) | Width of the generation |
| `height` | INT | `480` (min 64, max 2048, step 1) | Height of the generation |

**Optional inputs**

| Name | Type | Default (range) | Description |
|------|------|-----------------|-------------|
| `retarget_image` | IMAGE | `None`  | Optional reference image for pose retargeting |


## `AnimalPoseDetectionOneToAllAnimation` — Animal Pose Detection OneToAll Animation

> Specialized animal pose detection and alignment for OneToAllAnimation model. Detects animal poses from input images and aligns them based on a reference image if provided.

- **Category:** `WanAnimalPreprocess`
- **Returns:** `IMAGE, IMAGE, IMAGE, MASK` → `pose_images, ref_pose_image, ref_image, ref_mask`

**Required inputs**

| Name | Type | Default (range) | Description |
|------|------|-----------------|-------------|
| `model` | POSEMODEL | `""`  | From ONNX Animal Detection Model Loader. |
| `images` | IMAGE | `""`  | Input video frames as IMAGE batch. |
| `width` | INT | `832` (min 64, max 2048, step 2) | Width of the generation |
| `height` | INT | `480` (min 64, max 2048, step 2) | Height of the generation |
| `align_to` | combo[ref, pose, none] | `"ref"`  | Alignment mode for poses |
| `draw_head` | combo[full, weak, none] | `"full"`  | Whether to draw head keypoints on the pose images |

**Optional inputs**

| Name | Type | Default (range) | Description |
|------|------|-----------------|-------------|
| `ref_image` | IMAGE | `None`  | Optional reference image for pose retargeting |


## `AnimalPoseRetargetPromptHelper` — Animal Pose Retarget Prompt Helper

> Generates text prompts for animal pose retargeting based on visibility of limbs in the template pose.

- **Category:** `WanAnimalPreprocess`
- **Returns:** `STRING, STRING` → `prompt, retarget_prompt`

**Required inputs**

| Name | Type | Default (range) | Description |
|------|------|-----------------|-------------|
| `pose_data` | POSEDATA | `""`  | From Animal Pose and Detection. |


## `DrawAnimalViTPose` — Draw Animal ViTPose

> Draws animal pose skeleton images from pose data (AP10k/APT36k format).

- **Category:** `WanAnimalPreprocess`
- **Returns:** `IMAGE` → `pose_images`

**Required inputs**

| Name | Type | Default (range) | Description |
|------|------|-----------------|-------------|
| `pose_data` | POSEDATA | `""`  | From Animal Pose and Detection. |
| `width` | INT | `832` (min 64, max 2048, step 1) | Width of the generation |
| `height` | INT | `480` (min 64, max 2048, step 1) | Height of the generation |
| `retarget_padding` | INT | `16` (min 0, max 512, step 1) | When > 0, the retargeted pose image is padded and resized to the target size |
| `body_stick_width` | INT | `-1` (min -1, max 20, step 1) | Width of the body sticks. Set to 0 to disable body drawing, -1 for auto |
| `draw_head` | BOOLEAN | `True`  | Whether to draw head keypoints (eyes, nose) |


## `OnnxAnimalDetectionModelLoader` — ONNX Animal Detection Model Loader

> Loads ONNX models for animal pose detection. Supports both AP10k and APT36k datasets (both use 17 keypoints). Select the dataset matching your ViTPose model.

- **Category:** `WanAnimalPreprocess`
- **Returns:** `POSEMODEL` → `model`

**Required inputs**

| Name | Type | Default (range) | Description |
|------|------|-----------------|-------------|
| `vitpose_model` | combo[anim\vitpose-b-apt36k.onnx, anim\yolov8m.onnx, model.onnx, vitpose_h_wholebody_data.bin, vitpose_h_wholebody_model.onnx, yolov10m.onnx] | `""`  | ViTPose ONNX model for animal pose estimation. Loaded from 'ComfyUI/models/detection' folder. |
| `yolo_model` | combo[anim\vitpose-b-apt36k.onnx, anim\yolov8m.onnx, model.onnx, vitpose_h_wholebody_data.bin, vitpose_h_wholebody_model.onnx, yolov10m.onnx] | `""`  | YOLOv8 ONNX model for animal detection. Loaded from 'ComfyUI/models/detection' folder. |
| `dataset` | combo[ap10k, apt36k] | `"ap10k"`  | Dataset the ViTPose model was trained on. AP10k: 23 animal families, good for common animals (cat, dog, horse). APT36k: 30 species, broader coverage and more training data. |
| `onnx_device` | combo[CUDAExecutionProvider, CPUExecutionProvider] | `"CUDAExecutionProvider"`  | Device to run the ONNX models on |
