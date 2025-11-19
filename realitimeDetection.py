# packages import
import torch
import uuid
import os
import cv2
import time
import numpy as np
import pydeck as pdk
from streamlit_folium import st_folium
import folium
import streamlit as st
from ultralytics import YOLO
from matplotlib import pyplot as plt

model = YOLO("yolov8n.pt")
model = YOLO("runs/classify/train3/weights/best.pt")


def Detect_RealTime():
    st_frame = st.empty()  # container for streaming frame

    if "run_detection" not in st.session_state:
        st.session_state.run_detection = False

    # start button
    if st.button("Start Real-Time Detection", key="start_btn"):
        st.session_state.run_detection = True

    # stop button
    if st.button("Stop Detection", key="Stop_btn"):
        st.session_state.run_detection = False

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Camera Failed to Open!!")
        return

    while st.session_state.run_detection:
        ret, frame = cap.read()
        if not ret:
            st.warning("No frame captured. Camera Off?")
            break

        results = model(frame)
        probs = results[0].probs.data.tolist() # probability array
        awake_prob = probs[0]
        drowsy_prob = probs[1]

        # checking if the drowsy is above 0.51%>
        threshold = 0.51
        is_drowsy_now = drowsy_prob >= threshold

        current_time = time.time()

        if is_drowsy_now:
            if st.session_state.drowsy_start_time is None:
                st.session_state.drowsy_start_time = current_time
            else:
                elapsed = current_time - st.session_state.drowsy_start_time

                if elapsed >= 10 and not st.session_state.drowsy_warning_triggered:
                    st.warning("Wake Up!!!!")
                    st.session_state.drowsy_warning_triggered = True

        annotated = results[0].plot()

        # Convert BGR to RGB for Streamlit
        rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

        st_frame.image(rgb, channels='RGB')

    cap.release()
