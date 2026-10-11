import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore') 

print("--- VERİ MADENCİLİĞİ ÖDEVİ: VERİ TEMİZLEME VE GÖRSELLEŞTİRME ---\n")

dosya_dizini = os.path.dirname(os.path.abspath(__file__))

# ==========================================
# 1. VERİ YÜKLEME VE YAPISAL TEMİZLİK
# ==========================================
print("1. Veriler yükleniyor, metin formatları ve veri tipleri düzeltiliyor...")
try:
    df_calisanlar = pd.read_excel(os.path.join(dosya_dizini, 'Calisanlar.xlsx'))
except:
    df_calisanlar = pd.read_excel('Calisanlar.xlsx', header=None, skiprows=1, names=['Name', 'Gender', 'Age', 'City', 'Department', 'Salary', 'Email'])

df_ilanlar = pd.read_csv(os.path.join(dosya_dizini, 'Is_ilanlari.csv'), sep=';', on_bad_lines='skip')
df_ilanlar.columns = df_ilanlar.columns.str.replace(r'\\', '', regex=True)

for col in df_calisanlar.select_dtypes(include=['object']).columns: df_calisanlar[col] = df_calisanlar[col].astype(str).str.strip().str.title()
for col in df_ilanlar.select_dtypes(include=['object']).columns: df_ilanlar[col] = df_ilanlar[col].astype(str).str.strip().str.title()
df_calisanlar['Email'] = df_calisanlar['Email'].str.lower()

gizli_eksikler = ['-1', -1, '-1.0', 'Unknown', 'Unknown / Non-Applicable', 'na', 'N/A', 'null', '', 'Nan', 'None', '?', 'Gender']
df_calisanlar.replace(gizli_eksikler, np.nan, inplace=True)
df_ilanlar.replace(gizli_eksikler, np.nan, inplace=True)

df_calisanlar['Salary'] = pd.to_numeric(df_calisanlar['Salary'], errors='coerce')

# Yaş sütunundaki metinleri NaN'a çevirme
if 'Age' in df_calisanlar.columns: 
    df_calisanlar['Age'] = pd.to_numeric(df_calisanlar['Age'], errors='coerce')

for col in ['Rating', 'min_salary', 'max_salary', 'avg_salary', 'company_age']:
    if col in df_ilanlar.columns: 
        df_ilanlar[col] = pd.to_numeric(df_ilanlar[col].astype(str).str.replace(',', '.'), errors='coerce')

# ==========================================
# 2. EKSİK VERİ GÖRSELLEŞTİRMESİ
# ==========================================
print("2. Eksik veri haritaları PNG olarak kaydediliyor...")
plt.figure(figsize=(14, 5))
plt.subplot(1, 2, 1)
sns.heatmap(df_calisanlar.isnull(), cbar=False, cmap='viridis')
plt.title('Çalışanlar - Eksik Veriler (TEMİZLİK ÖNCESİ)')
plt.subplot(1, 2, 2)
sns.heatmap(df_ilanlar.isnull(), cbar=False, cmap='viridis')
plt.title('İş İlanları - Eksik Veriler (TEMİZLİK ÖNCESİ)')
plt.tight_layout()
plt.savefig(os.path.join(dosya_dizini, '1_Eksik_Veri_Oncesi.png'), dpi=300)
plt.close()

# ==========================================
# 3. EKSİK VERİ STRATEJİSİ
# ==========================================
print("3. Bilimsel doldurma stratejileri uygulanıyor...")

# 'Age' Sütununu Onarma
if 'Age' in df_calisanlar.columns:
    df_calisanlar.loc[df_calisanlar['Age'] >= 100, 'Age'] = df_calisanlar['Age'] / 10
    df_calisanlar['Age'] = df_calisanlar['Age'].fillna(df_calisanlar['Age'].mean())
    df_calisanlar['Age'] = df_calisanlar['Age'].round()

df_calisanlar.drop_duplicates(subset=['Email'], keep='first', inplace=True)

df_calisanlar['Salary'] = df_calisanlar.groupby('Department')['Salary'].transform(lambda x: x.fillna(x.mean()))
for col in df_calisanlar.columns:
    if df_calisanlar[col].isnull().sum() > 0:
        if df_calisanlar[col].dtype in ['float64', 'int64']: df_calisanlar[col] = df_calisanlar[col].fillna(df_calisanlar[col].mean())
        else: df_calisanlar[col] = df_calisanlar[col].fillna(df_calisanlar[col].mode()[0])

if 'company_age' in df_ilanlar.columns:
    df_ilanlar['company_age'] = df_ilanlar.groupby('Sector')['company_age'].transform(lambda x: x.fillna(x.mean()))

for col in df_ilanlar.columns:
    if df_ilanlar[col].isnull().sum() > 0:
        if df_ilanlar[col].dtype in ['float64', 'int64']: 
            df_ilanlar[col] = df_ilanlar[col].fillna(df_ilanlar[col].mean())
        else: 
            df_ilanlar[col] = df_ilanlar[col].fillna(df_ilanlar[col].mode()[0])

# ==========================================
# 4. AYKIRI DEĞER (OUTLIER) ANALİZİ
# ==========================================
print("4. Aykırı değerler tespit ediliyor (Boxplot grafikleri)...")
def iqr_baskila_ve_kaydet(df, column, dosya_eki, title_prefix):
    orijinal_veri = df[column].copy()
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    sns.boxplot(x=df[column], color='lightcoral')
    plt.title(f'{title_prefix} - Baskılama Öncesi')

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    alt_sinir = Q1 - 1.5 * IQR
    ust_sinir = Q3 + 1.5 * IQR

    df.loc[df[column] < alt_sinir, column] = alt_sinir
    df.loc[df[column] > ust_sinir, column] = ust_sinir

    plt.subplot(1, 2, 2)
    sns.boxplot(x=df[column], color='lightgreen')
    plt.title(f'{title_prefix} - Baskılama Sonrası')
    plt.tight_layout()
    plt.savefig(os.path.join(dosya_dizini, f'2_Outlier_Boxplot_{dosya_eki}.png'), dpi=300)
    plt.close()
    return orijinal_veri

calisanlar_orijinal_maas = iqr_baskila_ve_kaydet(df_calisanlar, 'Salary', 'Calisanlar_Maas', 'Çalışanlar: Maaş')
calisanlar_orijinal_yas = iqr_baskila_ve_kaydet(df_calisanlar, 'Age', 'Calisanlar_Yas', 'Çalışanlar: Yaş')
ilanlar_orijinal_yas = iqr_baskila_ve_kaydet(df_ilanlar, 'company_age', 'Ilanlar', 'İş İlanları: Şirket Yaşı')

# ==========================================
# 5. DAĞILIM (HİSTOGRAM) VE KATEGORİK GRAFİKLER
# ==========================================
print("5. Dağılım histogramları ve istenen kategorik grafikler hazırlanıyor...")
def dagilim_kaydet(orijinal, temizlenmis, dosya_eki, title):
    plt.figure(figsize=(8, 4))
    sns.histplot(orijinal, color='red', label='Orijinal', kde=True, alpha=0.4)
    sns.histplot(temizlenmis, color='blue', label='Temizlenmiş', kde=True, alpha=0.4)
    plt.legend()
    plt.title(title)
    plt.tight_layout()
    plt.savefig(os.path.join(dosya_dizini, f'3_Dagilim_Histogram_{dosya_eki}.png'), dpi=300)
    plt.close()

dagilim_kaydet(calisanlar_orijinal_maas, df_calisanlar['Salary'], 'Calisanlar_Maas', 'Çalışanlar: Maaş Dağılımı')
dagilim_kaydet(calisanlar_orijinal_yas, df_calisanlar['Age'], 'Calisanlar_Yas', 'Çalışanlar: Yaş Dağılımı')
dagilim_kaydet(ilanlar_orijinal_yas, df_ilanlar['company_age'], 'Ilanlar', 'İş İlanları: Şirket Yaşı Dağılımı')

kategorik_sutunlar = ['Headquarters', 'Size', 'Type of ownership', 'Industry', 'Sector', 'Revenue']

for col in kategorik_sutunlar:
    if col in df_ilanlar.columns:
        plt.figure(figsize=(10, 6))
        top_kategoriler = df_ilanlar[col].value_counts().nlargest(10).index
        sns.countplot(y=col, data=df_ilanlar, order=top_kategoriler, palette='magma')
        plt.title(f'İş İlanları - En Çok Dağılım Gösteren: {col} (Top 10)')
        plt.xlabel('İlan Sayısı (Frekans)')
        plt.ylabel(col)
        plt.tight_layout()
        plt.savefig(os.path.join(dosya_dizini, f'4_Kategorik_{col.replace(" ", "_")}.png'), dpi=300)
        plt.close()

# ==========================================
# 6. EXCEL DOSYASINA KAYDETME
# ==========================================
print("6. Temizlenmiş nihai veriler Excel'e aktarılıyor...")
df_calisanlar.to_excel(os.path.join(dosya_dizini, 'Calisanlar_Temiz.xlsx'), index=False)
df_ilanlar.to_excel(os.path.join(dosya_dizini, 'Is_Ilanlari_Temiz.xlsx'), index=False)

print("\n✓ HARİKA! İşlem tamamlandı.")