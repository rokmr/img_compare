import streamlit as st
from streamlit_image_comparison import image_comparison
from streamlit_js_eval import streamlit_js_eval
from PIL import Image

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

    # Set default container width and try to get actual width
    DEFAULT_WIDTH = 1200  # Default width in pixels
    container_width = streamlit_js_eval(js_expressions='window.innerWidth', key='WIDTH', want_output=True)
    
    # Use default width if JavaScript evaluation fails
    if container_width is None:
        container_width = DEFAULT_WIDTH
    
    padding = 10  # Account for padding between columns
    width = (container_width // n) - (2 * padding)  # Divide width by number of columns

    # For each column, make a folder input and image comparator
    for i, col in enumerate(cols):
        with col:  # Use 'with' statement to ensure everything is in the column
            # Create the text input for folder path
            folder_path = st.text_input("Folder path", value=f"folder{i+1}", key=f"folder_{i}")
            
            # Load image for this column
            image_path = f"{folder_path}/{i+1}.png"
            try:
                image = Image.open(image_path)
                aspect_ratio = image.height / image.width
                height = int(width * aspect_ratio)
            except:
                height = width  # fallback height if image can't be loaded

            # Create image comparator in this column
            image_comparison(
                img1=image_path,
                img2=image_path,
                label1="Original",
                label2="Modified",
                width=width,
                show_labels=True,
                starting_position=50,
                make_responsive=True,
                in_memory=True
            )

    folder1_path = "folder1"
    folder2_path = "folder2"


    foldercol1, col2 = st.columns(2)




    # Configuration options in a more compact layout
    col1, col2 = st.columns(2)
    with col1:
        show_labels = st.checkbox("Show Labels", value=True)
        starting_pos = st.slider("Starting Position", 0, 100, 50)
    with col2:
        make_responsive = st.checkbox("Responsive Mode", value=True)
        label1 = st.text_input("Label for Image 1", value="Original")
        label2 = st.text_input("Label for Image 2", value="Modified")

    # Load images to get dimensions
    # image1 = Image.open(image1_path)
    width = st.session_state.get('folder_path', 700)
    
    # Calculate height while maintaining aspect ratio
    # aspect_ratio = image1.height / image1.width
    # height = int(width * aspect_ratio)

    # Image comparison component


    # Add information about the comparison
    with st.expander("About this comparison"):
        st.write("""
        This tool allows you to compare two images using an interactive slider.
        - Drag the slider left or right to compare the images
        - Adjust the width and starting position as needed
        - Toggle labels and responsive mode
        - Labels can be customized for better context
        """)

if __name__ == "__main__":
    main()