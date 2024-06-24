import os

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["PATH"] = "/usr/bin" + os.pathsep + os.environ["PATH"]

import gradio as gr  # noqa: E402
import cv2  # noqa: E402
import ffmpeg  # noqa: E402
from ultralytics import YOLOv10  # noqa: E402

last_model_id = None
model = None


def yolov10_inference(image, video, model_id, image_size, conf_threshold):
    global last_model_id, model
    if last_model_id is None or last_model_id != model_id:
        if model_id == "custom":
            model = YOLOv10("runs/detect/train/weights/best.pt")
        else:
            model = YOLOv10.from_pretrained(f"jameslahm/{model_id}", cache_dir="./models")
    last_model_id = model_id
    if image:
        results = model.predict(source=image, imgsz=image_size, conf=conf_threshold)
        annotated_image = results[0].plot()
        return annotated_image[:, :, ::-1], None
    else:
        video_path = "input.mp4"
        with open(video_path, "wb") as f:
            with open(video, "rb") as g:
                f.write(g.read())

        cap = cv2.VideoCapture(video)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        output_video_path = "output.mp4"

        process = (
            ffmpeg.input("pipe:", format="rawvideo", pix_fmt="bgr24", s=f"{frame_width}x{frame_height}")
            .output(output_video_path, vcodec="libx265", pix_fmt="yuv420p", r=fps)
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )

        # out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*"hvc1"), fps, (frame_width, frame_height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = model.predict(source=frame, imgsz=image_size, conf=conf_threshold)
            annotated_frame = results[0].plot()
            process.stdin.write(annotated_frame.tobytes())
            # out.write(annotated_frame)

        cap.release()
        process.stdin.close()
        # out.release()

        return None, output_video_path


def yolov10_inference_for_examples(image, model_path, image_size, conf_threshold):
    annotated_image, _ = yolov10_inference(image, None, model_path, image_size, conf_threshold)
    return annotated_image


def app():
    with gr.Blocks():
        with gr.Row():
            with gr.Column():
                image = gr.Image(type="pil", label="Image", visible=True)
                video = gr.Video(label="Video", visible=False, format="mp4")
                input_type = gr.Radio(
                    choices=["Image", "Video"],
                    value="Image",
                    label="Input Type",
                )
                model_id = gr.Dropdown(
                    label="Model",
                    choices=[
                        "yolov10n",
                        "yolov10s",
                        "yolov10m",
                        "yolov10b",
                        "yolov10l",
                        "yolov10x",
                        "custom",
                    ],
                    value="custom",
                )
                image_size = gr.Slider(
                    label="Image Size",
                    minimum=320,
                    maximum=1280,
                    step=32,
                    value=640,
                )
                conf_threshold = gr.Slider(
                    label="Confidence Threshold",
                    minimum=0.0,
                    maximum=1.0,
                    step=0.05,
                    value=0.25,
                )
                yolov10_infer = gr.Button(value="Detect Objects")

            with gr.Column():
                output_image = gr.Image(type="numpy", label="Annotated Image", visible=True)
                output_video = gr.Video(label="Annotated Video", visible=False, format="mp4")

        def update_visibility(input_type):
            image = gr.update(visible=True) if input_type == "Image" else gr.update(visible=False)
            video = gr.update(visible=False) if input_type == "Image" else gr.update(visible=True)
            output_image = gr.update(visible=True) if input_type == "Image" else gr.update(visible=False)
            output_video = gr.update(visible=False) if input_type == "Image" else gr.update(visible=True)

            return image, video, output_image, output_video

        input_type.change(
            fn=update_visibility,
            inputs=[input_type],
            outputs=[image, video, output_image, output_video],
        )

        def run_inference(image, video, model_id, image_size, conf_threshold, input_type):
            if input_type == "Image":
                return yolov10_inference(image, None, model_id, image_size, conf_threshold)
            else:
                return yolov10_inference(None, video, model_id, image_size, conf_threshold)

        yolov10_infer.click(
            fn=run_inference,
            inputs=[image, video, model_id, image_size, conf_threshold, input_type],
            outputs=[output_image, output_video],
        )

        gr.Examples(
            examples=[
                [
                    "ultralytics/assets/bus.jpg",
                    "yolov10s",
                    640,
                    0.25,
                ],
                [
                    "ultralytics/assets/zidane.jpg",
                    "yolov10s",
                    640,
                    0.25,
                ],
            ],
            fn=yolov10_inference_for_examples,
            inputs=[
                image,
                model_id,
                image_size,
                conf_threshold,
            ],
            outputs=[output_image],
            cache_examples="lazy",
        )


gradio_app = gr.Blocks()
with gradio_app:
    gr.HTML(
        """
    <h1 style='text-align: center'>
    YOLOv10: Real-Time End-to-End Object Detection
    </h1>
    """
    )
    gr.HTML(
        """
        <h3 style='text-align: center'>
        <a href='https://arxiv.org/abs/2405.14458' target='_blank'>arXiv</a> | <a href='https://github.com/THU-MIG/yolov10' target='_blank'>github</a>
        </h3>
        """
    )
    with gr.Row():
        with gr.Column():
            app()
if __name__ == "__main__":
    gradio_app.launch()
