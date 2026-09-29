# Boş repodan Aşama 1 kurulumu

Komutlar Windows PowerShell içindir. Her bloğu sırayla çalıştırın; hata varsa sonraki bloğa geçmeden nedenini çözün. GitHub repo URL'si bilinmediği için Read-Host size kendi URL'nizi sorar. Aynı isimli yerel klasör varsa klonlama için başka hedef ad seçin; mevcut klasörü silmeyin.

## 1 Yalnız Kişi 1 ilk main commitini oluşturur

VS Code'da terminali projeyi saklayacağınız üst klasörde açın. Henüz ZIP dosyalarını kopyalamayın.

```powershell
$resfiRepoUrl = Read-Host "GitHub reponuzun HTTPS adresini yapistirin"
git clone $resfiRepoUrl ResFi
cd ResFi
git config user.name "KENDI ADINIZ"
git config user.email "GITHUB E-POSTANIZ"
git branch -M main
Set-Content -Path README.md -Value "# ResFi" -Encoding utf8
git add README.md
git commit -m "chore: initialize repository"
git push -u origin main
```

Ad/e-posta yer tutucularını gerçek bilgilerinizle değiştirin. Empty repository uyarısı bu durumda normaldir. Başka üye bu sırada commit göndermemelidir. GitHub'a giriş gerektiğinde kendi hesabınızı kullanın. main zaten başka bir işlemle oluşturulduysa bu ilk-commit bloğunu tekrarlamayın; güncel main'i alın.

## 2 Başlangıç branchini açın

```powershell
git switch -c k1/a01-bootstrap
```

ZIP'i başka bir klasöre çıkarın. İçindeki README.md, requirements.txt, pyproject.toml, src, tests, docs, data, config, results ve noktayla başlayan dosya/klasörleri klonladığınız ResFi köküne kopyalayın. README'nin başlangıçtaki tek satırlık halini paketteki README ile değiştirin. ResFi içinde ikinci bir ResFi klasörü oluşmasın. ZIP içinde .git veya .venv yoktur. Yereldeki .git klasörünü taşımayın/silmeyin.

## 3 Ortamı kurup kontrol edin

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -e . --no-deps
.\.venv\Scripts\python.exe -c "import resfi; print(resfi.__version__)"
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Beklenen: sürüm 0.1.0 ve mevcut pakette 13 testin OK olması. Bu yalnız sözleşme testidir; kamera başarısı değildir. Python veya Git bulunamadıysa önce terminali yeniden açın ve kurulum yolunu kontrol edin. requirements yüklemesi internet gerektirir.

## 4 Kendi bilgilerinizi doldurun ve push edin

README ekip alanını ve YapayZeka.md öğrenci bölümünü gerçekten yaptıklarınıza göre doldurun. Kişi 2/3 yerine isimlerini yazın. Henüz yapmadığınız incelemeyi tamamlandı işaretlemeyin.

```powershell
git status
git add .gitignore .gitattributes .github
git add README.md requirements.txt pyproject.toml
git add src tests docs data config results
git add Rapor.md Literatur.md YapayZeka.md
git diff --cached --stat
git diff --cached
git commit -m "chore: add stage one scaffold and contracts"
git push -u origin k1/a01-bootstrap
```

Diff içinde .venv veya özel dosya olmadığını kontrol edin. main'de başlangıç README'si kalması normaldir; yeni dosyalar branch'ta bulunur.

## 5 PR açın ve inceletin

GitHub Pull requests > New pull request. base main, compare k1/a01-bootstrap. Başlık: chore: add stage one scaffold and contracts. Şablonu doldurun. K2'yi ana inceleyici, K3'ü sonuç sözleşmesi için ek inceleyici seçin. İnceleme yapılmadan kendi kendinize onay varmış gibi birleştirmeyin.

K2/K3 PR incelemesi için kendi bilgisayarında:

```powershell
# Repo ilk kez alinacaksa clone ve cd yapin.
git clone https://github.com/REPO_SAHIBI/REPO_ADI.git ResFi
cd ResFi
git fetch origin
git switch -c review-bootstrap origin/k1/a01-bootstrap
```

Sonra README'nin kurulum ve test komutlarını çalıştırırlar. K2 maskeleri ve renk sözlüğünü; K3 ret/null ve LOCKED koşullarını inceler. Gerçek bulgularını yorum yazarlar. Sorun varsa K1 aynı branch'ta düzeltip push eder. Onay sonrası uygun merge yöntemiyle main'e alınır.

## 6 Diğer üyeler kendi katkı branchlarını açar

Bootstrap PR main'e birleşmeden bu aşamaya geçmeyin. Her üye önce git status ile yerel değişikliklerini kontrol eder. Temiz çalışma ağacında:

```powershell
git switch main
git pull --ff-only origin main
```

Kişi 2:

```powershell
git switch -c k2/a01-color-contract
```

Gerçek görev: docs/contracts.md içinde maskenin tam ROI boyutunda olmasını örnekle açıklayın; test_contracts.py içine boş candidates listesinin geçerli olduğunu ve yinelenen renk adayının reddedildiğini denetleyen test ekleyin. Testi çalıştırıp kendi inceleme notunu/AI kaydını yazın. Sonra:

```powershell
git add docs/contracts.md tests/test_contracts.py YapayZeka.md
git commit -m "test: clarify color evidence edge cases"
git push -u origin k2/a01-color-contract
```

Kişi 3:

```powershell
git switch -c k3/a01-decision-contract
```

Gerçek görev: docs/contracts.md içinde sıfır ohm tek bantlı parçanın mevcut dört bant kapsamının dışında olduğunu ve REJECT'in null taşıdığını açıklayın. Testlerde nedensiz REJECT ile geçersiz stable_duration_ms için denetim ekleyin. Testi çalıştırıp kendi inceleme notunu/AI kaydını yazın. Sonra:

```powershell
git add docs/contracts.md tests/test_contracts.py YapayZeka.md
git commit -m "test: clarify rejection and scan duration rules"
git push -u origin k3/a01-decision-contract
```

K2 PR'ını K3, K3 PR'ını K1 inceler. Bu iki iş aynı dosyalara değdiğinden önce K2'yi birleştirmek basittir. K3 kendi dalında git fetch origin ve git merge origin/main yaparak K2'nin değişikliklerini alır; gerekirse çakışmayı iki katkıyı da koruyarak çözer, test eder ve git push yapar. Sonra kendi PR'ı birleşir. Boş PR/commit açmayın; gerçek değişiklik gerekir.

## 7 Aşama 1 bitişi

Üç bilgisayarda kurulum/test geçmeli, üç kişi sözleşmeyi açıklayabilmeli ve PR incelemeleri görünür olmalı. Kuralları docs/team-agreement.md içindeki listeyle kontrol edin. Sonraki iş her seferinde güncel main'den yeni branch'ta açılır. Şu an final-v1 etiketi oluşturulmaz.
