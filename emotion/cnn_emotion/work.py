import sys
import cv2
import os
import torch
from torchvision.transforms.functional import to_pil_image
from cnn_emotion.utils import image_to_tensor
# from cnn_emotion.web_crawling import find_music


def predict_emotion(frame, net, emotion_model):
    # if result:
    #     del result

    num2class = {
        0: 'angry',
        1: 'disgust',
        2: 'fear',
        3: 'happy',
        4: 'neutral',
        5: 'sad',
        6: 'surprise',
    }

    blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123))
    net.setInput(blob)
    out = net.forward()

    detect = out[0, 0, :, :]
    (h, w) = frame.shape[:2]

    for i in range(detect.shape[0]):
        confidence = detect[i, 2]
        if confidence < 0.5:
            break

        x1 = int(detect[i, 3] * w)
        y1 = int(detect[i, 4] * h)
        x2 = int(detect[i, 5] * w)
        y2 = int(detect[i, 6] * h)
        # print(x1, y1, x2, y2)

        img = frame[y1:y2, x1:x2, :]
        img = image_to_tensor(to_pil_image(img))
        img = torch.unsqueeze(img, 0)
        output = emotion_model(img)
        _, pred = torch.max(output, 1)
        global result
        result = num2class[pred[0].item()]

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0))

        label = f'Emotion: {result}'
        cv2.putText(frame, label, (x1, y1 - 1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
    return frame, result


# cap.release()
# cv2.destroyAllWindows()
# print(f'감정: {result}')
# music = find_music(result)
# print(music)
