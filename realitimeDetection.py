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
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    while cap.isOpened():
        ret, frame = cap.read()

        # make detection
        results = model(frame)

        annotated_frame = results[0].plot()
        frame_resized = cv2.resize(annotated_frame, (960, 540))  # (width, height)
        cv2.imshow("Awake/Drowsy", frame_resized)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
