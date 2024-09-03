from tksheet import Sheet
import tkinter as tk
import matplotlib.pyplot as plt

class Demo(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.sheet = Sheet(self.frame,
                           data=[[f"" for c in range(10)] for r in range(10)])
        self.sheet.enable_bindings()
        self.frame.grid(row=0, column=0, sticky="nswe")
        self.sheet.grid(row=0, column=0, sticky="nswe")

        self.sheet.set_options(table_bg="#34353d")

        # Add a button to trigger plotting
        self.plot_button = tk.Button(self, text="Plotar Selecionados", command=self.plot_selected)
        self.plot_button.grid(row=1, column=0, sticky="ew")

    def plot_selected(self):
        # Get selected cells
        selected_cells = self.sheet.get_selected_cells(sort_by_row=True)
        if not selected_cells:
            return  # No selection, do nothing

        # Get data from selected cells
        x_values = []
        y_values = []
        legendas = []
        for col, row in selected_cells:
            print(row, col)
            if row == 0:  # First row as legend
                legendas.append(self.sheet.get_cell_data(row, col))
            else:
                x_valor = self.sheet.get_cell_data(row, 0)
                y_valor = self.sheet.get_cell_data(row, col)
                if x_valor != "" and y_valor != "":
                    x_values.append(float(x_valor.replace(',', '.')))  # Convert to float
                    y_values.append(float(y_valor.replace(',', '.')))  # Convert to float

        # Plot values using matplotlib
        if len(x_values) > 0 and len(y_values) > 0:
            plt.scatter(x_values, y_values)#, label=legendas[0])  # Plot x_values with y_values
            # plt.xticks(x_values, rotation=45)  # Rotate X axis labels
            # plt.yticks(y_values)  # Add Y axis labels
            plt.xlabel("Eixo X")
            plt.ylabel("Eixo Y")
            plt.title("Valores Selecionados")
            plt.legend()  # Add legend with Y axis names
            plt.show()
        else:
            print("Selecione células válidas para plotar")

app = Demo()
app.mainloop()