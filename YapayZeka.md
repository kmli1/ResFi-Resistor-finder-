# Yapay zeka kullanım kayıtları

Bu dosyadaki oturum kayıtları yapay zekâ yardımıyla hazırlanır. Her kayıt, yalnızca belirtilen oturumun erişilebilir bağlamını kapsar. Öğrenciler kayıtları kontrol etmekten, kaynakları doğrulamaktan ve teslim edilen çalışmanın tamamını açıklayabilmekten sorumludur.

## Oturum 1 - 29 Eylül 2026

Bu paket yeni boş repo için hazırlanmıştır. Önceki planlama oturumunun kaydı bu dosyada birleştirilmiş değildir; ekip onu ayrıca doğrulanmış bilgilerle eklemelidir. Başka bir mevcut YapayZeka.md varsa üzerine yazmayın, yalnız bu yeni kaydı ekleyin ve oturum numarasını uyarlayın.

### Oturum bilgileri

- Katılan öğrenci: Kamil.
- Kullanılan araç: ChatGPT/Codex. Kesin model adı doğrulanmadı.
- Amaç: Boş ortak repo için Aşama 1 altyapısı ve uygulama talimatı.
- İlgili commit veya PR: Öğrenci tarafından sonradan eklenecek.

### Yapay zeka katkısı

| İş | Katkı türü | İlgili dosya | Uygulama durumu |
|---|---|---|---|
| Paket ve klasör iskeleti | Kod üretimi | pyproject.toml, src/resfi | Yerel başlangıç paketine uygulandı |
| Yedi ortak veri tipi | Kod üretimi | contracts.py | Yerel pakete uygulandı; sınır testleri çalıştırıldı |
| Sözleşme testleri | Test hazırlama | test_contracts.py | 13 test Linux ortamında geçti |
| Repo ve branch talimatları | Dokümantasyon | docs/BASLANGIC.md | Yazıldı; kullanıcının GitHub reposunda uygulanmadı |
| Sorumluluk ve inceleme kuralları | Yöntem önerisi | docs/team-agreement.md | Taslak; ekip onayı bekleniyor |

### Yöntem ve ders kapsamına uygunluk

Bu aşamada görüntü tanıma algoritması yazılmadı; veri türleri ve doğrulama kuralları eklendi. NumPy görüntü dizileri için kullanılır. Çalışma sırasında AI/OCR/öğrenilen sınıflandırıcı çağrısı bulunmaz. Diğer modüller uygulama içermeyen yer tutuculardır. OpenCV ve kamera işlemleri sonraki aşamada eklenecektir. Başlangıç testleri standart unittest ile çalışır; bu, ana plandaki pytest kurulumunu bu aşama için sadeleştirir.

### Literatür taramasına yapay zeka katkısı

Akademik literatür taraması yapılmadı. GitHub'ın resmi repo klonlama ve PR oluşturma belgeleri kurulum talimatları için kontrol edildi; Literatur.md içinde akademik kaynak incelemesi tamamlanmış sayılmadı.

### Doğrulama ve açık sorunlar

Python 3.12.14, NumPy 2.3.5 ve Linux üzerinde 13 sözleşme testi çalıştırıldı ve geçti. Testler görüntü tanıma doğruluğunu ölçmez. Windows kurulum adımları, kullanıcının GitHub erişimi, gerçek kamera ve renk çözümü bu oturumda test edilmedi. Öğrencilerin kodu okuyup doğruladığı henüz bilinmiyor. GitHub'a commit, push, PR veya davet gönderilmedi.

### Öğrencinin dolduracağı bölüm

- Yapay zekâ çıktısında neyi değiştirdik veya reddettik, neden?
- Hangi kodu ve sonucu kendimiz kontrol ettik?
- Önerilen kaynaklardan hangilerini kendimiz okuyup doğruladık?
- Yapay zekânın kaynak bilgisi veya yorumunda hangi düzeltmeleri yaptık?
- Bu oturumda ne öğrendik?
- Kaydı kontrol eden öğrenciler:
