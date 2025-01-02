import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file, get_file
import time
from pathlib import Path
import tempfile
import os
from PIL import Image

st.set_page_config(
    page_title="Multimodal AI Agent",
    page_icon="🧬",
    layout="wide"
)

st.title("Multimodal AI Agent 🧬")

# Initialize single agent with both capabilities
@st.cache_resource
def initialize_agent():
    return Agent(
        name="Multimodal Analyst",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True,
    )

agent = initialize_agent()

# File uploader for both video and image (including jfif)
uploaded_video = st.file_uploader("Upload a video file", type=['mp4', 'mov', 'avi'])
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "jfif"])

# Function to resize images using Pillow
def resize_image(image_data, max_width=500, max_height=300):
    image = Image.open(image_data)
    image.thumbnail((max_width, max_height))  # Resize the image while maintaining aspect ratio
    return image

if uploaded_video:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        tmp_file.write(uploaded_video.read())
        video_path = tmp_file.name
    
    st.video(video_path)
    
    user_prompt = st.text_area(
        "What would you like to know about the video?",
        placeholder="Ask any question related to the video - the AI Agent will analyze it and search the web if needed",
        help="You can ask questions about the video content and get relevant information from the web"
    )
    
    if st.button("Analyze & Research Video"):
        if not user_prompt:
            st.warning("Please enter your question.")
        else:
            try:
                with st.spinner("Processing video and researching..."):
                    video_file = upload_file(video_path)
                    while video_file.state.name == "PROCESSING":
                        time.sleep(2)
                        video_file = get_file(video_file.name)

                    prompt = f"""
                    First analyze this video and then answer the following question using both 
                    the video analysis and web research: {user_prompt}
                    
                    Provide a comprehensive response focusing on practical, actionable information.
                    """
                    
                    result = agent.run(prompt, videos=[video_file])
                    
                st.subheader("Result")
                st.markdown(result.content)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            finally:
                Path(video_path).unlink(missing_ok=True)

elif uploaded_image:
    try:
        # Resize image before displaying and analyzing
        image_data = uploaded_image
        resized_image = resize_image(image_data)

        # Convert image to RGB before saving as JPEG
        resized_image = resized_image.convert("RGB")

        # Display the resized image
        st.image(resized_image, caption="Uploaded Image", use_container_width=True)

        # Input for dynamic task
        task_input = st.text_area(
            "Enter your task/question for the AI Agent regarding the image:"
        )

        # Button to process the image and task
        if st.button("Analyze Image") and task_input:
            with st.spinner("AI is thinking... 🤖"):
                try:
                    # Save the resized image in a temporary path (convert to RGB before saving)
                    temp_image_path = tempfile.mktemp(suffix='.jpg')
                    resized_image.save(temp_image_path)

                    response = agent.run(task_input, images=[temp_image_path])

                    # Display the response from the model
                    st.markdown("### AI Response:")
                    st.markdown(response.content)
                except Exception as e:
                    st.error(f"An error occurred during analysis: {str(e)}")
                finally:
                    # Clean up temp file
                    if os.path.exists(temp_image_path):
                        os.unlink(temp_image_path)

    except Exception as e:
        st.error(f"An error occurred while processing the image: {str(e)}")
else:
    st.info("Please upload a video or image to begin analysis.")

st.markdown("""
    <style>
    .stTextArea textarea {
        height: 100px;
    }
    </style>
    """, unsafe_allow_html=True)




# import streamlit as st
# from phi.agent import Agent
# from phi.model.google import Gemini
# from phi.tools.duckduckgo import DuckDuckGo
# from google.generativeai import upload_file, get_file
# import time
# from pathlib import Path
# import tempfile
# import os
# from PIL import Image

# st.set_page_config(
#     page_title="Multimodal AI Agent",
#     page_icon="🧬",
#     layout="wide"
# )

# st.title("Multimodal AI Agent 🧬")

# # Initialize single agent with both capabilities
# @st.cache_resource
# def initialize_agent():
#     return Agent(
#         name="Multimodal Analyst",
#         model=Gemini(id="gemini-2.0-flash-exp"),
#         tools=[DuckDuckGo()],
#         markdown=True,
#     )

# agent = initialize_agent()

# # File uploader for both video and image (including jfif)
# uploaded_video = st.file_uploader("Upload a video file", type=['mp4', 'mov', 'avi'])
# uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "jfif"])

# # Function to resize images using Pillow
# def resize_image(image_data, max_width=500, max_height=300):
#     image = Image.open(image_data)
#     image.thumbnail((max_width, max_height))  # Resize the image while maintaining aspect ratio
#     return image

# if uploaded_video:
#     with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
#         tmp_file.write(uploaded_video.read())
#         video_path = tmp_file.name
    
#     st.video(video_path)
    
#     user_prompt = st.text_area(
#         "What would you like to know about the video?",
#         placeholder="Ask any question related to the video - the AI Agent will analyze it and search the web if needed",
#         help="You can ask questions about the video content and get relevant information from the web"
#     )
    
#     if st.button("Analyze & Research Video"):
#         if not user_prompt:
#             st.warning("Please enter your question.")
#         else:
#             try:
#                 with st.spinner("Processing video and researching..."):
#                     video_file = upload_file(video_path)
#                     while video_file.state.name == "PROCESSING":
#                         time.sleep(2)
#                         video_file = get_file(video_file.name)

#                     prompt = f"""
#                     First analyze this video and then answer the following question using both 
#                     the video analysis and web research: {user_prompt}
                    
#                     Provide a comprehensive response focusing on practical, actionable information.
#                     """
                    
#                     result = agent.run(prompt, videos=[video_file])
                    
#                 st.subheader("Result")
#                 st.markdown(result.content)

#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")
#             finally:
#                 Path(video_path).unlink(missing_ok=True)

# elif uploaded_image:
#     try:
#         # Resize image before displaying and analyzing
#         image_data = uploaded_image
#         resized_image = resize_image(image_data)

#         # Display the resized image
#         st.image(resized_image, caption="Uploaded Image", use_container_width=True)

#         # Input for dynamic task
#         task_input = st.text_area(
#             "Enter your task/question for the AI Agent regarding the image:"
#         )

#         # Button to process the image and task
#         if st.button("Analyze Image") and task_input:
#             with st.spinner("AI is thinking... 🤖"):
#                 try:
#                     # Save the resized image in a temporary path (convert to RGB before saving)
#                     temp_image_path = tempfile.mktemp(suffix='.jpg')
#                     resized_image.save(temp_image_path)

#                     response = agent.run(task_input, images=[temp_image_path])

#                     # Display the response from the model
#                     st.markdown("### AI Response:")
#                     st.markdown(response.content)
#                 except Exception as e:
#                     st.error(f"An error occurred during analysis: {str(e)}")
#                 finally:
#                     # Clean up temp file
#                     if os.path.exists(temp_image_path):
#                         os.unlink(temp_image_path)

#     except Exception as e:
#         st.error(f"An error occurred while processing the image: {str(e)}")
# else:
#     st.info("Please upload a video or image to begin analysis.")

# st.markdown("""
#     <style>
#     .stTextArea textarea {
#         height: 100px;
#     }
#     </style>
#     """, unsafe_allow_html=True)




# import streamlit as st
# from phi.agent import Agent
# from phi.model.google import Gemini
# from phi.tools.duckduckgo import DuckDuckGo
# from google.generativeai import upload_file, get_file
# import time
# from pathlib import Path
# import tempfile
# import os
# from PIL import Image

# st.set_page_config(
#     page_title="Multimodal AI Agent",
#     page_icon="🧬",
#     layout="wide"
# )

# st.title("Multimodal AI Agent 🧬")

# # Initialize single agent with both capabilities
# @st.cache_resource
# def initialize_agent():
#     return Agent(
#         name="Multimodal Analyst",
#         model=Gemini(id="gemini-2.0-flash-exp"),
#         tools=[DuckDuckGo()],
#         markdown=True,
#     )

# agent = initialize_agent()

# # File uploader for both video and image
# uploaded_video = st.file_uploader("Upload a video file", type=['mp4', 'mov', 'avi'])
# uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# # Function to resize images using Pillow
# def resize_image(image_data, max_width=500, max_height=300):
#     image = Image.open(image_data)
#     image.thumbnail((max_width, max_height))  # Resize the image while maintaining aspect ratio
#     return image

# if uploaded_video:
#     with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
#         tmp_file.write(uploaded_video.read())
#         video_path = tmp_file.name
    
#     st.video(video_path)
    
#     user_prompt = st.text_area(
#         "What would you like to know about the video?",
#         placeholder="Ask any question related to the video - the AI Agent will analyze it and search the web if needed",
#         help="You can ask questions about the video content and get relevant information from the web"
#     )
    
#     if st.button("Analyze & Research Video"):
#         if not user_prompt:
#             st.warning("Please enter your question.")
#         else:
#             try:
#                 with st.spinner("Processing video and researching..."):
#                     video_file = upload_file(video_path)
#                     while video_file.state.name == "PROCESSING":
#                         time.sleep(2)
#                         video_file = get_file(video_file.name)

#                     prompt = f"""
#                     First analyze this video and then answer the following question using both 
#                     the video analysis and web research: {user_prompt}
                    
#                     Provide a comprehensive response focusing on practical, actionable information.
#                     """
                    
#                     result = agent.run(prompt, videos=[video_file])
                    
#                 st.subheader("Result")
#                 st.markdown(result.content)

#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")
#             finally:
#                 Path(video_path).unlink(missing_ok=True)

# elif uploaded_image:
#     try:
#         # Resize image before displaying and analyzing
#         image_data = uploaded_image
#         resized_image = resize_image(image_data)

#         # Display the resized image
#         st.image(resized_image, caption="Uploaded Image", use_container_width=True)

#         # Input for dynamic task
#         task_input = st.text_area(
#             "Enter your task/question for the AI Agent regarding the image:"
#         )

#         # Button to process the image and task
#         if st.button("Analyze Image") and task_input:
#             with st.spinner("AI is thinking... 🤖"):
#                 try:
#                     # Call the agent with the dynamic task and resized image
#                     temp_image_path = tempfile.mktemp(suffix='.jpg')
#                     resized_image.save(temp_image_path)

#                     response = agent.run(task_input, images=[temp_image_path])

#                     # Display the response from the model
#                     st.markdown("### AI Response:")
#                     st.markdown(response.content)
#                 except Exception as e:
#                     st.error(f"An error occurred during analysis: {str(e)}")
#                 finally:
#                     # Clean up temp file
#                     if os.path.exists(temp_image_path):
#                         os.unlink(temp_image_path)

#     except Exception as e:
#         st.error(f"An error occurred while processing the image: {str(e)}")
# else:
#     st.info("Please upload a video or image to begin analysis.")

# st.markdown("""
#     <style>
#     .stTextArea textarea {
#         height: 100px;
#     }
#     </style>
#     """, unsafe_allow_html=True)



# import streamlit as st
# from phi.agent import Agent
# from phi.model.google import Gemini
# from phi.tools.duckduckgo import DuckDuckGo
# from google.generativeai import upload_file, get_file
# import time
# from pathlib import Path
# import tempfile
# import os

# st.set_page_config(
#     page_title="Multimodal AI Agent",
#     page_icon="🧬",
#     layout="wide"
# )

# st.title("Multimodal AI Agent 🧬")

# # Initialize single agent with both capabilities
# @st.cache_resource
# def initialize_agent():
#     return Agent(
#         name="Multimodal Analyst",
#         model=Gemini(id="gemini-2.0-flash-exp"),
#         tools=[DuckDuckGo()],
#         markdown=True,
#     )

# agent = initialize_agent()

# # File uploader for both video and image
# uploaded_video = st.file_uploader("Upload a video file", type=['mp4', 'mov', 'avi'])
# uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# if uploaded_video:
#     with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
#         tmp_file.write(uploaded_video.read())
#         video_path = tmp_file.name
    
#     st.video(video_path)
    
#     user_prompt = st.text_area(
#         "What would you like to know about the video?",
#         placeholder="Ask any question related to the video - the AI Agent will analyze it and search the web if needed",
#         help="You can ask questions about the video content and get relevant information from the web"
#     )
    
#     if st.button("Analyze & Research Video"):
#         if not user_prompt:
#             st.warning("Please enter your question.")
#         else:
#             try:
#                 with st.spinner("Processing video and researching..."):
#                     video_file = upload_file(video_path)
#                     while video_file.state.name == "PROCESSING":
#                         time.sleep(2)
#                         video_file = get_file(video_file.name)

#                     prompt = f"""
#                     First analyze this video and then answer the following question using both 
#                     the video analysis and web research: {user_prompt}
                    
#                     Provide a comprehensive response focusing on practical, actionable information.
#                     """
                    
#                     result = agent.run(prompt, videos=[video_file])
                    
#                 st.subheader("Result")
#                 st.markdown(result.content)

#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")
#             finally:
#                 Path(video_path).unlink(missing_ok=True)

# elif uploaded_image:
#     try:
#         # Save uploaded image to a temporary file
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
#             tmp_file.write(uploaded_image.getvalue())
#             image_path = tmp_file.name

#         # Display the uploaded image
#         st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

#         # Input for dynamic task
#         task_input = st.text_area(
#             "Enter your task/question for the AI Agent regarding the image:"
#         )

#         # Button to process the image and task
#         if st.button("Analyze Image") and task_input:
#             with st.spinner("AI is thinking... 🤖"):
#                 try:
#                     # Call the agent with the dynamic task and image path
#                     response = agent.run(task_input, images=[image_path])

#                     # Display the response from the model
#                     st.markdown("### AI Response:")
#                     st.markdown(response.content)
#                 except Exception as e:
#                     st.error(f"An error occurred during analysis: {str(e)}")
#                 finally:
#                     # Clean up temp file
#                     if os.path.exists(image_path):
#                         os.unlink(image_path)

#     except Exception as e:
#         st.error(f"An error occurred while processing the image: {str(e)}")
# else:
#     st.info("Please upload a video or image to begin analysis.")

# st.markdown("""
#     <style>
#     .stTextArea textarea {
#         height: 100px;
#     }
#     </style>
#     """, unsafe_allow_html=True)





# import streamlit as st
# from phi.agent import Agent
# from phi.model.google import Gemini
# from phi.tools.duckduckgo import DuckDuckGo
# from google.generativeai import upload_file, get_file
# import time
# from pathlib import Path
# import tempfile

# st.set_page_config(
#     page_title="Multimodal AI Agent",
#     page_icon="🧬",
#     layout="wide"
# )

# st.title("Multimodal AI Agent 🧬")

# # Initialize single agent with both capabilities
# @st.cache_resource
# def initialize_agent():
#     return Agent(
#         name="Multimodal Analyst",
#         model=Gemini(id="gemini-2.0-flash-exp"),
#         tools=[DuckDuckGo()],
#         markdown=True,
#     )

# agent = initialize_agent()

# # File uploader
# uploaded_file = st.file_uploader("Upload a video file", type=['mp4', 'mov', 'avi'])

# if uploaded_file:
#     with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
#         tmp_file.write(uploaded_file.read())
#         video_path = tmp_file.name
    
#     st.video(video_path)
    
#     user_prompt = st.text_area(
#         "What would you like to know?",
#         placeholder="Ask any question related to the video - the AI Agent will analyze it and search the web if needed",
#         help="You can ask questions about the video content and get relevant information from the web"
#     )
    
#     if st.button("Analyze & Research"):
#         if not user_prompt:
#             st.warning("Please enter your question.")
#         else:
#             try:
#                 with st.spinner("Processing video and researching..."):
#                     video_file = upload_file(video_path)
#                     while video_file.state.name == "PROCESSING":
#                         time.sleep(2)
#                         video_file = get_file(video_file.name)

#                     prompt = f"""
#                     First analyze this video and then answer the following question using both 
#                     the video analysis and web research: {user_prompt}
                    
#                     Provide a comprehensive response focusing on practical, actionable information.
#                     """
                    
#                     result = agent.run(prompt, videos=[video_file])
                    
#                 st.subheader("Result")
#                 st.markdown(result.content)

#             except Exception as e:
#                 st.error(f"An error occurred: {str(e)}")
#             finally:
#                 Path(video_path).unlink(missing_ok=True)
# else:
#     st.info("Please upload a video to begin analysis.")

# st.markdown("""
#     <style>
#     .stTextArea textarea {
#         height: 100px;
#     }
#     </style>
#     """, unsafe_allow_html=True)