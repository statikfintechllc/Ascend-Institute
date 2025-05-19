import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def glowing_golden_eye():
    return html.Div(
        id="golden-eye-container",
        children=[
            html.Div(
                "",
                id="golden-eye",
                style={
                    "width": "75px",
                    "height": "75px",
                    "border-radius": "50%",
                    "background": "radial-gradient(circle, gold, orange, darkgoldenrod)",
                    "box-shadow": "0px 0px 20px 5px rgba(255, 215, 0, 0.8)",
                    "text-align": "center",
                    "font-size": "40px",
                    "line-height": "75px",
                    "cursor": "grab",
                    "position": "absolute",
                    "top": "50px",
                    "left": "50px",
                },
            )
        ],
    )


if __name__ == "__main__":
    glowing_golden_eye()
