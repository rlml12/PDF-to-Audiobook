# Veri Madenciliği ve Temizleme Projesi (Data Cleaning & EDA)

Bu proje, yapısal bozukluklar ve eksik veriler içeren iki farklı veri setinin (`Calisanlar.xlsx` ve `Is_ilanlari.csv`) bilimsel yöntemlerle temizlenmesi, eksik veri stratejilerinin uygulanması, aykırı değer analizinin yapılması ve görselleştirilmesini içermektedir.

## Proje Adımları ve Bilimsel Yaklaşımlar

1. **Veri Yükleme ve Yapısal Temizlik:**
   * Sütunlardaki gizli boşluklar silinmiş ve metinler `Title Case` formatına standartlaştırılmıştır.
   * `?, -1, Unknown, N/A` gibi gizli eksik değerler tespit edilip yapısal `NaN` formatına dönüştürülmüştür.
   * Yanlış veri tipleri (örneğin virgüllü yazılmış maaşlar) matematiksel işlemlere uygun hale getirilmiştir.

2. **Eksik Veri Stratejisi (Imputation & Deletion):**
   * Kurtarılamayacak kadar yüksek oranda eksik/bozuk olan `Age` sütunu silinmiştir.
   * Tekrar eden (duplicate) e-posta kayıtları temizlenmiştir.
   * **Grouped Mean Imputation:** Çalışanların eksik maaşları, bulundukları *Departmanın* maaş ortalaması baz alınarak; İş ilanlarındaki eksik şirket yaşları ise *Sektör* ortalaması baz alınarak doldurulmuş ve orijinal varyans korunmuştur.
   * Kategorik verilerdeki eksiklikler, en çok tekrar eden değer (Mod) ile tamamlanmıştır.

3. **Aykırı Değer (Outlier) Analizi:**
   * Sayısal değişkenler (Maaş ve Şirket Yaşı) için Kutu Grafiği (Boxplot) analizi yapılmıştır.
   * İstatistiksel **IQR (Interquartile Range)** yöntemi kullanılarak aykırı değerler tespit edilmiş ve alt/üst sınırlara baskılanmıştır (Winsorization).

4. **Dağılım Kontrolü ve Görselleştirme:**
   * İşlem öncesi ve sonrası dağılımlar örtüşen Histogram grafikleri ile doğrulanmıştır.
   * Veri setinin profilini yansıtmak amacıyla sektörel ve boyutsal (Top 10) Bar grafik (Countplot) analizleri çıkarılmıştır.

## Kurulum ve Kullanım

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

1. Repoyu bilgisayarınıza klonlayın.
2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Temizleme ve görselleştirme scriptini çalıştırın:
   ```bash
   python proje.py
   ```

## Çıktılar
Script çalıştığında aşağıdaki dosyaları otomatik olarak proje dizinine üretir:
* `Calisanlar_Temiz.xlsx` ve `Is_Ilanlari_Temiz.xlsx` (Nihai temizlenmiş veri setleri)
* Eksik veri ısı haritaları (Heatmap PNG)
* Aykırı değer analiz grafikleri (Boxplot PNG)
* Dağılım kontrol grafikleri (Histogram PNG)
* Kategorik dağılım grafikleri (Barplot PNG)