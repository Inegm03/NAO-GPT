from naoqi import ALProxy
import time
import sys
import subprocess

# Robot's IP address and port
NAO_IP = "10.1.95.3"  # Unified IP address
NAO_PORT = 9559

# Connect to the robot's modules
try:
    faceProxy = ALProxy("ALFaceDetection", NAO_IP, NAO_PORT)
    memoryProxy = ALProxy("ALMemory", NAO_IP, NAO_PORT)
    motionProxy = ALProxy("ALMotion", NAO_IP, NAO_PORT)
    ttsProxy = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
    posture = ALProxy("ALRobotPosture", NAO_IP, NAO_PORT)
except Exception as e:
    print("Could not create proxy to ALFaceDetection, ALMemory, ALMotion, or ALTextToSpeech")
    print("Error was: ", e)
    exit(1)

# Subscribe to the Face Detected event
faceProxy.subscribe("FaceDetector")

# Set stiffness on for Head motors
motionProxy.setStiffnesses("Head", 1.0)

print("Starting face detection")

try:
    moveLeft = True
    while True:
        # Move head to scan for faces
        if moveLeft:
            motionProxy.setAngles("HeadYaw", -1.0, 0.1)  # Move head left
        else:
            motionProxy.setAngles("HeadYaw", 1.0, 0.1)  # Move head right
        moveLeft = not moveLeft
        time.sleep(3)  # Adjust as needed for the speed of head movement

        # Check if a face is detected
        faceDetected = memoryProxy.getData("FaceDetected")

        if faceDetected and faceDetected[1]:
            # Stop head movement
            motionProxy.setAngles("HeadYaw", 0, 0.1)
            motionProxy.setAngles("HeadPitch", 0, 0.1)

            # Robot speaks
            ttsProxy.say("Hello, my name is NAO")
            
            posture.goToPosture("Stand", 0.75)
            motionProxy.setAngles("RShoulderPitch", -1.0, 0.2)
            motionProxy.setAngles("RShoulderRoll", 0.2, 0.2)
            motionProxy.setAngles("RElbowRoll", 0.5, 0.2)
            motionProxy.setAngles("RElbowYaw", 1.5, 0.2)
            time.sleep(1)

            # Wave a few times
            motionProxy.openHand("RHand")
            for _ in range(3):
                motionProxy.setAngles("RElbowYaw", 1.0, 0.2)
                time.sleep(0.5)
                motionProxy.setAngles("RElbowYaw", 1.5, 0.2)
                time.sleep(0.5)

            # Lower the arm
            motionProxy.setAngles("RShoulderPitch", 1.5, 0.2)
            motionProxy.setAngles("RShoulderRoll", 0.0, 0.2)
            motionProxy.setAngles("RElbowRoll", 0.0, 0.2)
            motionProxy.setAngles("RElbowYaw", 0.0, 0.2)

            # Process audio to text
            # Assuming convert_audio_to_text function and local_path variable are defined elsewhere
            transcription = convert_audio_to_text(local_path)
            text1 = transcription

            file_path1 = "text1.txt"
            with open(file_path1, "w") as file:
                file.write(text1)

            run = ['python3', 'testapi.py']
            subprocess.call(run)

            file_path2 = "text2.txt"
            with open(file_path2, "r") as file:
                res = file.read()

            ttsProxy.say(res)
            time.sleep(2)
            ttsProxy.say("Nice conversation with you")

            # Stop the loop after greeting and processing
            break
        else:
            print("No face detected")

except KeyboardInterrupt:
    print("Interrupted by user, stopping face detection")
    faceProxy.unsubscribe("FaceDetector")
    motionProxy.setAngles("HeadYaw", 0, 0.1)
    motionProxy.setAngles("HeadPitch", 0, 0.1)
    motionProxy.setStiffnesses("Head",0.0)
