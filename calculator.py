#mPythonType:0
#mPythonType:0
#mPythonType:0
#mPythonType:0
#mPythonType:0
import sys, io

# Force stdout/stderr to UTF-8, even on Windows Big5/CP950 locale
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# server.py
from mcp.server.fastmcp import FastMCP
import sys
import logging
from googleapiclient.discovery import build
import webbrowser

logger = logging.getLogger('Calculator')

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

import math
import random
from googlesearch import search
import subprocess

# Create an MCP server
mcp = FastMCP("MyMCPServer")

# Add an addition tool
@mcp.tool()
def calculator(python_expression: str) -> dict:
    """For mathamatical calculation, always use this tool to calculate the result of a python expression. You can use 'math' or 'random' directly, without 'import'."""
    result = eval(python_expression, {"math": math, "random": random})
    logger.info(f"Calculating formula: {python_expression}, result: {result}")
    return {"success": True, "result": result}


# Google Search
@mcp.tool()
def google_search(query: str, num_results: int = 5) -> dict:
    """
    Search Google for the given query and return the top results.
    """
    try:
        logger.info(f"Searching Google for: {query}")
        results = list(search(query, num_results=num_results))
        return {
            "success": True,
            "query": query,
            "results": results
        }
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }
    


# YouTubeSearch
API_KEY = "AIzaSyAi70p-iP6isgbPcoBoXBepUraU7-xZ2yw"

@mcp.tool()
def youtube_search_play(query: str) -> dict:
    """
    Search YouTube for a keyword and play the first result in the browser.
    """
    try:
        youtube = build("youtube", "v3", developerKey=API_KEY, cache_discovery=False)
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=1
        )
        response = request.execute()

        if "items" in response and len(response["items"]) > 0:
            video_id = response["items"][0]["id"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            # subprocess.Popen(["mpv", "--no-video", video_url])
            subprocess.Popen([r"C:\Users\user\Downloads\mpv-x86_64-20250811-git-01b7edc\mpv.exe", video_url])

            logger.info(f"Playing video: {video_url}")
            return {

                "success": True,
                "video_url": video_url
            }
        else:
            return {
                "success": False,
                "error": "No videos found."
            }
    except Exception as e:
        logger.error(f"Search/play failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }


import time
import threading

# Timing
# Global variable to keep track of alarm time
alarm_end_time = None
alarm_thread = None
import threading, time
from mcp.server.fastmcp import FastMCP

# 全域變數
alarm_end_time = None
alarm_thread = None
def alarm_countdown(duration_sec):
    global alarm_end_time
    alarm_end_time = time.time() + duration_sec
    while True:
        remaining = alarm_end_time - time.time()
        if remaining < 0:
            alarm_end_time = None  # 設定鬧鐘結束
            break
        time.sleep(1)
@mcp.tool()
def set_alarm(time_limit: int) -> dict:
    global alarm_thread

    if alarm_thread and alarm_thread.is_alive():
        return {"success": False, "message": "已有鬧鐘正在運行"}

    alarm_thread = threading.Thread(target=alarm_countdown, args=(time_limit,))
    alarm_thread.daemon = True
    alarm_thread.start()

    return {"success": True, "message": f"鬧鐘設定成功，{time_limit}秒後響鈴。"}

@mcp.tool()
def get_alarm_status() -> dict:
    """
    讓 AI 小智定期查詢剩餘時間
    """
    global alarm_end_time
    if not alarm_end_time:
        return {"active": False, "remaining": 0, "message": "鬧鐘未設定或已響"}
    remaining = int(alarm_end_time - time.time())
    if remaining <= 0:
        return {"active": False, "remaining": 0, "message": "鬧鐘響了！⏰"}
    return {"active": True, "remaining": remaining}


# WebCam take photos
import cv2
from mcp.server.fastmcp import FastMCP
@mcp.tool()
def webcam_take_photo() -> dict:
    """啟用 USB 攝影機（開始錄影或拍照）"""
    try:
        cap = cv2.VideoCapture("http://192.168.0.160:8080/video")
        #cap = cv2.VideoCapture(0)  # 0 = default webcam
        if not cap.isOpened():
            return {"success": False, "error": "無法開啟攝影機"}    
        # 你可以立即拍一張照片測試
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("test.jpg", frame)  # 存一張照片測試
        cap.release()
        return {"success": True, "message": "攝影機已啟用"}
    except Exception as e:
        return {"success": False, "error": str(e)}




# Webcam + Object Detection
import cv2
import numpy as np
from mcp.server.fastmcp import FastMCP
# Pre-trained model files (download beforehand)
PROTO_TXT = "MobileNetSSD_deploy.prototxt"
MODEL_FILE = "MobileNetSSD_deploy.caffemodel"
# Class labels (20 classes + background)
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant",
           "sheep", "sofa", "train", "tvmonitor","TV","Computer","book","Raspberry Pi"]

# Load pre-trained network
net = cv2.dnn.readNetFromCaffe(PROTO_TXT, MODEL_FILE)
@mcp.tool()
def webcam_detect_objects() -> dict:
    """使用 USB 攝影機進行物件偵測 (大約 20 種常見物件)"""
    try:
        cap = cv2.VideoCapture("http://192.168.0.160:8080/video")


        if not cap.isOpened():
            return {"success": False, "error": "無法開啟攝影機"}

        ret, frame = cap.read()
        cap.release()

        if not ret:
            return {"success": False, "error": "無法讀取影像"}

        # Prepare frame for detection
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                     0.007843, (300, 300), 127.5)

        net.setInput(blob)
        detections = net.forward()

        results = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.4:  # threshold
                idx = int(detections[0, 0, i, 1])
                label = CLASSES[idx] if idx < len(CLASSES) else "unknown"
                results.append({"label": label, "confidence": float(confidence)})

                # Draw bounding box
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              (0, 255, 0), 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, f"{label}: {confidence:.2f}",
                            (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 0), 2)

        # Save detection result image
        cv2.imwrite("detection_result.jpg", frame)

        return {"success": True, "message": "物件偵測完成",
                "results": results, "output_image": "detection_result.jpg"}

    except Exception as e:
        return {"success": False, "error": str(e)}
import requests
import logging
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger("TVControl")

HOME_ASSISTANT_URL = ""
TOKEN = ""
TV_ENTITY_ID = ""

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def check_ha_api():
    """Check if Home Assistant API is reachable."""
    try:
        r = requests.get(f"{HOME_ASSISTANT_URL}/api/", headers=HEADERS, timeout=5)
        if r.status_code == 200:
            return True, "Home Assistant API reachable"
        else:
            return False, f"HA API returned {r.status_code}: {r.text}"
    except Exception as e:
        return False, str(e)

def check_tv_entity():
    """Check if TV entity exists and is available."""
    try:
        r = requests.get(f"{HOME_ASSISTANT_URL}/api/states/{TV_ENTITY_ID}", headers=HEADERS, timeout=5)
        if r.status_code == 200:
            state = r.json()
            return True, state.get("state", "unknown")
        else:
            return False, f"Entity check returned {r.status_code}: {r.text}"
    except Exception as e:
        return False, str(e)

@mcp.tool()
def tv_control(action: str, query: str = None) -> dict:
    try:
        # Step 1: Check HA API
        api_ok, api_msg = check_ha_api()
        if not api_ok:
            return {"success": False, "error": f"Cannot reach Home Assistant: {api_msg}"}

        # Step 2: Check TV entity
        entity_ok, tv_state = check_tv_entity()
        if not entity_ok:
            return {"success": False, "error": f"TV entity not found or unavailable: {tv_state}"}

        # Step 3: Perform action
        if action.lower() == "on":
            url = f"{HOME_ASSISTANT_URL}/api/services/media_player/turn_on"
            payload = {"entity_id": TV_ENTITY_ID}
            r = requests.post(url, json=payload, headers=HEADERS, timeout=5)
            if r.status_code == 200:
                return {"success": True, "message": "TV turned ON successfully"}
            else:
                return {"success": False, "error": r.text}

        elif action.lower() == "off":
            url = f"{HOME_ASSISTANT_URL}/api/services/media_player/turn_off"
            payload = {"entity_id": TV_ENTITY_ID}
            r = requests.post(url, json=payload, headers=HEADERS, timeout=5)
            if r.status_code == 200:
                return {"success": True, "message": "TV turned OFF successfully"}
            else:
                return {"success": False, "error": r.text}

        else:
            return {"success": False, "error": "Invalid action. Use 'on' or 'off'."}

    except Exception as e:
        return {"success": False, "error": str(e)}



# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
