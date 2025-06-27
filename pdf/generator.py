from fpdf import FPDF
from .formatter import format_rupiah
import datetime

class StrukPDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', (80, 200))
        self.set_auto_page_break(auto=True, margin=2)
        self.set_margins(7, 5, 7)
        self.add_page()
        self.set_font("Courier", size=8)
        self.content_width = 66
        self.line_width = 40

    def header_struk(self, data):
        self.set_font("Courier", 'B', 9)
        self.cell(self.content_width, 5, data['toko'], ln=1, align='C')
        self.set_font("Courier", size=8)
        self.cell(self.content_width, 4, "PT. SUMBER ALFARIA TRIJAYA, TBK", ln=1, align='C')
        self.cell(self.content_width, 4, "", ln=1)
        self.cell(self.content_width, 4, "ALFA TOWER LT.12, ALAM SUTERA, TANGERANG", ln=1, align='C')
        self.cell(self.content_width, 4, f"NPWP : {data['npwp']}", ln=1, align='C')
        self.cell(self.content_width, 4, data['alamat'], ln=1, align='C')
        self.cell(0, 4, "=" * 38, ln=1)
        self.cell(self.content_width, 4, f"Bon : {data['bon']}  Kasir: {data['kasir']}", ln=1)
        self.cell(0, 4, "=" * 38, ln=1)

    def body_struk(self, items):
        self.cell(self.content_width, 4, "Nama Barang       Qty Harga     Total", ln=1)
        total_item = 0
        total_diskon = 0
        subtotal = 0
        for item in items:
            nama = item['nama'][:15].ljust(15)
            qty = int(item['qty'])
            harga = int(item['harga'])
            disc = int(item.get('diskon', 0))
            total = qty * harga - disc
            subtotal += qty * harga
            total_diskon += disc
            total_item += qty
            self.cell(self.content_width, 4, f"{nama} {qty:>3} {format_rupiah(harga):>7} {format_rupiah(total):>9}", ln=1)
            if disc > 0:
                self.cell(self.content_width, 4, f"{'Disc.':15} {'':>3} {'':>7} -{format_rupiah(disc):>8}", ln=1)
        return total_item, subtotal, total_diskon

    def footer_struk(self, total_item, subtotal, total_diskon, bayar, metode, ppn_included=False, tanggal=None, jam=None):
        belanja_setelah_diskon = subtotal - total_diskon
        if ppn_included:
            ppn = int(belanja_setelah_diskon * 11 / 111)
            total_belanja = belanja_setelah_diskon
        else:
            ppn = int(belanja_setelah_diskon * 0.11)
            total_belanja = belanja_setelah_diskon + ppn

        kembali = bayar - total_belanja if metode == "Tunai" else 0

        self.cell(0, 4, "-" * 38, ln=1)

        def footer_line(label, qty, harga, total):
            label_fmt = label[:15].ljust(15)
            qty_fmt = f"{qty:>3}" if qty is not None else "   "
            harga_fmt = f"{format_rupiah(harga):>7}" if isinstance(harga, (int, float)) else "       "
            total_fmt = f"{format_rupiah(total):>9}"
            self.cell(self.content_width, 4, f"{label_fmt}{qty_fmt}{harga_fmt}{total_fmt}", ln=1)

        footer_line("Total Item", total_item, None, subtotal)
        footer_line("Total Disc.", None, None, total_diskon)
        footer_line("Total Belanja", None, None, total_belanja)
        footer_line(metode, None, None, bayar)
        if metode == "Tunai":
            footer_line("Kembalian", None, None, kembali)
        footer_line("PPN", None, None, ppn)

        self.cell(0, 4, "=" * 38, ln=1)
        self.cell(
            self.content_width,
            4,
            f"Tgl. {tanggal or datetime.datetime.now().strftime('%d-%m-%Y')} Jam {jam or datetime.datetime.now().strftime('%H:%M:%S')} V.2025.3.2",
            ln=1
        )
        self.cell(0, 4, "-" * 38, ln=1)
        self.cell(self.content_width, 4, "KRITIK&SARAN:1500959", ln=1, align='C')
