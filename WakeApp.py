import torch
import uuid
import os
import cv2
import time
import numpy as np
import streamlit as st
from ultralytics import YOLO
from matplotlib import pyplot as plt

# modification of streamlit page
st.set_page_config(page_title="Driving Monitor app", layout="wide", initial_sidebar_state="expanded")

CUSTOM_CSS = r"""
    <style>
:root[data-theme="light"] {
  --bg: #0f172a;
  --card: rgba(255,255,255,0.06);
  --text: #0b1220;
  --accent1: linear-gradient(90deg,#7c3aed, #06b6d4);
}
:root[data-theme="dark"] {
  --bg: #070812;
  --card: rgba(255,255,255,0.04);
  --text: #dbeafe;
  --accent1: linear-gradient(90deg,#06b6d4, #7c3aed);
}

/* Apply glass card effect to streamlit elements */
main .block-container {
  background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.00));
  padding: 1.6rem 2rem;
}
section[data-testid="stSidebar"] .css-1d391kg {
  background: transparent;
}
.css-1d391kg, .css-1d391kg .stButton button {
  border-radius: 14px;
}

/* Title style */
.header {
  display:flex; align-items:center; gap:12px;
}
.logo-circle {
  width:56px;height:56px;border-radius:12px;
  background: var(--accent1);
  display:flex;align-items:center;justify-content:center;color:white;font-weight:700;
  box-shadow: 0 8px 30px rgba(99,102,241,0.15);
}

/* Card style used in columns */
.card {
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border: 1px solid rgba(255,255,255,0.04);
  padding: 16px;
  border-radius: 12px;
}

/* small pills */
.pill {
  display:inline-block;padding:6px 10px;border-radius:999px;font-size:12px;background:rgba(255,255,255,0.03);
}

/* bot bubble */
.bot {
  background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  padding: 10px 12px;border-radius:12px;margin:6px 0;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
with st.sidebar:
    st.markdown(
        "<div style='display:flex;align-items:center;gap:10px'><div class='logo-circle'>WA</div><div><h3 style='margin:0'>WakeApp</h3><div style='font-size:12px;color:gray'>Opencv · YOLO · Torch</div></div></div>",
        unsafe_allow_html=True)
    st.markdown("-------")
    st.caption("Built w/ OpenCv + YOLO + Torch. prototype")

tabs = st.tabs(["Overview", "visual", "settings"])

with tabs[0]:
    st.markdown(
        """
            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:20px'>
            <div>
                <h1 style='margin:0;background:linear-gradient(90deg,#06b6d4,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
                    WakeApp
                </h1>
                <div style='color:gray;font-size:15px;'>AI-powered and monitoring  — checks if you are awake when driving</div>
            </div>
            </div>
            """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin-bottom:10px'></div>", unsafe_allow_html=True)

    c1 = st.columns(1)

    with c1:
        st.markdown(
            "<div class='card'><h4 style='margin:0'>Overview</h4>"
            "<div style='color:gray;margin-top:6px'>Quick glance at what users search for</div></div>",
            unsafe_allow_html=True
        )
