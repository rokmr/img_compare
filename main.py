import streamlit as st
from streamlit_image_comparison import image_comparison
from streamlit_js_eval import streamlit_js_eval
from PIL import Image
import os
# Custom theme settings
st.set_page_config(
    page_title="Image-Comparison",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load and apply custom CSS
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('style.css')

def main():
    st.title("Image Comparison Tool")
    st.subheader("Compare two images with an interactive slider")

    n = st.number_input("Number of folders", min_value=1, value=2)

    # Make n columns
    cols = st.columns(n)
    DEFAULT_WIDTH = 1200  # Default width in pixels
    container_width = streamlit_js_eval(js_expressions='window.innerWidth', key='WIDTH', want_output=True)
    if container_width is None:
        container_width = DEFAULT_WIDTH
    
    padding = 10  # Account for padding between columns
    width = (container_width // n) - (2 * padding)  # Divide width by number of columns

    # For each column, make a folder input and image comparator
    for i, col in enumerate(cols):
        with col:  # Use 'with' statement to ensure everything is in the column
            folder_path = st.text_input("Folder path", value=f"folder{i+1}", key=f"folder_{i}")
            image_paths = [os.path.join(folder_path, f) for f in sorted(os.listdir(folder_path)) 
                             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            use_image_comparison = st.toggle("overlay slider", value=True, key=f"use_image_comparison_{i}")
            if use_image_comparison:
                second_folder_path = st.text_input("Second folder path", value=f"folder{i+1}", key=f"second_folder_{i}")
                second_image_paths = [os.path.join(second_folder_path, f) for f in sorted(os.listdir(second_folder_path)) 
                                            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
                for image_path1, image_path2 in zip(image_paths, second_image_paths):
                    image_comparison(
                        img1=image_path1,
                        img2=image_path2,
                        label1="Original",
                        label2="Modified",
                        width=width,
                        show_labels=True,
                        starting_position=50,
                        make_responsive=True,
                        in_memory=True
                    )
            else:
                for image_path in image_paths:
                    st.image(image_path, use_container_width=True)

if __name__ == "__main__":
    main()