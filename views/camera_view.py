import flet as ft
# THIS PROJECT USE OPENCV THEN INSTALL OPENCV IN YOU PC
import cv2
import time
import os
import base64

cap = cv2.VideoCapture(0)

class Countdown(ft.UserControl):
    def __init__(self, router):
        super().__init__()
        self.router = router
        self.show = True

    def did_mount(self):
        self.update_timer()

    def save_image(self, e, *_):
        timestamp = str(int(time.time()))
        file_name = str("picture" + "_" + timestamp + '.jpg')
        path = f"assets/captured_images/{file_name}"
        # Decode base64
        decoded_img_data = base64.b64decode((self.im_b64))

        # Create image file from base64
        with open(path, 'wb') as img_file:
            img_file.write(decoded_img_data)
                
        self.router.set_data("img_org", path)
        self.router.image_manager.set_image(path)
        e.page.go("/compare")
        self.show = False
        

    def update_timer(self):
        while self.show:
            _, frame = cap.read()
            # frame = cv2.resize(frame,(400,400))
            _, im_arr = cv2.imencode('.png', frame)
            self.im_b64 = base64.b64encode(im_arr)
            self.img.src_base64 = self.im_b64.decode("utf-8")
            self.update()

    def build(self):
        self.img = ft.Image(
            border_radius=ft.border_radius.all(20)
        )
        content = ft.Column([
                    self.img,
                    ft.IconButton(
                        icon=ft.icons.PLAY_CIRCLE_FILL_OUTLINED,
                        on_click=self.save_image,
                        data=0,
                        icon_size=100,
                    )
        ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

        )
        return content

def height_changed(e):
    print(e.control.value)

def CameraView(router):
    def remove_photos():
        folder_path = "assets/captured_images/"
        # CHECK ALL FILE IN YOUPHOTO FOLDER
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path,file)
            # AND IF FOUND THEN REMOVE
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"YOU FILE SUUCESS REMOVE {file_path}")
    remove_photos()
    content = ft.Column([
                    Countdown(router=router)
                ],
                # Params for content column
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
    return content

# def CameraView(router):	
# 	# SHOW YOU FACE IMAGE WIDGET
#     image_placeholder = ft.Image(
# 		src=False,
# 		width=300,
# 		height=300,
# 		fit="cover"

# 		)

# 	# REMOVE ALL IMAGE IN YOUPHOTO FOLDER 
#     def remove_photos():
#         folder_path = "assets/captured_images/"
#         # CHECK ALL FILE IN YOUPHOTO FOLDER
#         files = os.listdir(folder_path)
#         for file in files:
#             file_path = os.path.join(folder_path,file)
#             # AND IF FOUND THEN REMOVE
#             if os.path.isfile(file_path):
#                 os.remove(file_path)
#                 print(f"YOU FILE SUUCESS REMOVE {file_path}")

            
#     def takemepicture(e):
#         remove_photos()
#         cap = cv2.VideoCapture(0)
#         cv2.namedWindow("Webcam",cv2.WINDOW_NORMAL)
#         # AND SET YOU WINDOW HEIGHT AND WIDTH WEBCAM
#         cv2.resizeWindow("Webcam",400,600)
#         timestamp = str(int(time.time()))
#         file_name = str("myCumFaceFile" + "_" + timestamp + '.jpg')

#         def save_image(event, *params):
#             if event == cv2.EVENT_LBUTTONDOWN:
#                 path = f"assets/captured_images/{file_name}"
#                 cv2.imwrite(path, frame)
#                 cv2.destroyAllWindows()
#                 router.set_data("img_org", path)
#                 router.image_manager.set_image(path)
#                 image_placeholder.src = path
#                 e.page.go("/compare")

#         cv2.setMouseCallback("Webcam", save_image)

#         # AND SAVE THE FILE NAME WITH TIME NOW 
        
#         try:
#             while True:
#                 ret, frame = cap.read()
#                 cv2.imshow("Webcam",frame)

#                 # AFTER THAT WAITING YOU INPUT FROM KEYBOARD
#                 key = cv2.waitKey(1)

#                 # # AND IF YOU PRESS Q FROM YOU KEYBOARD THEN
#                 # # THE WEBCAM WINDOW CAN CLOSE 
#                 # # AND YOU NOT CAPTURE YOU IMAGE
#                 if key == ord("q"):
#                     break
#                 elif key == 27:
#                     print("27!")
#                     break
#                 elif key == ord("s"):
#                     path = f"assets/captured_images/{file_name}"
#                     # AND IF YOU PRESS s FROM YOU KEYBOARD
#                     # THE THE YOU CAPTURE WILL SAVE IN FOLDER YOUPHOTO
#                     #path = f"assets/captured_images/{myfileface}"
#                     cv2.imwrite(path,frame)
#                     # AND SHOW TEXT YOU PICTURE SUCCESS INPUT
#                     # cv2.putText(frame,"YOU SUCESS CAPTURE GUYS !!!",(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
#                     # cv2.imshow("Webcam",frame)
#                     # cv2.waitKey(3000)
#                     # folder_path = "youphoto/"
#                     # myimage.src = folder_path + myfileface
#                     # break
#                     cap.release()
#                     cv2.destroyAllWindows()
#                     router.set_data("img_org", path)
#                     router.image_manager.set_image(path)
#                     image_placeholder.src = path
#                     e.page.go("/compare")

#             cap.release()
#             cv2.destroyAllWindows()

#         except Exception as e:
#             print(e)
#             print("YOU FAILED CHECK ERROR !!!!")

	
#     content = ft.Column([
# 	                ft.Text("Webcam Capture You FAce", size=30,weight="bold"),
# 	                ft.ElevatedButton(
# 						"Take My Face", 
# 						bgcolor="blue",
# 						color="white",
# 		                on_click=takemepicture
# 	                ),
# 	            image_placeholder 
# 	            ])
	
#     return content


# # AND PRESS s for capture
# # YOU FACEs