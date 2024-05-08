import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox


class CRM(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Müşteri İlişkileri Yönetimi (CRM)")
        self.setStyleSheet("background-color: ; font-family: Arial, sans-serif;")
        self.arayuz_olustur()
        self.veritabani_baglantisi_olustur()

    def arayuz_olustur(self):
        self.duzen = QVBoxLayout()
        
        self.heading_label = QLabel("Müşteri İlişkileri Yönetimi (CRM)")
        self.heading_label.setStyleSheet("font-size: 30px; color: darkkhaki;")
        self.duzen.addWidget(self.heading_label)

        # Customer (Müşteri) Section
        self.musteri_label = QLabel("Müşteri Adı:")
        self.musteri_label.setStyleSheet("font-weight: bold;")
        self.musteri_input = QLineEdit()
        self.duzen.addWidget(self.musteri_label)
        self.duzen.addWidget(self.musteri_input)

        self.iletisim_label = QLabel("İletişim Bilgileri:")
        self.iletisim_label.setStyleSheet("font-weight: bold;")
        self.iletisim_input = QLineEdit()
        self.duzen.addWidget(self.iletisim_label)
        self.duzen.addWidget(self.iletisim_input)

        self.musteri_ekle_button = QPushButton("Müşteri Ekle")
        self.musteri_ekle_button.setStyleSheet("background-color: #483D8B; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;")
        self.musteri_ekle_button.clicked.connect(self.musteri_ekle)
        self.duzen.addWidget(self.musteri_ekle_button)

        # Sale (Satış) Section
        self.satis_numarasi_label = QLabel("Satış Numarası:")
        self.satis_numarasi_label.setStyleSheet("font-weight: bold;")
        self.satis_numarasi_input = QLineEdit()
        self.duzen.addWidget(self.satis_numarasi_label)
        self.duzen.addWidget(self.satis_numarasi_input)

        self.satilan_urunler_label = QLabel("Satılan Ürünler:")
        self.satilan_urunler_label.setStyleSheet("font-weight: bold;")
        self.satilan_urunler_input = QLineEdit()
        self.duzen.addWidget(self.satilan_urunler_label)
        self.duzen.addWidget(self.satilan_urunler_input)

        # Support (Destek) Section
        self.destek_talebi_label = QLabel("Destek Talebi Detayları:")
        self.destek_talebi_label.setStyleSheet("font-weight: bold;")
        self.destek_talebi_input = QTextEdit()
        self.duzen.addWidget(self.destek_talebi_label)
        self.duzen.addWidget(self.destek_talebi_input)

        self.destek_talebi_ekle_button = QPushButton("Destek Talebi Oluştur")
        self.destek_talebi_ekle_button.setStyleSheet("background-color:#483D8B; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;")
        self.destek_talebi_ekle_button.clicked.connect(self.destek_talebi_olustur)
        self.duzen.addWidget(self.destek_talebi_ekle_button)

        # Delete Support (Destek) Ticket Section
        self.destek_talebi_sil_button = QPushButton("Destek Talebini Sil")
        self.destek_talebi_sil_button.setStyleSheet("background-color: #8B0000; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;")
        self.destek_talebi_sil_button.clicked.connect(self.destek_talebi_sil)
        self.duzen.addWidget(self.destek_talebi_sil_button)

        # Panel to display information
        self.info_panel = QTextEdit()
        self.info_panel.setReadOnly(True)
        self.duzen.addWidget(self.info_panel)

        self.setLayout(self.duzen)

    def veritabani_baglantisi_olustur(self):
        self.veritabani_baglantisi = sqlite3.connect('crm.db')
        self.cursor = self.veritabani_baglantisi.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Musteriler
                                (id INTEGER PRIMARY KEY,
                                ad TEXT,
                                iletisim TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS DestekTalepleri
                                (id INTEGER PRIMARY KEY,
                                musteri_id INTEGER,
                                detaylar TEXT,
                                FOREIGN KEY(musteri_id) REFERENCES Musteriler(id))''')
        self.veritabani_baglantisi.commit()

    def musteri_ekle(self):
        musteri_ad = self.musteri_input.text().strip()
        iletisim_bilgisi = self.iletisim_input.text().strip()

        if musteri_ad and iletisim_bilgisi:
            self.cursor.execute("INSERT INTO Musteriler (ad, iletisim) VALUES (?, ?)", (musteri_ad, iletisim_bilgisi))
            self.veritabani_baglantisi.commit()
            QMessageBox.information(self, "Başarılı", "Müşteri başarıyla eklendi!")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen müşteri adı ve iletişim bilgilerini girin.")

    def destek_talebi_olustur(self):
        musteri_id = self.musteri_input.text().strip()
        detaylar = self.destek_talebi_input.toPlainText().strip()
        satis_numarasi = self.satis_numarasi_input.text().strip()
        satilan_urunler = self.satilan_urunler_input.text().strip()

        if musteri_id and detaylar:
            self.cursor.execute("INSERT INTO DestekTalepleri (musteri_id, detaylar) VALUES (?, ?)", (musteri_id, detaylar))
            self.veritabani_baglantisi.commit()
            QMessageBox.information(self, "Başarılı", "Destek talebi başarıyla oluşturuldu!")
            # Display the information in the panel
            info_text = f"Müşteri ID: {musteri_id}\n"
            info_text += f"Destek Talebi Detayları: {detaylar}\n"
            info_text += f"Satış Numarası: {satis_numarasi}\n"
            info_text += f"Satılan Ürünler: {satilan_urunler}\n"
            self.info_panel.append(info_text)
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen müşteri ID ve destek talebi detaylarını girin.")

    def destek_talebi_sil(self):
        selected_text = self.info_panel.textCursor().selectedText()
        if selected_text:
            try:
                self.cursor.execute("DELETE FROM DestekTalepleri WHERE detaylar=?", (selected_text,))
                self.veritabani_baglantisi.commit()
                self.info_panel.setText("")
                QMessageBox.information(self, "Başarılı", "Destek talebi başarıyla silindi!")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek istediğiniz destek talebini seçin.")

    def closeEvent(self, event):
        self.veritabani_baglantisi.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CRM()
    window.show()
    sys.exit(app.exec_())
