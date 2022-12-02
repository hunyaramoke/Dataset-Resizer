import gradio as gr

from modules import script_callbacks
import modules.shared as shared

from PIL import Image
import glob
import os


def on_ui_tabs():
    with gr.Blocks() as dr_interface:
        with gr.Row(equal_height=True):
            with gr.Column(variant='panel'):
                with gr.Column(variant='panel'):
                    input_dir = gr.Textbox(label="Input directory", placeholder="Input directory", value="")
                    output_dir = gr.Textbox(label="Output directory", placeholder="Output directory", value="")
                with gr.Column(variant='panel'):
                    padding_background = gr.Radio(choices=["Transparent", "White"], value="Transparent", label="Background")
                    width = gr.Textbox(label="Width", placeholder="Width", value="512")
                    height= gr.Textbox(label="Height", placeholder="Height", value="512")
            with gr.Column(variant='panel'):
                status = gr.Textbox(label="", interactive=False, show_progress=True)
                
        
        dir_run = gr.Button(elem_id="dir_run", label="Generate", variant='primary')
        
        dir_run.click(
            fn=main,
            inputs=[input_dir, output_dir,padding_background, width, height],
            outputs=[status]
        )

      
    return (dr_interface, "Dataset Resizer", "dr_interface"),


script_callbacks.on_ui_tabs(on_ui_tabs)


def expand2square(pil_img, background_color):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new("RGBA", (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new("RGBA", (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result


def main(input_dir, output_dir,padding_background, width, height):
    files = glob.glob(input_dir + "/*")
    for file in files:
        print("input:" + file)
        im = Image.open(file)
        if padding_background == "Transparent":
            im_new = expand2square(im, (0, 0, 0, 0)).resize((int(width), int(height)))
        elif padding_background == "White":
            im_new = expand2square(im, (255, 255, 255, 255)).resize((int(width), int(height)))
        print("output;" + output_dir + "/" + file.split('/')[-1])
        im_new.save(output_dir + "/" + os.path.split(file)[1], quality=95)
        
    
    print("Resize_finished")
    return "Resize finished"