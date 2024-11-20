import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk
#Membuka atau membuat file database SQLite bernama nilai_siswa.db.
#fungsi untuk membuat database dan tabel
# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswaaa.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''') ##Membuat tabel nilai_siswa
     # Kolom untuk menyimpan data siswa dan prediksi fakultas.
    conn.commit()#Menyimpan perubahan ke database.
    conn.close()#Menutup koneksi ke database.


def fetch_data():
    conn = sqlite3.connect('nilai_siswaaa.db') 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")#Mengambil semua data dari tabel nilai_siswa.
    rows = cursor.fetchall()#Mengembalikan hasil query sebagai daftar.
    conn.close()
    return rows

def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswaaa.db')# Membuka koneksi ke database SQLite
     # Perintah SQL untuk memasukkan data baru ke tabel 
    cursor = conn.cursor()  # Memperbaiki query SQL untuk memasukkan data baru ke dalam tabel nilai_siswa
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))  #Menambahkan data baru ke tabel
    conn.commit()
    conn.close()

def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswaaa.db')
    cursor = conn.cursor() # Perintah SQL untuk memperbarui data dalam tabel nilai_siswa
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()
    conn.close()
#delete_database digunakan untuk menghapus baris data tertentu dari 
# tabel nilai_siswa dalam database SQLite berdasarkan ID (kolom id).
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswaaa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()
#Fungsi ini membantu memprediksi fakultas yang cocok 
# untuk siswa berdasarkan nilai mereka.
def calculate_prediction(biologi, fisika, inggris):  #Fungsi ini menerima tiga parameter :biologi,fisika,inggris
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    #Jika nilai Biologi lebih besar dari nilai Fisika dan lebih besar dari nilai Bahasa Inggris,
    #  maka fungsi akan mengembalikan hasil "Kedokteran". 
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    #Jika nilai Fisika lebih besar dari nilai Biologi dan lebih besar dari nilai Bahasa Inggris,
    #  maka fungsi akan mengembalikan hasil "Teknik".
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
     #Jika nilai Bahasa Inggris lebih besar dari nilai Biologi dan lebih besar dari nilai Fisika, 
     # maka fungsi akan mengembalikan hasil "Bahasa".
    else:
        return "Tidak Diketahui"
    #ika tidak ada nilai yang lebih besar dari dua nilai lainnya (misalnya, jika nilai-nilai sama besar), 
    # maka fungsi akan mengembalikan hasil "Tidak Diketahui".

def submit():
#Fungsi submit dirancang untuk menangani input data dari pengguna, memvalidasi data,
#  memproses prediksi fakultas, menyimpan data ke database, dan memperbarui tampilan aplikasi dengan data baru.
    try: #try digunakan untuk menangkap kesalahan (error) yang mungkin terjadi selama eksekusi kode di dalamnya.
        nama = nama_var.get()  #Mengambil input dari kolom Nama Siswa.Disimpan dalam variabel nama
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())
        #Mengambil input nilai Biologi, Fisika, dan Bahasa Inggris, 
        # lalu dikonversi ke tipe data integer menggunakan int()
        if not nama: #Mengecek apakah variabel nama kosong.
            raise Exception("Nama siswa tidak boleh kosong.")
        #Jika kosong, maka akan memunculkan Exception dengan pesan "Nama siswa tidak boleh kosong."
        prediksi = calculate_prediction(biologi, fisika, inggris)#menentukan fakultas berdasarkan nilai Biologi, Fisika, dan Bahasa Inggris.
        save_to_database(nama, biologi, fisika, inggris, prediksi)#enyimpan data siswa ke tabel nilai_siswa di database.

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        #Menampilkan pesan notifikasi sukses menggunakan kotak dialog messagebox.showinfo.
        clear_inputs()
        populate_table()
    except ValueError as e:  #menangkap error jika input nilai 
        messagebox.showerror("Error", f"Input tidak valid: {e}") #Menampilkan pesan error kepada pengguna

def update():#Fungsi update dirancang untuk memperbarui data siswa yang sudah ada di database berdasarkan input dari pengguna. 
    try:
        if not selected_record_id.get():  #Mengecek apakah ID data yang dipilih dari tabel kosong.
            raise Exception("Pilih data dari tabel untuk di-update!")
        #ika kosong, program akan menampilkan error dengan pesan "Pilih data dari tabel untuk di-update!"
        record_id = int(selected_record_id.get()) #Menyimpan ID data yang dipilih dari tabel (bertipe integer
        nama = nama_var.get()
        biologi = int(biologi_var.get())#Mengambil input dari form, lalu menyimpan nilai-nilai tersebut ke variabel.
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)
        #Memanggil fungsi update_database untuk memperbarui data di database.
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def delete(): #Fungsi delete bertugas untuk menghapus data yang dipilih dari tabel.
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())#Mengambil ID dari data yang dipilih pada tabel dan mengonversinya menjadi tipe integer.
        delete_database(record_id)#Fungsi delete_database digunakan untuk menghapus data dari database berdasarkan ID yang sudah didapatkan sebelumnya.
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()
        populate_table()#Memperbarui tabel untuk menampilkan data terbaru dari database.
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def clear_inputs():#Fungsi ini bertugas untuk membersihkan input pada form,
    nama_var.set("")#mengosongkan input field untuk nama siswa.
    biologi_var.set("") #mengosongkan input field untuk nilai Biologi.
    fisika_var.set("") #mengosongkan input field untuk nilai Fisika.
    inggris_var.set("") #mengosongkan input field untuk nilai Bahasa Inggris.
    selected_record_id.set("") #Mengatur nilai selected_record_id (yang menyimpan ID record yang dipilih) menjadi string kosong.
#set("") digunakan untuk mengatur nilai dari variabel input menjadi string kosong (""), yang berarti menghapus teks yang ada di dalamnya.

def populate_table(): #bekerja dengan menghapus data lama yang ada di tabel, kemudian menambahkannya kembali dengan data terbaru yang diambil dari database.
    for row in tree.get_children(): #mengembalikan daftar semua item (baris) yang ada dalam tabel tree (yang merupakan komponen Treeview di Tkinter)
        tree.delete(row) #menghapus setiap baris yang ada di tabel tree. row adalah setiap item yang dikembalikan oleh get_children() (yaitu ID dari setiap baris dalam tabel).
    for row in fetch_data(): #mengambil semua data yang ada di database.
        tree.insert('', 'end', values=row) #Fungsi insert() digunakan untuk menambahkan baris data baru ke dalam tabel tree.
    #Parameter pertama '' berarti data akan dimasukkan di tingkat root
    #Parameter kedua 'end' berarti data akan dimasukkan di bagian akhir tabel.
    #Parameter ketiga values=row menunjukkan bahwa data yang akan dimasukkan adalah nilai row, yang berisi data yang diambil dari database

def fill_inputs_from_table(event): #Fungsi fill_inputs_from_table memungkinkan pengguna untuk memilih data dari tabel dan secara otomatis mengisi form dengan data tersebut
    try:
        selected_item = tree.selection()[0] #Fungsi ini digunakan untuk mendapatkan item yang dipilih (baris) di dalam Treeview (tabel tree). [0] berarti mengambil item pertama dari daftar tersebut
        selected_row = tree.item(selected_item)['values'] #Fungsi ini mengembalikan informasi lengkap tentang item yang dipilih di tabel.['values'] digunakan untuk mengakses nilai-nilai 

        selected_record_id.set(selected_row[0]) #yang menyimpan ID record yang dipilih
        nama_var.set(selected_row[1]) #nama siswa yang diambil dari baris yang dipilih.
        biologi_var.set(selected_row[2]) #untuk input nilai biolog
        fisika_var.set(selected_row[3])#untuk input nilai fisika
        inggris_var.set(selected_row[4])#untuk input nilai inggris
    except IndexError: #mengembalikan daftar kosong
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih
#membuat form input dengan label dan entry fields 
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)
#Label adalah widget yang digunakan untuk menampilkan teks di GUI.
#root adalah window utama (sebuah objek dari kelas Tk())
#text="Nama Siswa" menampilkan teks "Nama Siswa" di label.
#grid(row=0, column=0) menyusun label pada baris ke-0 dan kolom ke-0 dalam layout grid (penataan widget).
#padx=10, pady=5 memberikan padding horizontal 10 dan vertikal 5 antara widget dan batasnya.
Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)
#Entry adalah widget input yang memungkinkan pengguna untuk memasukkan teks.
#textvariable=nama_var menghubungkan widget Entry dengan variabel nama_var, sehingga nilai yang dimasukkan di dalam Entry disimpan di nama_var.
#grid(row=0, column=1) menyusun Entry di baris ke-0 dan kolom ke-1.
#Padding yang sama diterapkan di sini dengan padx=10, pady=5.
Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)
#Button adalah widget yang digunakan untuk membuat tombol.
#root adalah window utama tempat tombol ditempatkan.
#text="Add" memberikan label "Add" pada tombol.
#command=submit menunjukkan bahwa saat tombol diklik, fungsi submit() akan dipanggil untuk menambahkan data.
#grid(row=4, column=0) menempatkan tombol pada baris ke-4 dan kolom ke-0.
# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')
#columns adalah tuple yang berisi nama-nama kolom yang akan digunakan dalam Treeview.
# Mengatur posisi isi tabel di tengah
# Mengatur posisi isi tabel di tengah
for col in columns: #loop yang akan iterasi (berulang) untuk setiap nama kolom yang ada dalam columns.
    tree.heading(col, text=col.capitalize()) #digunakan untuk mengatur judul (header) untuk setiap kolom di Treeview
    #col.capitalize() mengubah nama kolom menjadi kapital pertama saja.
    tree.column(col, anchor='center') #igunakan untuk mengatur alignment (penyelarasan) isi kolom pada Treeview.
    #nama kolom yang sedang diproses dalam loop
    #anchor='center' memastikan bahwa teks di setiap kolom akan terpusat (center-aligned).

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
#digunakan untuk menempatkan Treeview ke dalam grid
#row=5: Menempatkan Treeview pada baris ke-5 grid (row 5).
#column=0: Menempatkan Treeview pada kolom ke-0 (kolom pertama).
#columnspan=3: Membuat Treeview meluas ke 3 kolom
#padx=10, pady=10: Memberikan padding (jarak)
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)
#tree.bind() adalah cara untuk menghubungkan (bind) sebuah event ke sebuah fungsi.
#'<ButtonRelease-1>': Ini adalah event yang terpicu ketika tombol mouse kiri (button 1) dilepaskan setelah ditekan.
#fill_inputs_from_table: Ketika event ButtonRelease-1 terjadi

populate_table()#Fungsi ini dipanggil untuk mengisi Treeview dengan data yang ada di dalam database.

root.mainloop()    #perintah terakhir yang diperlukan untuk menjalankan aplikasi Tkinter.