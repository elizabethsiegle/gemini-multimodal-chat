import os

import google.generativeai as genai
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from st_multimodal_chatinput import multimodal_chatinput

st.title("Chat w/ Gemini")
st.image("gemini.jpeg")

GOOGLE_API_KEY=os.environ['GOOGLE_API_KEY']

genai.configure(api_key=GOOGLE_API_KEY)

# Create the Model
model = genai.GenerativeModel('gemini-pro')
llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")
# vision_model = genai.GenerativeModel('gemini-pro-vision')

# call llm: query and resp
def call_txt_llm(q):
    resp = model.generate_content(q)
    # display Assistant msg
    with st.chat_message("assistant", avatar="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGVfLdUg7kVxuSqqBGgAL3UJeQgRCLPhxIZlXbVxmUAdYaJm-fcUal7x-FHhwxzpeg6_M&usqp=CAU"):
      st.markdown(resp.text)
      
      # store User msg
      st.session_state.messages.append(
        {
            "role":"user",
            "content": q
        }
      )

      # store User msg
      st.session_state.messages.append(
        {
            "role":"assistant",
            "content": resp.text
        }
      )


def call_vis_llm(q):
  chatinput = multimodal_chatinput()
  uploaded_images = chatinput["uploadedImages"] # list of base64 encodings of uploaded images
  txt_inp_with_pic = chatinput["textInput"] # submitted text
  resp = txt_inp_with_pic + str(uploaded_images)
  # display Assistant msg
  with st.chat_message("assistant", avatar="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGVfLdUg7kVxuSqqBGgAL3UJeQgRCLPhxIZlXbVxmUAdYaJm-fcUal7x-FHhwxzpeg6_M&usqp=CAU"):
          st.markdown(resp.text)
          # store User msg
          st.session_state.messages.append(
          {
              "role":"user",
              "content": q
          }
          )

          # store User msg
          st.session_state.messages.append(
          {
              "role":"assistant",
              "content": resp.text
          }
        )
  message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": txt_inp_with_pic,
        },
        {
            "type": "image_url",
            "image_url": uploaded_images[0]
        },
    ]
  )
  response = llm.invoke(message)
  print(response.content)
  
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"assistant",
            "content":"Ask Gemini anything or get a detailed story about an input image!"
        }
    ]
  
# Display msgs from history upon rerun
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# get user input
q = st.chat_input("What would you like to know || what image would you like a detailed story about?")

# call func when user input is true
if q:
    # Displaying the User Message
    with st.chat_message("user", avatar= "https://d112y698adiu2z.cloudfront.net/photos/production/user_photos/000/517/300/datas/profile.png"):
        st.markdown(q)
    # check if input is image
    if type(q) == str:
      call_txt_llm(q)
    else:
      call_vis_llm(q)
    


# could do st.write, use st.markdown for styling
# st.markdown(
#     """
#     <div>
#     <p style="text-align: center;font-family:Arial; color:Pink; font-size: 12px;display: table-cell; vertical-align: bottom">Made with ❤️ in SF. ✅ out <a href="https://replit.com/@LizzieSiegle/gemini-play">the repl!</a></p>
#     </div>
#     """,
#     unsafe_allow_html=True, # HTML tags found in body escaped -> treated as pure text
# )