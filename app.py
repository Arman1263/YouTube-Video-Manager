import streamlit as st
from pymongo import MongoClient
from bson import ObjectId

# MongoDB Connection
client = MongoClient('mongodb+srv://arman:arman123@project.lsbywbi.mongodb.net/', tlsAllowInvalidCertificates=True)
db = client["ytmanager"]
video_collection = db["videos"]

# App Title
st.title("🎥 YouTube Video Manager")

# --- Add Video ---
st.subheader("➕ Add New Video")
with st.form("add_video_form"):
    new_name = st.text_input("Video Name")
    new_time = st.text_input("Video Time (e.g., 12:34)")
    add_btn = st.form_submit_button("Add Video")
    if add_btn:
        if new_name and new_time:
            video_collection.insert_one({"name": new_name, "time": new_time})
            st.success("Video added successfully!")
        else:
            st.error("Please provide both name and time.")

# --- View Videos (Controlled) ---
st.subheader("📄 View Saved Videos")
if st.button("📂 Show Videos"):
    videos = list(video_collection.find({}))
    if videos:
        for video in videos:
            st.write(f"**ID:** {video['_id']}")
            st.write(f"**Name:** {video['name']}")
            st.write(f"**Time:** {video['time']}")
            st.markdown("---")
    else:
        st.info("No videos found.")

# --- Update Video ---
st.subheader("✏️ Update Video")
with st.form("update_video_form"):
    video_id_update = st.text_input("Enter Video ID to Update")
    updated_name = st.text_input("New Video Name")
    updated_time = st.text_input("New Video Time")
    update_btn = st.form_submit_button("Update Video")
    if update_btn:
        try:
            result = video_collection.update_one(
                {"_id": ObjectId(video_id_update)},
                {"$set": {"name": updated_name, "time": updated_time}}
            )
            if result.modified_count:
                st.success("Video updated successfully.")
            else:
                st.warning("No video found or no changes made.")
        except Exception as e:
            st.error(f"Error: {e}")

# --- Delete Video ---
st.subheader("❌ Delete Video")
with st.form("delete_video_form"):
    video_id_delete = st.text_input("Enter Video ID to Delete")
    delete_btn = st.form_submit_button("Delete Video")
    if delete_btn:
        try:
            result = video_collection.delete_one({"_id": ObjectId(video_id_delete)})
            if result.deleted_count:
                st.success("Video deleted successfully.")
            else:
                st.warning("Video not found.")
        except Exception as e:
            st.error(f"Error: {e}")
