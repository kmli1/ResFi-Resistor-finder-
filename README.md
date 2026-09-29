# ResFi

Klasik görüntü işleme ile dört bantlı direnç kodu okuma projesi.

## Mevcut durum

Aşama 1 başlangıç altyapısı: Python paketi, ortak veri sözleşmeleri, sınır testleri ve ekip çalışma kuralları. Henüz çalışan direnç tanıma, kamera veya Android uygulaması yoktur.

## Ekip

| Rol | Ad | GitHub kullanıcı adı | Ana sorumluluk |
|---|---|---|---|
| Kişi 1 | Kamil, ekipçe doğrulanacak | Doldurulacak | ROI, hizalama, kamera, entegrasyon |
| Kişi 2 | Doldurulacak | Doldurulacak | Bant segmentasyonu ve renk kuralları |
| Kişi 3 | Doldurulacak | Doldurulacak | Bant sırası, yön, karar ve değerlendirme |

## Kurulum

Repo kökünde PowerShell ile:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -e . --no-deps
.\.venv\Scripts\python.exe -c "import resfi, numpy; print(resfi.__version__, numpy.__version__)"
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Sanal ortamı etkinleştirmek gerekmez. Python 3.11 veya üzeri gerekir; ekip aynı minor sürümde anlaşmalıdır. Bu paket Python 3.12.14 ve NumPy 2.3.5 ile Linux üzerinde kontrol edildi; Windows ve kamera denemesi ekip tarafından yapılacaktır. Paketlenmiş ortam değil kaynak dosyalar sağlanır.

Bu aşamada standart kütüphanenin unittest aracı kullanılır; ek test paketi gerektirmez. Sonraki aşamada istenirse pytest bu unittest testlerini de çalıştırabilir. OpenCV bu pakette henüz bağımlılık değildir; görüntü giriş modülü eklendiğinde ekipçe sürümü seçilip gerçek bilgisayarlarda doğrulanacaktır. Bu, ana planın Aşama 1 kurulumu için küçük bir sadeleştirmedir.

## Çalışma düzeni

Ayrıntılı başlangıç: `docs/BASLANGIC.md`.
Ortak alanlar: `docs/contracts.md`.
Ekip kuralları: `docs/team-agreement.md`.

Her görev güncel main'den açılan kısa ömürlü branch'ta geliştirilir. PR başka üye tarafından incelenmeden main'e alınmaz. Her üye kendi hesabını kullanır. İlk ortak commit dışında normal geliştirme main'e doğrudan gönderilmez.

## Yöntem ve veri sınırları

Çalışma sırasında görüntü anlamak için AI modeli, OCR motoru veya öğrenilen sınıflandırıcı kullanılmaz. AI geliştirme desteği YapayZeka.md dosyasına kaydedilir. Kağıt kartlar ve gerçek direnç deneyleri ayrı raporlanır. Aynı fiziksel nesnenin benzer görüntüleri geliştirme ve final test arasında paylaşılmaz.

Gerçek fotoğraf henüz eklenmedi. Bu paketteki testler veri tanıma doğruluğu değil yazılım sözleşmesi kontrolleridir. Eğitim/test başarı oranı ölçülmedi. Sonraki aşamalar 14 aşamalı ana plana göre yürütülür.
