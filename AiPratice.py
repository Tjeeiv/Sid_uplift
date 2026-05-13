import shutil
import streamlit as st
from gradio_client import Client

st.set_page_config(page_title="Text → Image", page_icon="🎨")
st.title("🎨 Text → Image")
st.caption("Powered by Stable Cascade on Hugging Face")

prompt = st.text_area("Prompt", placeholder="A futuristic city at sunset, cinematic lighting...", height=120)
negative_prompt = st.text_input("Negative Prompt (optional)", placeholder="blurry, low quality, distorted")

col1, col2, col3 = st.columns(3)
with col1:
    width = st.selectbox("Width", [512, 768, 1024], index=2)
with col2:
    height = st.selectbox("Height", [512, 768, 1024], index=2)
with col3:
    seed = st.number_input("Seed (0 = random)", min_value=0, max_value=999999, value=0)

if st.button("✨ Generate Image", use_container_width=True):
    if prompt.strip() == "":
        st.warning("Please enter a prompt first.")
    else:
        with st.spinner("Connecting to Stable Cascade and generating your image..."):
            try:
                client = Client("multimodalart/stable-cascade")
                result = client.predict(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    seed=seed,
                    width=width,
                    height=height,
                    prior_num_inference_steps=20,
                    prior_guidance_scale=4.0,
                    decoder_num_inference_steps=10,
                    decoder_guidance_scale=0.0,
                    num_images_per_prompt=1,
                    api_name="/run"
                )

                # result is a list; each item is a dict with 'image' key or a file path
                if isinstance(result, list) and len(result) > 0:
                    item = result[0]
                    if isinstance(item, dict):
                        image_path = item.get("image") or item.get("path") or list(item.values())[0]
                    else:
                        image_path = item

                    output_path = "generated_image.png"
                    shutil.copy(image_path, output_path)

                    st.success("Image generated!")
                    st.image(output_path, caption=prompt, use_container_width=True)

                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Image",
                            data=f,
                            file_name="stable_cascade_output.png",
                            mime="image/png",
                            use_container_width=True
                        )
                else:
                    st.error("No image returned. Try again.")

            except Exception as e:
                st.error(f"Error: {e}")