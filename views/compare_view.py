
import flet as ft

# handling translations
import utils 
translator = utils.translator["compare_view"]

def CompareView(router):
    
    def go_to(e: ft.ControlEvent):
        e.page.go("/1")

    row_user = ft.Column([
                    ft.TextField(label=translator["user_input"], icon=ft.icons.PERSON_ROUNDED),
                    ft.Text(
                        translator[f"user_text"],
                        theme_style = ft.TextThemeStyle.BODY_MEDIUM
                    ),
                    #ft.ElevatedButton(translator["button"], on_click=go_to)
                ],
                # Params for content column
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    row_ai = ft.Column([
                    ft.TextField(label=translator["user_input"], icon=ft.icons.COMPUTER, read_only=True),
                    ft.Text(
                        translator[f"user_text"],
                        theme_style = ft.TextThemeStyle.BODY_MEDIUM
                    ),
                    ft.ElevatedButton(translator["button"], on_click=go_to)
                ],
                # Params for content column
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    content = ft.Container(
        ft.Container(
            ft.Row([
                # User
                row_user,
                #AI
                row_ai
            ],
                # Params for content row
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        # Params for Main content container
        width= 900,
        height= 300,
        border_radius= 18,
        border= ft.border.all(1, "#44f4f4f4"),
        alignment=ft.alignment.center,
        blur= ft.Blur(10,12,ft.BlurTileMode.MIRROR),        
        ),
        margin=100,
        alignment=ft.alignment.center,
    )
    
    
    return content
