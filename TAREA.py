import tkinter as tk
from tkinter import messagebox

class Deque:
    def __init__(self):
        self.items = []

    def add_front(self, item):
        self.items.insert(0, item)

    def add_rear(self, item):
        self.items.append(item)

    def remove_front(self):
        if self.is_empty():
            return None
        return self.items.pop(0)

    def remove_rear(self):
        if self.is_empty():
            return None
        return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def get_items(self):
        return self.items.copy()


class UndoRedoSystem:
    def __init__(self):
        self.history = Deque()
        self.redo_stack = Deque()
        self.current_state = []

    def add_action(self, action):

        if not action.strip():
            return "Error: acción vacía"

        self.history.add_rear(action)
        self.current_state.append(action)

        # Limpiar redo al agregar nueva acción
        self.redo_stack = Deque()

        return f"Acción agregada: {action}"

    def undo(self):

        if self.history.is_empty():
            return "No hay acciones para deshacer"

        action = self.history.remove_rear()

        self.redo_stack.add_rear(action)

        if self.current_state:
            self.current_state.pop()

        return f"Undo realizado: {action}"

    def redo(self):

        if self.redo_stack.is_empty():
            return "No hay acciones para rehacer"

        action = self.redo_stack.remove_rear()

        self.history.add_rear(action)

        self.current_state.append(action)

        return f"Redo realizado: {action}"

    def get_history(self):
        return self.history.get_items()

    def get_current_state(self):
        return self.current_state.copy()



class App:
    def __init__(self, root):

        self.system = UndoRedoSystem()

        self.root = root
        self.root.title("Sistema Undo / Redo")
        self.root.geometry("600x500")
        self.root.config(bg="#f0f0f0")

        title = tk.Label(
            root,
            text="Sistema de Edición Undo / Redo",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0"
        )
        title.pack(pady=10)

        self.entry = tk.Entry(root, width=40, font=("Arial", 12))
        self.entry.pack(pady=10)

        btn_frame = tk.Frame(root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        add_btn = tk.Button(
            btn_frame,
            text="Agregar Acción",
            width=18,
            command=self.add_action,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold")
        )
        add_btn.grid(row=0, column=0, padx=5)

        undo_btn = tk.Button(
            btn_frame,
            text="Undo",
            width=12,
            command=self.undo_action,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold")
        )
        undo_btn.grid(row=0, column=1, padx=5)

        redo_btn = tk.Button(
            btn_frame,
            text="Redo",
            width=12,
            command=self.redo_action,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold")
        )
        redo_btn.grid(row=0, column=2, padx=5)

        self.display = tk.Text(
            root,
            width=70,
            height=20,
            font=("Consolas", 11)
        )
        self.display.pack(pady=10)

        self.update_display()

    def add_action(self):

        action = self.entry.get()

        result = self.system.add_action(action)

        messagebox.showinfo("Resultado", result)

        self.entry.delete(0, tk.END)

        self.update_display()

    def undo_action(self):

        result = self.system.undo()

        messagebox.showinfo("Undo", result)

        self.update_display()

    def redo_action(self):

        result = self.system.redo()

        messagebox.showinfo("Redo", result)

        self.update_display()

    def update_display(self):

        self.display.delete(1.0, tk.END)

        self.display.insert(tk.END, "===== HISTORIAL =====\n\n")

        history = self.system.get_history()

        if history:
            for i, action in enumerate(history, start=1):
                self.display.insert(
                    tk.END,
                    f"{i}. {action}\n"
                )
        else:
            self.display.insert(
                tk.END,
                "No hay acciones registradas\n"
            )

        self.display.insert(tk.END, "\n")

        self.display.insert(
            tk.END,
            "===== ESTADO ACTUAL =====\n\n"
        )

        current = self.system.get_current_state()

        if current:
            for i, action in enumerate(current, start=1):
                self.display.insert(
                    tk.END,
                    f"{i}. {action}\n"
                )
        else:
            self.display.insert(
                tk.END,
                "Estado vacío\n"
            )


def run_tests():

    system = UndoRedoSystem()

    system.add_action("Escribir Hola")
    system.add_action("Borrar línea")

    assert system.get_history() == [
        "Escribir Hola",
        "Borrar línea"
    ]

    system.undo()

    assert system.get_history() == [
        "Escribir Hola"
    ]

    system.redo()

    assert system.get_history() == [
        "Escribir Hola",
        "Borrar línea"
    ]

    system.undo()
    system.undo()

    result = system.undo()

    assert result == "No hay acciones para deshacer"

    print("Todas las pruebas pasaron correctamente")



if __name__ == "__main__":

    # Ejecutar pruebas
    run_tests()

    # Ejecutar interfaz
    root = tk.Tk()
    app = App(root)
    root.mainloop()