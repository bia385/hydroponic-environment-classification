import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk

data = pd.read_csv('Dataset2.csv', delimiter=';')
print(data.head())
print(data.columns)
print(data.shape)

# Mengganti koma dengan titik pada 'ph air' dan mengonversi menjadi float
data['ph air'] = data['ph air'].str.replace(',', '.').astype(float)

# mengubah data menjadi dummy variabel
data = pd.get_dummies(data, columns=['musim', 'kategori', 'tanaman'])

X = data.drop(['kategori_baik', 'kategori_buruk'], axis=1)
y = data['kategori_baik']  

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=49)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=49)
model.fit(X_train, y_train)

from sklearn.metrics import classification_report, accuracy_score
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

akurasi = accuracy_score(y_test, y_pred)
print("\nAkurasi:", akurasi)

# Membuat GUI menggunakan tkinter
from tkinter import messagebox

def predict():
    try:
        suhu = float(entry_suhu.get())
        ph_air = float(entry_ph_air.get())
        musim = entry_musim.get().strip().lower()

        if musim == "kemarau":
            musim_panas = 1
            musim_hujan = 0
        elif musim == "hujan":
            musim_panas = 0
            musim_hujan = 1
        else:
            raise ValueError("Input musim tidak valid")

        X_value = [suhu, ph_air, musim_panas, musim_hujan]
        
        # Menambahkan kolom tanaman dengan nilai 0 untuk prediksi
        X_value.extend([0, 0, 0, 0])
        
        prediksi_lingkungan = model.predict([X_value])[0]
        hasil = "Lingkungan tersebut cocok digunakan untuk menanam hidroponik" if prediksi_lingkungan == 1 else "Lingkungan tersebut tidak cocok digunakan untuk menanam hidroponik"
        
        rekomendasi = ""
        if hasil == "Lingkungan tersebut cocok digunakan untuk menanam hidroponik":
            # Logika rekomendasi tanaman
            rekomendasi = "Rekomendasi tanaman : Sawi, Bayam, Kangkung, atau Selada"
        
        messagebox.showinfo("Hasil Prediksi", f"{hasil}\n\n{rekomendasi}")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Tata letak GUI
root = tk.Tk()
root.title("Prediksi Lingkungan Pada Hidroponik")

tk.Label(root, text="Suhu (°), (masukkan suhu antara 19°-28°):").grid(row=0, column=0)
entry_suhu = tk.Entry(root)
entry_suhu.grid(row=0, column=1)

tk.Label(root, text="pH Air (masukkan pH air antara 4-7):").grid(row=1, column=0)
entry_ph_air = tk.Entry(root)
entry_ph_air.grid(row=1, column=1)

tk.Label(root, text="Musim (masukkan musim hujan atau kemarau):").grid(row=2, column=0)
entry_musim = tk.Entry(root)
entry_musim.grid(row=2, column=1)

tk.Button(root, text="Prediksi", command=predict).grid(row=3, column=0, columnspan=2, pady=4)

root.mainloop()

