import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pdf.generator import StrukPDF
from pdf.formatter import generate_npwp, generate_bon, format_rupiah
import datetime

class StrukApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cetak Struk Alfamart/Indomaret")

        self.data = {
            'toko': tk.StringVar(value='ALFAMART CONTOH'),
            'alamat': tk.StringVar(value='JL. CONTOH RAYA NO.123'),
            'npwp': tk.StringVar(),
            'bon': tk.StringVar(),
            'kasir': tk.StringVar(value='Rina'),
            'metode': tk.StringVar(value='Tunai'),
            'bayar': tk.StringVar(value='20000'),
            'tanggal': tk.StringVar(),
            'jam': tk.StringVar(),
            'ppn_included': tk.BooleanVar(value=False)
        }

        self.items = []
        self.build_form()

    def build_form(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill='both', expand=True)

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)

        ttk.Label(frame, text="Nama Toko").grid(row=0, column=0, sticky='w')
        ttk.Entry(frame, textvariable=self.data['toko']).grid(row=0, column=1, columnspan=3, sticky='we')

        ttk.Label(frame, text="Alamat").grid(row=1, column=0, sticky='w')
        ttk.Entry(frame, textvariable=self.data['alamat']).grid(row=1, column=1, columnspan=3, sticky='we')

        ttk.Label(frame, text="NPWP (kosong = random)").grid(row=2, column=0, sticky='w')
        ttk.Entry(frame, textvariable=self.data['npwp']).grid(row=2, column=1, columnspan=3, sticky='we')

        ttk.Label(frame, text="BON (kosong = random)").grid(row=3, column=0, sticky='w')
        ttk.Entry(frame, textvariable=self.data['bon']).grid(row=3, column=1, columnspan=3, sticky='we')

        ttk.Label(frame, text="Kasir").grid(row=4, column=0, sticky='w')
        ttk.Entry(frame, textvariable=self.data['kasir']).grid(row=4, column=1)

        ttk.Label(frame, text="Metode").grid(row=4, column=2, sticky='e')
        metode = ttk.Combobox(frame, textvariable=self.data['metode'], values=['Tunai', 'Debit'], width=10)
        metode.grid(row=4, column=3, sticky='w')

        ttk.Label(frame, text="Bayar").grid(row=5, column=0, sticky='w')
        ttk.Entry(frame, textvariable=self.data['bayar']).grid(row=5, column=1)

        ttk.Label(frame, text="Tanggal (dd-mm-yyyy)").grid(row=5, column=2, sticky='e')
        ttk.Entry(frame, textvariable=self.data['tanggal']).grid(row=5, column=3)

        ttk.Label(frame, text="Jam (hh:mm:ss)").grid(row=6, column=2, sticky='e')
        ttk.Entry(frame, textvariable=self.data['jam']).grid(row=6, column=3)

        ttk.Checkbutton(frame, text="Harga sudah termasuk PPN (11%)", variable=self.data['ppn_included']).grid(row=6, column=0, columnspan=2, sticky='w')

        ttk.Label(frame, text="Tambah Barang:").grid(row=7, column=0, columnspan=6, sticky='w', pady=(10,0))
        ttk.Label(frame, text="Nama Barang").grid(row=8, column=0, sticky='ew')
        ttk.Label(frame, text="Qty").grid(row=8, column=1, sticky='ew')
        ttk.Label(frame, text="Harga").grid(row=8, column=2, sticky='ew')
        ttk.Label(frame, text="Diskon").grid(row=8, column=3, sticky='ew')

        self.entry_nama = tk.Entry(frame)
        self.entry_nama.grid(row=9, column=0, sticky='ew')

        self.entry_qty = tk.Entry(frame)
        self.entry_qty.grid(row=9, column=1, sticky='ew')

        self.entry_harga = tk.Entry(frame)
        self.entry_harga.grid(row=9, column=2, sticky='ew')

        self.entry_diskon = tk.Entry(frame)
        self.entry_diskon.grid(row=9, column=3, sticky='ew')

        ttk.Button(frame, text="+", command=self.tambah_barang).grid(row=9, column=4)
        ttk.Button(frame, text="Hapus Barang", command=self.hapus_barang).grid(row=9, column=5)

        tree_frame = ttk.Frame(frame)
        tree_frame.grid(row=10, column=0, columnspan=6, sticky='nsew', pady=5)
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')

        self.tree = ttk.Treeview(tree_frame, columns=("nama", "qty", "harga", "diskon"), show='headings', height=5, yscrollcommand=tree_scroll.set)
        self.tree.heading("nama", text="Nama Barang")
        self.tree.heading("qty", text="Qty")
        self.tree.heading("harga", text="Harga")
        self.tree.heading("diskon", text="Diskon")
        self.tree.pack(fill='both', expand=True)
        tree_scroll.config(command=self.tree.yview)

        ttk.Button(frame, text="Cetak Struk", command=self.cetak_struk).grid(row=11, column=0, columnspan=6, pady=10)

    def tambah_barang(self):
        nama = self.entry_nama.get().strip()
        if not nama:
            messagebox.showerror("Input Salah", "Nama barang tidak boleh kosong")
            return
        try:
            qty = int(self.entry_qty.get())
            harga = int(self.entry_harga.get())
            diskon = int(self.entry_diskon.get() or 0)
        except ValueError:
            messagebox.showerror("Input Salah", "Qty, Harga, dan Diskon harus berupa angka")
            return

        for item in self.items:
            if item['nama'].lower() == nama.lower():
                if messagebox.askyesno("Barang Sama", "Barang dengan nama sama sudah ada. Gabungkan?"):
                    item['qty'] += qty
                    item['harga'] = harga
                    item['diskon'] += diskon
                    self.refresh_tree()
                    return

        self.items.append({'nama': nama, 'qty': qty, 'harga': harga, 'diskon': diskon})
        self.tree.insert('', 'end', values=(nama, qty, format_rupiah(harga), format_rupiah(diskon)))
        self.entry_nama.delete(0, 'end')
        self.entry_qty.delete(0, 'end')
        self.entry_harga.delete(0, 'end')
        self.entry_diskon.delete(0, 'end')

    def hapus_barang(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Tidak ada pilihan", "Pilih salah satu barang untuk dihapus")
            return
        for i in selected:
            idx = self.tree.index(i)
            self.tree.delete(i)
            del self.items[idx]

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in self.items:
            self.tree.insert('', 'end', values=(item['nama'], item['qty'], format_rupiah(item['harga']), format_rupiah(item['diskon'])))

    def cetak_struk(self):
        if not self.items:
            messagebox.showwarning("Barang Kosong", "Tambahkan minimal 1 barang dulu")
            return

        if not self.data['toko'].get().strip():
            messagebox.showerror("Input Wajib", "Nama toko harus diisi.")
            return
        if not self.data['alamat'].get().strip():
            messagebox.showerror("Input Wajib", "Alamat toko harus diisi.")
            return
        if not self.data['kasir'].get().strip():
            messagebox.showerror("Input Wajib", "Nama kasir harus diisi.")
            return

        bayar_str = self.data['bayar'].get().strip()
        if not bayar_str:
            messagebox.showerror("Input Wajib", "Jumlah bayar harus diisi.")
            return
        try:
            bayar = int(bayar_str)
            if bayar <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Wajib", "Jumlah bayar harus berupa angka lebih dari 0.")
            return

        try:
            if self.data['tanggal'].get():
                datetime.datetime.strptime(self.data['tanggal'].get(), "%d-%m-%Y")
            if self.data['jam'].get():
                datetime.datetime.strptime(self.data['jam'].get(), "%H:%M:%S")
        except ValueError:
            messagebox.showerror("Format Salah", "Gunakan format tanggal: dd-mm-yyyy dan jam: hh:mm:ss")
            return

        npwp = self.data['npwp'].get() or generate_npwp()
        bon = self.data['bon'].get() or generate_bon()
        tanggal = self.data['tanggal'].get()
        jam = self.data['jam'].get()

        if not tanggal or not jam:
            now = datetime.datetime.now()
            tanggal = tanggal or now.strftime('%d-%m-%Y')
            jam = jam or now.strftime('%H:%M:%S')

        pdf = StrukPDF()
        data = {
            'toko': self.data['toko'].get(),
            'alamat': self.data['alamat'].get(),
            'npwp': npwp,
            'bon': bon,
            'kasir': self.data['kasir'].get(),
            'tanggal': tanggal,
            'jam': jam,
            'ppn_included': self.data['ppn_included'].get()
        }
        pdf.header_struk(data)
        total_item, subtotal, total_diskon = pdf.body_struk(self.items)

        belanja_setelah_diskon = subtotal - total_diskon
        if self.data['ppn_included'].get():
            ppn = int(belanja_setelah_diskon * 11 / 111)
            total_belanja = belanja_setelah_diskon
        else:
            ppn = int(belanja_setelah_diskon * 0.11)
            total_belanja = belanja_setelah_diskon + ppn

        if self.data['metode'].get() == "Tunai" and bayar < total_belanja:
            messagebox.showerror("Bayar Kurang", f"Jumlah bayar ({format_rupiah(bayar)}) kurang dari total belanja ({format_rupiah(total_belanja)}).")
            return

        pdf.footer_struk(
            total_item, subtotal, total_diskon,
            bayar=bayar,
            metode=self.data['metode'].get(),
            ppn_included=self.data['ppn_included'].get(),
            tanggal=tanggal,
            jam=jam
        )

        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"struk_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        if filename:
            pdf.output(filename)
            messagebox.showinfo("Selesai", f"Struk berhasil disimpan sebagai\n{filename}")

if __name__ == '__main__':
    root = tk.Tk()
    app = StrukApp(root)
    root.mainloop()
