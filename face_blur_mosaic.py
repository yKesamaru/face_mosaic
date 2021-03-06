import cv2
import face_recognition
import PySimpleGUI as sg

def mosaic(src, ratio):
    small = cv2.resize(src, None, fx=ratio, fy=ratio,
                       interpolation=cv2.INTER_NEAREST)
    return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

# もし写真にぼかし処理を行いたい場合、コメントアウトを解除する ----------------------
# image = cv2.imread('img/people.jpg')
# face_location_list = face_recognition.face_locations(image, 2, 'cnn')
# if len(face_location_list) > 0:
#     dst = image.copy()
#     for (top, right, bottom, left) in face_location_list:
#         dst[top:top + (bottom - top), left:left + (right - left)] = mosaic(
#             dst[top:top + (bottom - top), left:left + (right - left)], 0.2)
#     try:
#         cv2.imwrite('img/mosaic.jpg', dst)
#     except:
#         print('cant write image')
# else:
#     print('no face')
# -----------------------------------------------------------------------------------

vcap = cv2.VideoCapture('img/video.mp4', cv2.CAP_FFMPEG)

sg.theme('Reddit')
layout = [
    [sg.Text('blur')],
    [sg.Image(key='display')],
    [sg.Button('terminate', key='terminate', button_color='red')]
]
window = sg.Window('blur', layout, location=(50, 50), disable_close=True)

while True:
    ret, frame = vcap.read()
    if ret == False:
        break
    face_location_list = face_recognition.face_locations(
        frame, 0, 'cnn')

    if len(face_location_list) > 0:
        dst = frame.copy()
        for (top, right, bottom, left) in face_location_list:
            # rectangle blur ======
            # dst[top:top + (bottom - top), left:left + (right - left)] = cv2.blur(
            #     dst[top:top + (bottom - top), left:left + (right - left)], (50, 50))
            # mosaic blur =========
            dst[top:top + (bottom - top), left:left + (right - left)] = mosaic(
                dst[top:top + (bottom - top), left:left + (right - left)], 0.1)

    event, _ = window.read(timeout=1)
    imgbytes = cv2.imencode(".png", dst)[1].tobytes()
    window["display"].update(data=imgbytes)
    if event == 'terminate':
        break
vcap.release()
