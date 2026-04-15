import flet as ft
from database import supabase, encrypt_password, decrypt_password


def build_ui(page: ft.Page):
    page.title = "SafePass"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.SYSTEM

    def show_message(message, color=ft.Colors.BLUE):
        snack = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color,
            action="OK"
        )
        page.overlay.clear()
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def open_main_screen(e=None):
        page.clean()

        input_email = ft.TextField(
            label="Email",
            width=300,
            suffix=ft.Text("@gmail.com"),
            prefix_icon=ft.Icons.EMAIL
        )

        text_password = ft.Text(size=20, color=ft.Colors.GREEN)

        def search_password(e):
            email = input_email.value.strip()

            if not email:
                show_message("Type your email", ft.Colors.RED)
                return

            full_email = email + "@gmail.com"

            res = supabase.table("emails").select("*").eq("email", full_email).execute()

            if res.data:
                encrypted_password = res.data[0]["password"]
                password = decrypt_password(encrypted_password)

                text_password.value = f"Password: {password}"
            else:
                text_password.value = ""
                show_message("Email not found", ft.Colors.RED)

            page.update()

        page.add(
            ft.Column(
                [
                    ft.Text("SafePass", size=35, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    input_email,
                    text_password,
                    ft.ElevatedButton(
                        "Search Password",
                        width=250,
                        on_click=search_password,
                        icon=ft.Icons.SEARCH
                    ),
                    ft.Row(
                        [
                            ft.TextButton(
                                "Add Email?",
                                on_click=open_register_screen,
                                icon=ft.Icons.ADD
                            ),
                            ft.TextButton(
                                "Remove Email?",
                                on_click=open_remove_screen,
                                icon=ft.Icons.DELETE
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    def open_register_screen(e=None):
        page.clean()

        in_mail = ft.TextField(
            label="New Email",
            width=300,
            suffix=ft.Text("@gmail.com")
        )

        in_pass = ft.TextField(
            label="Password",
            width=300,
            password=True,
            can_reveal_password=True
        )

        in_conf = ft.TextField(
            label="Confirm Password",
            width=300,
            password=True,
            can_reveal_password=True
        )

        def register(e):
            email = in_mail.value.strip()
            pwd = in_pass.value
            cpwd = in_conf.value

            if not email or not pwd or not cpwd:
                show_message("Fill in all fields", ft.Colors.RED)
                return

            if pwd != cpwd:
                show_message("Passwords are different", ft.Colors.RED)
                return

            full_mail = email + "@gmail.com"

            check = supabase.table("emails").select("*").eq("email", full_mail).execute()

            if check.data:
                show_message("Email already registered", ft.Colors.RED)
                return

            encrypted_pwd = encrypt_password(pwd)

            supabase.table("emails").insert({
                "email": full_mail,
                "password": encrypted_pwd
            }).execute()

            show_message("Registered successfully", ft.Colors.GREEN)
            open_main_screen()

        page.add(
            ft.Column(
                [
                    ft.Text("Register", size=35),
                    in_mail,
                    in_pass,
                    in_conf,
                    ft.ElevatedButton(
                        "Register",
                        width=250,
                        on_click=register
                    ),
                    ft.TextButton("Back", on_click=open_main_screen),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    def open_remove_screen(e=None):
        page.clean()

        in_rem = ft.TextField(
            label="Email to Remove",
            width=300,
            suffix=ft.Text("@gmail.com")
        )

        in_rem_c = ft.TextField(
            label="Confirm Email",
            width=300,
            suffix=ft.Text("@gmail.com")
        )
        def open_remove_screen(e=None):
            page.clean()

            in_rem = ft.TextField(
            label="Email to Remove",
            width=300,
            suffix=ft.Text("@gmail.com")
        )

        in_rem_c = ft.TextField(
            label="Confirm Email",
            width=300,
            suffix=ft.Text("@gmail.com")
        )

        def confirm_delete(e):
            email1 = in_rem.value.strip()
            email2 = in_rem_c.value.strip()

            if not email1 or not email2:
                show_message("Fill in all fields", ft.Colors.RED)
                return

            if email1 != email2:
                show_message("Emails don't match", ft.Colors.RED)
                return

            full_mail = email1 + "@gmail.com"

            check = supabase.table("emails").select("email").eq("email", full_mail).execute()

            if not check.data:
                show_message("Email not found in database", ft.Colors.RED)
                return

            supabase.table("emails").delete().eq("email", full_mail).execute()

            show_message("Removed successfully!", ft.Colors.GREEN)
            open_main_screen()

        page.add(
            ft.Column(
                [
                    ft.Text("Remove Email", size=35),
                    in_rem,
                    in_rem_c,
                    ft.ElevatedButton(
                        "Remove",
                        width=250,
                        on_click=confirm_delete
                    ),
                    ft.TextButton(
                        "Back",
                        on_click=open_main_screen
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    open_main_screen()