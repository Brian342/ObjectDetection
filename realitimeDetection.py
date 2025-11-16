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


def Detect_RealTime():
    st_frame = st.empty() # container for streaming frame

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Camera Failed to Open!!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("No frame captured. Camera Off?")
            break

        results = model(frame)
        annotated = results[0].plot()

        # Convert BGR to RGB for Streamlit
        rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

        st_frame.image(rgb, channels='RGB')

        # stop button inside ui
        if st.button("Stop"):
            break
    cap.release()

