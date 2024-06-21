import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = "Datos-Competencia-Factify.xlsx"
df = pd.read_excel(file_path)

# Extracting the data from the dataframe
periodicos = df["Periódico"].tolist()
suscriptores = df["Número de suscriptores 2024"].tolist()
precio = df["Precio de la suscripción mensual 2024"].tolist()

# Crear el scatter plot
plt.figure(figsize=(10, 6))
for i, periodico in enumerate(periodicos):
    plt.scatter(suscriptores[i], precio[i], label=periodico)

plt.title("Número de suscriptores vs. Precio de la suscripción mensual (2024)")
plt.xlabel("Número de suscriptores")
plt.ylabel("Precio de la suscripción mensual (€)")
plt.legend()
plt.grid(True)
plt.show()
