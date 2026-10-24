# Yerel ses içe aktarma

`POST /api/aktar`, `Content-Type: application/json`; yalnız yerel arayüz.
Gövde: `ad` (boş olmayan metin, en fazla 100 karakter), `metin` (kaydın birebir
dökümü, en fazla 5000 karakter), `kayit` (WAV/FLAC dosyasının base64 içeriği).
Dosya en fazla 16 MiB, JSON gövdesi en fazla 24 MiB olabilir. Kayıt süresi
8–35 saniyedir. Tarayıcıdaki oynatıcı yüklemeden önce dinlemeye izin verir.

Başarı: HTTP 201, `{"kimlik":"kendi_sesim/1"}`. Bu kimlik `/api/oku` isteğinin
`ses` alanında kullanılır ve `/api/sesler` listesinin `tasarlanan` grubunda görünür.
Hatalar JSON `hata` alanıyla döner: 400 geçersiz alan, base64 veya kayıt;
413 boyut sınırı; 415 yanlış içerik türü; 403 izin verilmeyen Host veya Origin.
İçe aktarma GPU işi başlatmaz. Kayıtlar yerel, Git dışında tutulan `sesler/`
klasöründe saklanır. Yalnızca kendi veya açıkça izinli kayıtları kullanın.
