import flet as ft
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
            frame = cv2.resize(frame,(600,600))
            _, im_arr = cv2.imencode('.png', frame)
            self.im_b64 = base64.b64encode(im_arr)
            self.img.src_base64 = self.im_b64.decode("utf-8")
            self.update()

    def build(self):
        self.img = ft.Image(
            border_radius=ft.border_radius.all(20),
            #src="assets/error.svg"
        )
        content = ft.Column([
                    self.img,
                    ft.IconButton(
                        icon=ft.icons.CAMERA,
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
        
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path,file)
            
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"files removed ({file_path})")
    remove_photos()
    content = ft.Column([
                    Countdown(router=router)
                ],
                # Params for content column
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
    return content