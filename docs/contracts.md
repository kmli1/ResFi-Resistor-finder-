# Ortak veri sözleşmesi

Durum: AI tarafından hazırlanmış Aşama 1 taslağı. Üç üyenin incelemesinden sonra ekip sözleşmesi olarak kabul edilecek.

| Tip | Üreten | Tüketen | Kritik kural |
|---|---|---|---|
| FrameInput | K1 | Kalite ve ROI | uint8 HxWx3, BGR, zaman damgası |
| QualityReport | K1 | K3 | Başarıda neden yok, başarısızlıkta ret nedeni var |
| NormalizedROI | K1 | K2 ve K3 | Yatay uzun eksen, iki maske, ters dönüşüm |
| BandCandidate | K2 | K3 | ROI içinde yarı açık x0/x1 aralığı |
| ColorEvidence | K2 | K3 | Sıfır veya birden fazla renk adayı korunur |
| FrameResult | K3 | K1 | ACCEPT dört bant ve değer; REJECT sayısal değer taşımaz |
| ScanResult | K3 | K1 | LOCKED geçerli okuma ve track kimliği gerektirir |

Koordinat başlangıcı sol üsttür; x sağa, y aşağı artar. source_bbox kaynak karede (x0,y0,x1,y1) yarı açık kutudur. Bant aralıkları normalize ROI koordinatlarındadır. sample_mask ROI'nin tam yüksekliği/genişliğinde olmalı; piksel kümesi x0:x1 içinde bulunmalıdır. Bu son boyut eşleştirmesi çağıran pipeline tarafından da doğrulanacaktır.

valid_mask ve body_mask uint8, 0/255 maskelerdir. Gövde maskesi dolgu piksellerini içeremez. Transform kaynak kareyi normalize ROI'ye, inverse_transform tersine taşır. Matrisler 3x3'tür ve çarpımları birim matrise eşit olmalıdır; OpenCV'den alınan matris ölçeği buna göre normalize edilir.

frame_id oturum içinde artar; timestamp_ms için aynı oturumdaki monoton saat kullanılır. Bu taslak alanın geçerliliğini kontrol eder; iki kare arasındaki artış denetimi kamera/stability modülünde olacaktır. Kalite eşikleri, yöntem veya karar skoru burada hesaplanmaz. rule_score 0-1 aralığında kural skoru olarak tanımlıdır; olasılık değildir.

Renk adları contracts.COLORS içinde İngilizcedir. Gri için gray kullanılır; grey, gri veya sari bu makine sözlüğünde yoktur. Arayüz Türkçeye çevirebilir. Renk rolünün ve sayısal direnç hesabının doğruluğunu decoder doğrular; FrameResult yalnız yapısal koşulları kontrol eder.

FrameResult.to_dict JSON'a uygun liste/sayı/null üretir. diagnostics içinde Python JSON türleri kullanın; NumPy scalar/array ve NaN otomatik dönüştürülmez, hata verir. Büyük görüntüler JSON içine konmaz. Dataclass frozen olsa da NumPy dizileri veya dict içerikleri derinlemesine değişmez değildir; modüller girdileri yerinde değiştirmemeli, gerekirse copy almalıdır.

## Değişiklik kuralı

Alan adı/tipi/anlamı değişecekse Issue açılır. Üreten ve tüketen iki üye inceler. contracts.py, bu belge ve ilgili test aynı PR'da güncellenir. Davranış değişikliği sessizce yapılmaz.

## İnceleme kaydı

- K1 onayı ve PR bağlantısı: Doldurulacak.
- K2 renk/maske değerlendirmesi: Doldurulacak.
- K3 sonuç/ret değerlendirmesi: Doldurulacak.
