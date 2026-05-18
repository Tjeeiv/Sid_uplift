import os
import shutil
import streamlit as st
from gradio_client import Client

st.set_page_config(page_title="Text → Image", page_icon="🎨")
st.title("Text → Image")
st.caption("Powered by Stable Cascade on Hugging Face")

prompt = st.text_area("Prompt", placeholder="A futuristic city at sunset, cinematic lighting...", height=120)
negative_prompt = st.text_input("Negative Prompt (optional)", placeholder="blurry, low quality, distorted")
 

if st.button("Generate Image", use_container_width=True):
    if prompt.strip() == "":
        st.warning("Please enter a prompt first.")
    else:
        with st.spinner("Generating your image..."):
            try:
                client = Client("multimodalart/stable-cascade")
                result = client.predict(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    seed=0,
                    width=1024,
                    height=1024,
                    prior_num_inference_steps=20,
                    prior_guidance_scale=4.0,
                    decoder_num_inference_steps=10,
                    decoder_guidance_scale=0.0,
                    num_images_per_prompt=1,
                    api_name="/run"
                )

                # Robustly extract image path from result
                image_path = None

                if isinstance(result, (list, tuple)) and len(result) > 0:
                    item = result[0]
                    if isinstance(item, (list, tuple)) and len(item) > 0:
                        item = item[0]  # handle nested list [[{...}]]
                    if isinstance(item, dict):
                        image_path = item.get("image") or item.get("path") or item.get("url") or list(item.values())[0]
                    elif isinstance(item, str):
                        image_path = item
                elif isinstance(result, dict):
                    image_path = result.get("image") or result.get("path") or list(result.values())[0]
                elif isinstance(result, str):
                    image_path = result

                if image_path:
                    # Save image in the same folder as app.py
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    output_path = os.path.join(script_dir, "generated_image.png")
                    shutil.copy(image_path, output_path)

                    st.success("Image generated!")
                    st.image(output_path, caption=prompt, use_container_width=True)

                    
                else:
                    st.error(f"Could not extract image. Raw result: {result}")

            except Exception as e:
                st.error(f"Error: {e}")