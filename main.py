import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

# Initialize options for length and language
LENGTH_OPTIONS = ["Short", "Medium", "Long"]
LANGUAGE_OPTIONS = ["English", "Hinglish"]

# Function to set up the UI and generate the LinkedIn post
def main():
    st.title("LinkedIn Post Generator: Codebasics")

    # Initialize the FewShotPosts class and fetch available tags
    fs = FewShotPosts()
    tags = fs.get_tags()

    # User input section using columns for layout
    st.subheader("Select Parameters for Your Post")
    selected_tag = st.selectbox("Choose a Topic:", options=tags, index=0)
    selected_length = st.selectbox("Select Post Length:", options=LENGTH_OPTIONS, index=0)
    selected_language = st.selectbox("Select Language:", options=LANGUAGE_OPTIONS, index=0)

    # Generate and display post when the button is clicked
    if st.button("Generate Post"):
        with st.spinner("Generating your post..."):
            post = generate_post(selected_length, selected_language, selected_tag)
        st.success("Your LinkedIn post is ready!")
        st.write(post)

    # Add a footer for better user engagement
    st.markdown(
        """
        ---
        *Made with ❤️ using Streamlit | Follow [Codebasics](https://www.codebasics.io)*
        """
    )

# Entry point for the Streamlit app
if __name__ == "__main__":
    main()

