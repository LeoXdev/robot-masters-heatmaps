"""
detection.py

Purpose:
    Identify whether or not the host has a compatible GPU for use in training and prediction.

Usage:
    py detection.py
"""

import torch

# is preferable to make sure pytorch detects a gpu on the computer before training
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
