import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO
    input_marca = ft.TextField(value='', label="Marca")
    input_modello = ft.TextField(value='', label="Modello")
    input_anno = ft.TextField(value='', label="Anno")
    txt_posti = ft.TextField(width=100, disabled=True, value="4", text_align=ft.TextAlign.CENTER)   # inserisco 4 come valore standard

    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO
    def handleAdd(e):
        currentVal = int(txt_posti.value)
        txt_posti.value = str(currentVal + 1)
        txt_posti.update()

    def handleRemove(e):
        currentVal = int(txt_posti.value)
        txt_posti.value = str(currentVal - 1)
        txt_posti.update()

    def handle_aggiungi_auto(e):
        try:
            anno = int(input_anno.value)
            posti = int(txt_posti.value)
            autonoleggio.aggiungi_automobile(input_marca.value, input_modello.value, anno, posti)
            input_marca.value = ''
            input_modello.value = ''
            input_anno.value = ''
            txt_posti.value = '4'

            aggiorna_lista_auto()

            input_marca.update()
            input_modello.update()
            input_anno.update()
            txt_posti.update()

        except ValueError:
            alert.show_alert("Errore: Anno e Posti devono essere valori numerici.")
            return

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO

    btn_remove_posti = ft.IconButton(icon=ft.Icons.REMOVE, icon_color="red", icon_size=24, on_click=handleRemove)
    btn_add_posti = ft.IconButton(icon=ft.Icons.ADD, icon_color="green", icon_size=24, on_click=handleAdd)
    btn_aggiungi_auto = ft.ElevatedButton(text='Aggiungi automobile', on_click=handle_aggiungi_auto)
    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO

        # Sezione 3
        ft.Divider(),
        ft.Text("Aggiungi Nuova Automobile", size=20),
        ft.Row(
            [input_marca, input_modello, input_anno],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        ),
        ft.Row(
            [ft.Text("Posti:", size=16), btn_remove_posti, txt_posti, btn_add_posti],
            alignment=ft.MainAxisAlignment.CENTER),

        btn_aggiungi_auto,
        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
