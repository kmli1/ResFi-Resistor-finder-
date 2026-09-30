# Ekip çalışma sözleşmesi

Durum: Taslak. Aşağıdaki kurallar üyeler tarafından görüşülüp PR'da onaylanacaktır.

1. Tek ortak repo ve üç ayrı GitHub hesabı kullanılır.
2. main çalışabilir ortak sürümdür. İlk README commit'inden sonraki değişiklikler PR ile girer.
3. Bir görev için bir branch açılır. İlk branch: k1/a01-bootstrap.
4. K1'in ana inceleyicisi K2; K2'ninki K3; K3'ünki K1'dir. Arayüz değişiyorsa diğer tüketici de inceler.
5. Her üye kendi işini yapar, anlar ve kendi hesabıyla commit/PR gönderir. Boş commit katkı sayılmaz.
6. K1 bootstrap main'e girdikten sonra K2 k2/a01-color-contract; K3 k3/a01-decision-contract dallarını açar.
7. Ortak docs/contracts.md ve tests/test_contracts.py değişiklikleri mümkünse sırayla birleşir. Sonraki yazar güncel main'i kendi dalına alır.
8. Ortak dosyalarda yapılan başka değişiklikler silinmez. Force push yerine fetch ve merge ile senkronizasyon tercih edilir.
9. AI katkısı YapayZeka.md içinde öneri/uygulama/test ayrımıyla kaydedilir. Öğrenci kısmını öğrenci doldurur.
10. Geliştirme/test ayrımı veri toplanırken yapılır. Son teste bakılarak eşik değiştirilmez.

## Aşama 1 tamamlanma ölçütü

- Üç üye de README komutlarıyla kendi bilgisayarında paketi kurabildi.
- Testler geçti ve PR'da komut/ortam/sonuç yazıldı.
- K1 bootstrap PR'ı başka üye incelemesiyle birleşti.
- K2 renk/maske arayüzünü, K3 karar/ret arayüzünü okudu; gerekli gerçek düzeltme ve kontrolleri kendi PR'larında yaptı.
- İsimler, kullanıcı adları ve AI öğrenci değerlendirmeleri dolduruldu.
- Herkes kendi branch'ını açmayı, push etmeyi ve PR oluşturmayı gösterebiliyor.

Bu aşamadaki arayüz işi, ileride her kişinin gerçek görüntü işleme bileşeni geliştirme yükümlülüğünü tek başına tamamlamaz.
