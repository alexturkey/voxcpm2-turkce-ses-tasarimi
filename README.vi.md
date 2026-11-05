[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · **Tiếng Việt** · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**Thiết kế giọng nói tiếng Thổ Nhĩ Kỳ với VoxCPM2 trên GPU 4 GB.** Bạn mô tả một giọng nói bằng tiếng Anh, để mô hình
tạo ra giọng đó, chọn biến thể mình thích, rồi dùng giọng ấy đọc bất kỳ văn bản tiếng Thổ Nhĩ Kỳ nào. Dự án gồm một
trình cài đặt chỉ cần một lệnh, engine [audio.cpp](https://github.com/0xShug0/audio.cpp) đã vá để chạy vừa trên GTX
1050 Ti (4 GB), một giao diện web cục bộ nhỏ gọn và mười bốn giọng tổng hợp có sẵn: bảy giọng tiếng Thổ Nhĩ Kỳ và bảy
người dẫn chuyện bản ngữ tiếng Anh, Pháp, Đức, Tây Ban Nha, Nga, Trung và Nhật.

- Ứng dụng đọc được 30 ngôn ngữ; giao diện cũng có 30 ngôn ngữ.
- 14 giọng có sẵn: 7 giọng tiếng Thổ Nhĩ Kỳ, cộng thêm mỗi thứ tiếng một giọng: Anh, Pháp, Đức, Tây Ban Nha, Nga, Trung và Nhật.
- Giao diện web (v0.2.0): mỗi thẻ biến thể có hai giọng, giọng thiết kế thô và giọng bạn sẽ luôn nghe; danh sách
  đọc kèm menu giọng; đổi tên, ẩn hoặc xóa giọng; bản nháp cho các văn bản bạn đọc. Xem "Giao diện web" trong phần "Sử dụng".

[Cách chạy vừa 4 GB](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [Hướng dẫn cài đặt cho AI agent](AGENTS.md) · [Sử dụng có trách nhiệm](ETHICS.md)

> Các giọng đi kèm là giọng tổng hợp, được thiết kế từ một đoạn mô tả bằng văn bản. Phần nhân bản giọng chỉ dành cho
> giọng của chính bạn hoặc giọng đã được chủ sở hữu cho phép rõ ràng; giao diện sẽ yêu cầu bạn xác nhận sự cho phép đó.
> Nghiêm cấm mạo danh, lừa đảo và gây hiểu lầm. Hãy ghi rõ nội dung bạn tạo ra là do AI tạo. Xem [ETHICS.md](ETHICS.md).

## 30 ngôn ngữ

Chúng tôi đã làm một video tài liệu về Cappadocia bằng 8 ngôn ngữ: Thổ Nhĩ Kỳ, Anh, Pháp, Đức, Tây Ban Nha, Nga, Trung
và Nhật. Mỗi ngôn ngữ có **người dẫn chuyện bản ngữ** riêng, được thiết kế bằng VoxCPM2 từ một đoạn mô tả tiếng Anh.
Toàn bộ được tạo hoàn toàn cục bộ trên một GTX 1050 Ti 4 GB, với cùng một mức chất lượng cố định (16 bước, cfg 2.0).
Bảy người dẫn chuyện được kèm sẵn ở đây, cùng với prompt, văn bản thiết kế, seed và bản ghi tham chiếu của họ.

| Mã | Ngôn ngữ | Giọng | Nghe | Video |
|---|---|---|---|---|
| `tr` | Tiếng Thổ Nhĩ Kỳ | `hazir/belgesel_hanim` (và 6 giọng khác) | [mẫu](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | Tiếng Anh | `hazir/anlatici_en` | [mẫu](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791986763440439) |
| `fr` | Tiếng Pháp | `hazir/anlatici_fr` | [mẫu](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [video](https://x.com/i/status/2113790681575804962) |
| `de` | Tiếng Đức | `hazir/anlatici_de` | [mẫu](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791351645262249) |
| `es` | Tiếng Tây Ban Nha | `hazir/anlatici_es` | [mẫu](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [video](https://x.com/i/status/2113807365611122705) |
| `ru` | Tiếng Nga | `hazir/anlatici_ru` | [mẫu](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [video](https://x.com/i/status/2113801574136848884) |
| `zh` | Tiếng Trung (Quan thoại) | `hazir/anlatici_zh` | [mẫu](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [video](https://x.com/i/status/2113802229606121794) |
| `ja` | Tiếng Nhật | `hazir/anlatici_ja` | [mẫu](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [video](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**Vì sao đọc từng câu một.** VoxCPM2 không ổn định khi tạo một lần một đoạn dài (khoảng trên 30 giây): nhịp đọc nhanh
dần và giọng có thể bị lệch. Ở đây giọng được giữ nhờ một bản ghi tham chiếu và seed cố định, còn văn bản dài được đọc
mỗi dòng một câu, nên âm sắc và phong cách giữ nguyên từ câu đầu đến câu cuối. Với các ngôn ngữ khác tiếng Thổ Nhĩ Kỳ,
từ điển phát âm tiếng Thổ Nhĩ Kỳ không được áp dụng. Cả 30 ngôn ngữ mà VoxCPM2 hỗ trợ đều đã được thử và hoạt động; với
những ngôn ngữ chưa có giọng đi kèm, hãy dùng `--dil <code>`. Lệnh cho từng ngôn ngữ và những bài học chúng tôi rút ra:
[docs/cok_dilli.md](docs/cok_dilli.md). Skill Claude Code cho toàn bộ quy trình thiết kế:
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**144 prompt mẫu để bắt đầu.** 18 vai (người dẫn chuyện phim tài liệu, phát thanh viên tin tức, giọng quảng cáo, sách
nói, bà kể chuyện, người dẫn podcast, giáo viên, trailer phim, hướng dẫn thiền, bình luận viên thể thao và nhiều vai
khác, cả nam lẫn nữ) cho mỗi ngôn ngữ trong 8 ngôn ngữ. Prompt viết bằng tiếng Anh, nêu quốc tịch và giọng bản ngữ của
người nói; đi kèm là văn bản được đọc trong lúc tạo giọng, viết bằng chính ngôn ngữ đó và hợp với vai. Chọn một prompt,
nghe các biến thể, giữ lại cái bạn thích: `python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`, hoặc
chọn *Mô tả mẫu* trong giao diện web. Danh sách đầy đủ: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**Lồng tiếng video bằng giọng của chính bạn.** [DubWorld](https://github.com/alexturkey/dubworld) là chương trình lồng
tiếng video chạy cục bộ của chúng tôi; nó cài repo này làm engine giọng VoxCPM2. Giọng bạn thiết kế ở đây được dùng bên
đó với `ses.voxcpm2_ses = "<name>/<variant>"`.

## Bắt đầu nhanh (Windows, 3 bước)

1. **Tải** mã nguồn: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   Gói engine dựng sẵn cho card của bạn sẽ được trình cài đặt tải ở bước 3:
   NVIDIA → [gói CUDA](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [gói Vulkan, thử nghiệm](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (đã tải sẵn một gói? thêm `-HazirZip <path to the zip>` vào lệnh bên dưới).
2. **Giải nén** file zip, mở thư mục `voxcpm2-turkce-ses-tasarimi-main`, gõ `powershell` vào thanh địa chỉ của
   Explorer và nhấn Enter.
3. **Chạy** trình cài đặt (cần Python 3.10-3.13 bản 64-bit; driver NVIDIA ≥ 570 cho CUDA), rồi nhấp đúp vào **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: thêm `-Vulkan` vào cuối. Giao diện mở tại http://127.0.0.1:8765/.

File zip engine không phải là ứng dụng độc lập (file exe của nó cần mô hình và các DLL do trình cài đặt thiết lập).
Chi tiết, danh sách GPU và các lỗi thường gặp: xem "Cài đặt nhanh" bên dưới.

## Ubuntu / Linux (NVIDIA CUDA, thử nghiệm)

Build engine đã vá bằng `bash scripts/kur-linux.sh`, hoặc dùng `Dockerfile.linux` để build và chạy trong môi trường
Ubuntu 24.04 / CUDA 12.8.1. Cần GPU NVIDIA và driver tương thích; trình cài đặt native còn cần CUDA toolkit và Python
3.10-3.13. Giao diện chỉ lắng nghe trên loopback, kể cả trên máy chủ từ xa (chuyển tiếp qua SSH). Yêu cầu, lệnh, cách
chọn kiến trúc và phạm vi kiểm chứng: [docs/linux.md](docs/linux.md).

## Bắt đầu nhanh (macOS, Apple Silicon)

Cần Xcode Command Line Tools (`xcode-select --install`) và [Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
Trình cài đặt tải mô hình, build engine đã vá với Metal (~1 phút) và thiết lập mọi thứ trong `~/vox`. Sau đó nhấp đúp
vào **`baslat.command`**. Trên MacBook Air M4 16 GB: ~2 giây tính toán cho 1 giây giọng nói, cùng seed cho ra âm thanh
giống hệt từng byte, RAM đỉnh ~5,3 GB, không bị chậm do nhiệt sau 12 phút đọc liên tục. Chi tiết và số đo:
[docs/mac.md](docs/mac.md).

**Ứng dụng Mac native (không cần Python, Homebrew hay Terminal):** [macos/README.md](macos/README.md). Ứng dụng đóng gói
cùng engine đã vá và tải mô hình ở lần mở đầu tiên; hiện tại cần build từ mã nguồn bằng Xcode.

## Dành cho người dùng Mac (Apple Silicon)

Ngoài ra còn có một bản chuyển thể độc lập do cộng đồng làm cho Mac Apple Silicon, chạy VoxCPM2 bằng framework MLX của
Apple: **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
Bản này do Emre Koç ([@emre-koc](https://github.com/emre-koc)) phát triển và duy trì trong repo riêng của anh ấy, không
phải ở đây; các bước cài đặt và câu hỏi hỗ trợ xin gửi bên đó. Cảm ơn Emre đã đưa dự án này lên Mac!

## Cách hoạt động

1. **Thiết kế giọng.** Một *mô tả giọng* bằng tiếng Anh + một *văn bản được đọc trong lúc tạo giọng* (bằng ngôn ngữ của
   giọng) + số lượng biến thể. Mỗi biến thể có seed riêng; engine nhận `(description)text` và trả về một bản ghi thiết
   kế cho mỗi seed. Văn bản là một mẫu ngắn để làm quen với giọng: 1-3 câu, tối đa ~30 giây (giao diện hiển thị thời
   lượng ước tính và sẽ không chạy nếu vượt 33 giây); văn bản dài thuộc về bước 2.
2. **Đọc dựa trên tham chiếu.** Bản ghi thiết kế được đưa vào **cả hai** đầu vào của engine (`audio` và `voice_ref`),
   cùng với bản chép lời của nó (`reference_text`) và văn bản mới cần đọc, với cùng seed. Giọng được giữ bởi bản ghi,
   không phải bởi đoạn mô tả, nên không bị lệch giữa các văn bản. Văn bản được đọc từng câu một.
3. Chất lượng cố định: 16 bước diffusion, CFG 2.0. Seed không phải là nút chỉnh chất lượng.
4. **Thời điểm từng từ, cùng một âm thanh mỗi lần chạy.** Khi đọc, chính engine cho biết mỗi từ bắt đầu và kết thúc ở đâu (bản vá 0002, không cần mô hình thêm). Thời gian được ghi vào `kelimeler.json`, và các dòng được cắt để khoảng lặng giữa hai dòng bằng thiết lập khoảng nghỉ. Độ chính xác so với forced alignment bằng CTC (CTC = 100%): 89,66% (tiếng Thổ Nhĩ Kỳ, 12 giọng; thiết lập `kelime_zamani`, bật mặc định). Với bản vá 0003, cùng một seed cho âm thanh giống hệt từng byte ở mỗi lần chạy.

Bản ghi thiết kế thô là một mẫu giọng chỉ có một lần; không lần đọc nào sau đó nghe giống hệt nó. Thứ bạn nghe trong
mọi lần đọc sau là bước 2: bản ghi thiết kế làm tham chiếu cộng với seed riêng của biến thể. Vì vậy giao diện web thực
hiện bước 2 ngay sau khi thiết kế và hiển thị cả hai trên thẻ biến thể.

Engine là audio.cpp v0.7.2 kèm bản vá của chúng tôi (`patches/`), mô hình là VoxCPM2 Q8_0 GGUF. VRAM đỉnh ≈ 2,8 GB;
khoảng 2 giây tính toán cho 1 giây giọng nói trên GTX 1050 Ti. Chi tiết và số đo: [docs/4gb.md](docs/4gb.md).

## Giọng đi kèm (`hazir_sesler/`)

Cả mười bốn giọng đều được thiết kế từ các prompt lưu trong `ses.json` của chúng; không giọng nào được nhân bản từ bản
ghi (nhân bản là tab *Nhân bản giọng* riêng, có bước xác nhận sự cho phép).

| Giọng | Mô tả ngắn | Nghe |
|---|---|---|
| `belgesel_hanim` | Phụ nữ trưởng thành ngoài năm mươi, giọng alto trầm ấm; người dẫn chuyện phim tài liệu điềm tĩnh | [mẫu](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [tham chiếu](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Giọng nam dẫn chuyện trầm, mạnh mẽ, bí ẩn | [mẫu](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [tham chiếu](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Phát thanh viên tin tức dày dạn khoảng bảy mươi tuổi, điềm tĩnh và uy tín | [mẫu](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [tham chiếu](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Nữ phát thanh viên bản tin tối ngoài ba mươi, cuốn hút, giọng mượt như nhung và giàu biểu cảm | [mẫu](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [tham chiếu](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Phù thủy trong truyện cổ tích: giọng thấp, hơi giọng mũi, ngọt ngào ranh mãnh | [mẫu](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [tham chiếu](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Giọng nam dẫn chuyện cực kỳ trầm, dày và đầy uy lực | [mẫu](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [tham chiếu](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Ông lão thông thái, giọng trầm vang, hơi bí ẩn | [mẫu](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [tham chiếu](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | Nam dẫn chuyện phim tài liệu bản ngữ tiếng Anh ngoài năm mươi (General American); trầm, điềm tĩnh, ấm áp | [mẫu](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [tham chiếu](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | Nam dẫn chuyện phim tài liệu bản ngữ tiếng Pháp ngoài năm mươi (giọng Paris); trầm, điềm tĩnh, ấm áp | [mẫu](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [tham chiếu](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | Nam dẫn chuyện phim tài liệu bản ngữ tiếng Đức ngoài năm mươi (Hochdeutsch); trầm, điềm tĩnh, ấm áp | [mẫu](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [tham chiếu](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | Nam dẫn chuyện phim tài liệu bản ngữ tiếng Tây Ban Nha ngoài năm mươi (Castilla (Madrid)); trầm, điềm tĩnh, ấm áp | [mẫu](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [tham chiếu](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | Nam dẫn chuyện phim tài liệu bản ngữ tiếng Nga ngoài năm mươi (Moskva); trầm, điềm tĩnh, ấm áp | [mẫu](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [tham chiếu](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | Nam dẫn chuyện phim tài liệu bản ngữ tiếng Trung (Quan thoại) ngoài năm mươi (Phổ thông thoại Bắc Kinh); trầm, điềm tĩnh, ấm áp | [mẫu](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [tham chiếu](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | Nam dẫn chuyện phim tài liệu bản ngữ tiếng Nhật ngoài năm mươi (chuẩn Tokyo); trầm, điềm tĩnh, ấm áp | [mẫu](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [tham chiếu](hazir_sesler/anlatici_ja/referans.flac) |

Mỗi thư mục gồm: `referans.flac` (bản ghi thiết kế không nén mất dữ liệu), `ses.json` (prompt, bản chép lời, seed thiết
kế, seed đọc, mô tả; `dil` = ngôn ngữ của các người dẫn chuyện), `ornek_okuma.mp3` (+ văn bản của nó). Dùng trực tiếp:
`--ses hazir/<name>`. Bản ghi tham chiếu của các người dẫn chuyện khá ngắn (5,6-10 giây); bản mẫu của họ là ba câu đầu
tiên của kịch bản Cappadocia, cắt ra từ bản đọc hoàn chỉnh khi sản xuất.

## Cài đặt nhanh, không cần trình biên dịch (Windows 10/11, GPU NVIDIA ≥ 4 GB)

Yêu cầu: driver NVIDIA ≥ 570 và Python 3.10-3.13 bản 64-bit (`winget install Python.Python.3.12`). Không cần gì khác:
không Visual Studio, không trình cài đặt CUDA. Không chắc mình có card nào? Chạy `nvidia-smi` trong PowerShell: lệnh này
in ra tên GPU, phiên bản driver và dung lượng bộ nhớ. Không có card NVIDIA? Xem mục "AMD / Intel" bên dưới.

Với [Git](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Không có Git: trên trang này bấm **Code → Download ZIP**, giải nén, mở thư mục `voxcpm2-turkce-ses-tasarimi-main` vừa
giải nén, gõ `powershell` vào thanh địa chỉ của Explorer và nhấn Enter, rồi chạy dòng cuối ở trên. Chỉ cần Git khi
build từ mã nguồn.

`-ExecutionPolicy Bypass` chỉ áp dụng cho đúng tiến trình này và không thay đổi thiết lập hệ thống nào; hãy đọc
`scripts\kur.ps1` trước khi chạy, như với mọi script cài đặt khác. Một lệnh, ~10 phút, tải ~3,7 GB, mọi thứ đều được
kiểm tra sha256: mô hình (2,95 GB), các DLL runtime CUDA 12.8 dưới dạng zip portable (không cài vào hệ thống, không
động đến PATH), **engine dựng sẵn** từ trang Releases, một `.venv` với hai gói Python, `ayarlar.json`, và bước kiểm
tra GPU cuối cùng (`KONTROL_OK`). Nếu có lỗi, cứ chạy lại; các file đã kiểm tra sẽ được bỏ qua. Sau đó khởi động giao
diện web: nhấp đúp vào **`baslat.bat`** trong thư mục repo. Nó khởi động giao diện và mở **http://127.0.0.1:8765/**
trong trình duyệt khi đã sẵn sàng; đóng cửa sổ đen (hoặc nhấn Ctrl+C trong đó) để dừng. Cách tương tự từ PowerShell:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
rồi tự mở **http://127.0.0.1:8765/** (khởi động theo cách này thì giao diện không tự mở trình duyệt; nó chỉ lắng nghe
trên localhost).

> **File `audiocpp_cli.exe` trong zip release không dùng để nhấp đúp.** Đây là engine dòng lệnh, cần các DLL CUDA và
> mô hình nằm cạnh nó; `kur.ps1` sắp xếp mọi thứ vào đúng chỗ và gói Python sẽ điều khiển nó. Nhấp đúp vào nó chỉ hiện
> thông báo "cudart64_12.dll not found".

**GPU được hỗ trợ (release v0.1.1):** mã native cho GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx
(sm_89) và RTX 50xx (sm_120a); mọi GPU CUDA khác từ Pascal trở lên chạy PTX nhúng sẵn thông qua driver (lần khởi động
đầu chậm hơn). Maxwell (GTX 9xx) và cũ hơn không được CUDA 12.8 hỗ trợ. Chúng tôi đã thử trên GTX 1050 Ti 4 GB (cả qua Docker Desktop/WSL2 trên Windows, chỉ CLI); @mslmyilmaz5 đã đo (#15): RTX 3060 Ti 8 GB, Ubuntu 24.04 Docker,
CUDA 12.8.1 (chi tiết trong [docs/linux.md](docs/linux.md)). Rất hoan nghênh báo cáo từ các card khác trong [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**AMD / Intel (thử nghiệm):** một zip engine Vulkan riêng (`...-win64-vulkan.zip`, không có CUDA) được cài bằng
`scripts\kur.ps1 -Kok C:\vox -Vulkan`. Bản này mới chỉ được kiểm chứng trên card NVIDIA của chúng tôi qua backend
Vulkan (ở đó nó chạy chậm hơn CUDA nhưng cho ra cùng âm thanh với cùng seed; phép đo này được thực hiện khi ổ đĩa đang
bận với một tác vụ khác, nên vẫn còn chờ một phép so sánh tốc độ sạch) và chúng tôi **chưa** tự thử trên phần cứng AMD
hay Intel: nếu bạn thử, hãy đăng kết quả trong Discussions. Khi có nhiều hơn một thiết bị Vulkan (tích hợp + rời),
trình cài đặt ghi chỉ số của GPU rời vào `ayarlar.json` dưới khóa `cihaz`.

*Lưu ý: Hỗ trợ Vulkan hiện đang ở giai đoạn thử nghiệm. Nó đã được build và thử nghiệm thành công trên GTX 1050 Ti.
Một người dùng bên ngoài (mitra_tr) cũng đã báo cáo chạy được trên AMD 6900 XT. Vẫn cần thử nghiệm rộng hơn trên các
card AMD/Intel.*

**Thử nghiệm cộng đồng (AMD):** @mitraTR đã chạy v0.1.1 với Vulkan trên AMD Radeon RX 6900 XT trong Windows 11: cài đặt, thiết kế giọng, đọc, giao diện web và các bài kiểm thử đều chạy tốt; việc đọc mất khoảng 0,8-0,9 giây tính toán cho mỗi 1 giây lời nói ([báo cáo trong #6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655)). Hãy cài vào một thư mục ngắn mà đường dẫn chỉ có ký tự ASCII (ví dụ `C:\vox`): trên Windows, bộ máy không mở được đường dẫn có chữ có dấu hay ký tự ngoài ASCII khác. Tất cả báo cáo đến nay: [phần cứng đã kiểm thử](docs/donanim_testleri.md).

**Lưu ý về Vulkan:** hiện tại, mốc thời gian của từng từ chỉ có trên NVIDIA (CUDA) và Mac; trên AMD/Intel sẽ chưa có cho đến khi động cơ Vulkan được cập nhật (việc đọc vẫn hoạt động). Lần khởi động đầu tiên trên Vulkan có thể mất vài phút vì shader của GPU được biên dịch; các lần đọc sau sẽ nhanh hơn.

### Cách khác: build engine từ mã nguồn

Cần Visual Studio 2022 Build Tools với "Desktop development with C++" (gồm cả C++ CMake tools), ~7 GB. Sau đó:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
Lệnh này còn tải nvcc, lấy mã nguồn audio.cpp v0.7.2, áp dụng `patches/0001-voxcpm2-4gb-ve-hiz.patch` và build cho
GPU của bạn (`-Mimari native`, mặc định; hoặc ví dụ `-Mimari 61`), ~15-25 phút. Hãy giữ thư mục gốc ngắn (`C:\vox`):
nvcc lỗi với đường dẫn dài. Hướng dẫn từng bước kèm kiểm tra: [AGENTS.md](AGENTS.md).

### Lỗi cài đặt thường gặp

| Bạn thấy | Ý nghĩa, cách xử lý |
|---|---|
| `cudart64_12.dll not found` sau khi nhấp đúp vào exe | Engine không dùng để khởi động bằng tay. Chạy lệnh `kur.ps1` ở trên, rồi khởi động giao diện web. |
| `64-bit Python 3.10+ bulunamadı` (không tìm thấy Python) | Cài Python (`winget install Python.Python.3.12`), đóng PowerShell, mở cửa sổ mới và chạy lại đúng lệnh đó. |
| `motor ekran kartını görmedi` (engine không thấy GPU) | Cập nhật driver NVIDIA lên 570 hoặc mới hơn; kiểm tra xem `nvidia-smi` có chạy không. |
| `indirme başarısız` / `sha256 tutmadı` (tải thất bại / sai checksum) | Thường do tải bị ngắt giữa chừng. Chạy lại đúng lệnh đó; các file đã kiểm tra sẽ được bỏ qua. |
| Khi build: `nvcc` lỗi | Giữ thư mục cài đặt gốc ngắn (`-Kok C:\vox`). |
| Trang không mở | Khởi động giao diện bằng `baslat.bat`, hoặc tự mở http://127.0.0.1:8765/. Cổng bị chiếm? Đổi `"port"` trong `ayarlar.json`. |

Gặp vấn đề? [Discussions (Q&A)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) hoặc một
[issue cài đặt](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
kèm GPU, phiên bản Windows, lệnh đã chạy và những dòng cuối của nó.

## Sử dụng

Dòng lệnh:
```powershell
# list voices
.venv\Scripts\python.exe -m ses_tasarim.oku --liste
# read with a bundled voice (one sentence per line; blank line or "|| paragraf" = longer pause, "|| 0,8" = 0.8 s)
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/belgesel_hanim --metin @metin.txt --cikti cikti\deneme
# design a new voice: 3 variants, 3 seeds
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad deniz_feneri --cesit 3 --tarif "A calm Turkish woman ..." --metin @tanitim.txt
# read with variant 2 of it
.venv\Scripts\python.exe -m ses_tasarim.oku --ses deniz_feneri/2 --metin @metin.txt --cikti cikti\deniz
# design, then read a text with each variant's lasting voice (dinleme.wav in each variant folder)
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad deniz_feneri --cesit 3 --tarif "A calm Turkish woman ..." --metin @tanitim.txt --dinleme @metin.txt
```
Quy tắc văn bản: viết số bằng chữ, không dùng dấu ngoặc kép (công cụ từ chối chữ số và dấu ngoặc kép), mỗi dòng một
câu, ≤ 2000 ký tự mỗi dòng. Khoảng nghỉ sau một dòng: `|| bagli` 0,25 giây, `|| normal` 0,5 giây, `|| paragraf` 1
giây, `|| agir` 1,5 giây hoặc độ dài tự chọn `|| 0,8` (0-5 giây; chữ số trong dấu ngắt này được phép).
`ayarlar/okunus_sozlugu.tsv` sửa cách phát âm từ nước ngoài trong văn bản tiếng Thổ Nhĩ Kỳ. Ngôn ngữ được nhận diện
từ văn bản (chữ cái tiếng Thổ Nhĩ Kỳ, hệ chữ viết, từ thông dụng; nếu không chắc thì dùng `dil` trên thẻ giọng;
`--dil <code>` là tùy chọn). Với văn bản không phải tiếng Thổ Nhĩ Kỳ, dấu nháy đơn được phép, từ điển tiếng Thổ Nhĩ
Kỳ bị bỏ qua, chữ số vẫn bị từ chối. Nếu một lần đọc in ra `speed gate: satır [...]`, hãy nghe lại những dòng đó.

### Giao diện web

Chỉ chạy cục bộ (127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → tự mở http://127.0.0.1:8765/
(cổng khác: `--port 8800`), hoặc nhấp đúp vào `baslat.bat`. Dừng máy chủ bằng Ctrl+C. Ba tab: *Thiết kế giọng*,
*Đọc bằng giọng này*, *Nhân bản giọng*. Quy trình thông thường: *Thiết kế* → nghe các biến thể → *Thêm vào danh sách
đọc của tôi* → *Đọc bằng giọng này* → tải xuống. Hoặc chọn một giọng có sẵn từ menu giọng rồi đọc.

- **Phiên bản ở phần đầu trang.** Một dòng nhỏ, mờ `v0.2.0 · <short commit>` (có thêm `+` khi các file được theo dõi
  có thay đổi chưa commit; không có git thì chỉ hiện phiên bản), để ảnh chụp màn hình và video cho thấy đã dùng phiên
  bản nào.
- **Hai giọng trên mỗi thẻ biến thể.** Ở trên, màu xám, là *Giọng thiết kế thô*: nó chỉ được tạo một lần và không bao
  giờ ra y hệt nữa. Bên dưới, trong khung màu cam, là *↻ Đây là giọng bạn sẽ luôn nghe*: bản ghi thiết kế được đọc lại
  làm tham chiếu với seed riêng của biến thể (hiển thị trên thẻ). Đây là cách giọng nghe trong mọi lần đọc sau. Bên
  dưới nữa là *Đọc bằng giọng này* và *Thêm vào danh sách đọc của tôi*. Một lần nhấn *Thiết kế* làm cả hai việc: thiết
  kế mọi biến thể, rồi đọc văn bản của bạn bằng từng giọng lâu dài; một thanh tiến trình duy nhất đếm cả hai giai
  đoạn. Thư mục biến thể có thêm `dinleme.wav`. Nếu lần đọc đó dừng sớm, bản thiết kế vẫn được giữ và thẻ hiện một ghi chú.
- **Cửa sổ "Văn bản bạn muốn nghe".** Trong *Thiết kế giọng*, ô *↻ Văn bản bạn muốn nghe* chứa nội dung mà mỗi giọng
  lâu dài sẽ đọc (để trống thì câu mẫu được đọc). Bấm vào ô sẽ mở sổ đọc trong một cửa sổ: số dòng, menu dòng, dải
  khoảng nghỉ. *OK* ghi văn bản và các khoảng nghỉ trở lại ô; *Hủy* hoặc Esc không thay đổi gì. Tab đọc giữ văn bản riêng của nó.
- **Sổ đọc.** Mỗi dòng một câu. Bấm vào số dòng để mở menu dòng (di chuyển lên hoặc xuống, chuyển đến một vị trí, nhân
  đôi, xóa; Alt+↑/↓, Alt+Shift+↓, hoặc kéo bằng số dòng; Ctrl+Z hoàn tác cả văn bản lẫn khoảng nghỉ). Bấm vào dải mảnh
  giữa hai dòng để chọn khoảng nghỉ (bagli 0,25 · normal 0,5 · paragraf 1 · agir 1,5 giây, hoặc độ dài tự chọn 0-5
  giây bằng biểu tượng bánh răng); nhấn Enter hai lần để tạo đoạn (1 giây), và các dòng trống sẽ thành dải khoảng nghỉ.
  Khi phát kết quả, dòng đang được đọc sẽ sáng lên và được cuộn vào tầm nhìn; *▶ Nghe từ đây* trong menu dòng phát từ
  dòng đó. Văn bản và các khoảng nghỉ vẫn còn sau khi tải lại trang (bộ nhớ trình duyệt).
- **Bản nháp.** Nút *📄 Bản nháp* có ở cả hai sổ (tab đọc và cửa sổ). Lưu văn bản hiện tại kèm khoảng nghỉ thành bản
  nháp, bấm một lần để tải một bản (Ctrl+Z hoàn tác), và dùng ⋯ để ghi đè, đổi tên hoặc xóa. Bản nháp được lưu trong
  `sesler/taslaklar.json`, không bao giờ nằm trong repo.
- **Danh sách đọc và menu giọng.** Trên thẻ biến thể, *Thêm vào danh sách đọc của tôi* mở một ô nhập tên: đặt tên
  riêng cho biến thể và ✓ sẽ thêm nó. *Tên lượt tạo* vẫn được giữ trên mọi biến thể của lượt đó. Trong *Đọc bằng giọng
  này*, nút giọng (cờ + tên) mở menu giọng: *Danh sách đọc của tôi* ở trên cùng, sau đó là các giọng có sẵn kèm cờ
  (ngôn ngữ giao diện đứng đầu). Mỗi hàng có ▶ nghe (giọng lâu dài nếu có), trái tim (thêm hoặc bỏ) và ⋯; ↑/↓ và Enter
  để chọn, Esc để đóng, giọng cuối cùng được ghi nhớ. Danh sách nằm trong `sesler/okuma_listesi.json`, bên ngoài repo,
  và vẫn còn sau khi khởi động lại.
- **Quản lý giọng.** Menu ⋯ (hàng trong menu giọng hoặc thẻ biến thể) có *Đọc bằng giọng này*, thêm vào hoặc bỏ khỏi
  danh sách, *Đổi tên* (để trống tên sẽ khôi phục tên gốc; *Về tên gốc*), *Xóa* cho giọng tự thiết kế và *Ẩn* cho giọng
  có sẵn; cả hai đều hỏi lại trước. Giọng bị xóa được chuyển vào `sesler/_cop/`; việc ẩn không bao giờ động đến file
  của repo. *Giọng đã ẩn và đã xóa (N)* ở cuối menu giọng có nút *Khôi phục*. Tên tùy chỉnh và các giọng bị ẩn được
  lưu trong `sesler/yerel_katman.json`. Giọng đã đổi tên hiển thị nguồn gốc màu xám (*tên lượt tạo · biến thể N*);
  ⋯ → *Đến lượt tạo* mở bản thiết kế của nó.
- **Phím tắt và file.** Ctrl+Enter (⌘+Enter trên Mac) bắt đầu *Thiết kế* hoặc *Đọc bằng giọng này* trên tab đang mở.
  Thanh tiến trình hiển thị *đã chạy / ~tổng*, với thời gian ước tính học được từ các tác vụ trước trên máy của bạn.
  File tải xuống được đặt tên theo giọng và thời gian (`Voice_Name_2026-11-02_0152.wav`).

**Nhân bản giọng (giọng của bạn hoặc giọng đã được cho phép).** Trong tab *Nhân bản giọng* của giao diện, cung cấp bản ghi của bạn (wav/mp3/flac/ogg, nên dùng 5-30 giây giọng nói sạch; dưới 3 giây bị từ chối, trên 36 giây bị cắt bớt), bản chép lời chính xác của nó và văn bản cần đọc. Nút bấm sẽ bị vô hiệu cho đến khi bạn tích vào "Giọng này là của tôi hoặc tôi đã được chủ sở hữu cho phép rõ ràng". Bản ghi chỉ được gửi tới máy chủ cục bộ (127.0.0.1), được xử lý trong một thư mục tạm cùng với phần mã hóa tham chiếu của nó, và thư mục đó bị xóa khi tác vụ kết thúc, kể cả khi thất bại; không có gì được gửi qua mạng. Chỉ đầu ra tổng hợp được giữ lại (giao diện: `sesler/_okumalar/<job>/`, CLI: `--cikti`). Đầu ra là `klon_synthetic.wav` với nhãn "synthetic"; hãy ghi rõ là do AI tạo khi chia sẻ. CLI: `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## Câu hỏi thường gặp

**Mô hình hay engine? Cái nào là cái nào?** VoxCPM2 (OpenBMB) là *mô hình*: mạng nơ-ron 2 tỷ tham số biến văn bản
thành giọng nói. audio.cpp là *engine*: chương trình C++/CUDA chạy mô hình trên GPU của bạn (`audiocpp_cli.exe`). Bản
vá của chúng tôi thay đổi engine, không thay đổi mô hình: nó giúp VoxCPM2 vừa trong 4 GB và giúp cùng một seed luôn
cho ra cùng một âm thanh. Gói Python trong repo này chỉ chuẩn bị văn bản, gọi engine và gom các file.

**GPU nào?** Xem "GPU được hỗ trợ" ở trên: NVIDIA từ GTX 10xx trở lên, VRAM 4 GB trở lên, driver ≥ 570. Release có mã
native cho sm_61/75/86/89/120a; các card khác từ Pascal trở lên dùng PTX nhúng sẵn (lần khởi động đầu chậm hơn).
AMD/Intel: zip Vulkan thử nghiệm, `kur.ps1 -Vulkan`; một người dùng bên ngoài đã báo cáo chạy được trên AMD 6900 XT,
nhưng vẫn cần thử nghiệm rộng hơn trên AMD/Intel (xem "AMD / Intel" ở trên). Chỉ dùng CPU (`"backend": "cpu"` trong
`ayarlar.json`) vẫn chạy nhưng chậm hơn ~6× so với GTX 1050 Ti (số đo engine, 535 giây so với 94 giây cho 48 giây
giọng nói); đây không phải là cách dùng được hỗ trợ.

**Nhanh đến đâu?** Đo trên GTX 1050 Ti 4 GB (i7-7700HQ): một biến thể thiết kế (bản ghi ≈ 25 giây) mất 55 giây; đọc
≈ 2 giây tính toán cho 1 giây giọng nói (hệ số thời gian thực 1,9-2,8) sau một lần mã hóa tham chiếu ~50 giây cho mỗi
giọng (được lưu cache trên đĩa) và 10-20 giây nạp mô hình cho mỗi lô; VRAM đỉnh 2,6-2,9 GB. Card mới hơn chạy nhanh
hơn; số liệu và phương pháp: [docs/4gb.md](docs/4gb.md).

**Có nhân bản giọng được không?** Mô hình VoxCPM2 bên dưới có thể bắt chước một giọng từ bản ghi tham chiếu, và phần
nhân bản dùng khả năng đó. Chỉ dùng với giọng của chính bạn hoặc khi có sự cho phép rõ ràng của người sở hữu giọng; giao
diện sẽ yêu cầu bạn xác nhận sự cho phép đó. Thiết kế giọng không cần bản ghi nào: nó bắt đầu từ một đoạn mô tả bằng
tiếng Anh hoặc tiếng Trung, và "tham chiếu" dùng để đọc một giọng đã thiết kế chính là bản ghi thiết kế tổng hợp do mô
hình tự tạo. Nghiêm cấm mạo danh, lừa đảo và gây hiểu lầm. Xem [ETHICS.md](ETHICS.md). Hãy ghi rõ nội dung bạn đăng
là do AI tạo.

**Làm sao viết một mô tả giọng tốt?** Bằng tiếng Anh, 1-3 câu: tuổi và giới tính, âm sắc (trầm/sáng, ấm, giọng mũi,
khàn), sắc thái và vai trò (người dẫn chuyện phim tài liệu điềm tĩnh, người dẫn chương trình năng động), tốc độ (chậm,
khoan thai), và "clean studio recording, no background noise". Hãy giữ nó là một đoạn mô tả, không phải kịch bản;
không dùng dấu ngoặc đơn. Yêu cầu 3-5 biến thể rồi nghe: seed thay đổi giọng rất nhiều. Với văn bản tạo giọng, dùng
1-3 câu tự nhiên bằng ngôn ngữ của giọng, đúng tâm trạng bạn muốn (tối đa ~30 giây giọng nói). Khi đọc, mỗi dòng một
câu; tách câu dài, viết số bằng chữ.

## Đóng góp

Chưa biết bắt đầu từ đâu? Bốn issue nhỏ này là bước khởi đầu tốt:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Thử trên GPU của bạn và báo lại card, driver và thời gian chạy
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: thử bản build Vulkan thử nghiệm
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Thêm một câu vào bộ câu thử nghiệm
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Chia sẻ một giọng bạn đã thiết kế, kèm mô tả và seed

**Thử card đồ họa của bạn, gửi báo cáo:** không cần biết lập trình, chỉ cần [biểu mẫu báo cáo kiểm thử phần cứng](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml); hiện chưa có báo cáo nào từ card Intel.

Bộ câu thử nghiệm chung: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); hướng dẫn giọng thương hiệu:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); cách gửi mã: [CONTRIBUTING.md](CONTRIBUTING.md).
Lỗi cài đặt: [mẫu issue](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); câu hỏi và kết quả: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Mọi người tham gia đều tuân theo [Bộ quy tắc ứng xử](CODE_OF_CONDUCT.md): hãy tử tế, góp ý về công việc.

## Người đóng góp

- [@alexturkey](https://github.com/alexturkey): người duy trì; mã nguồn, giọng đi kèm, tài liệu
- [@cayir21](https://github.com/cayir21): hỗ trợ Metal cho macOS (Apple Silicon), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): sửa lỗi kết thúc câu (EOS) khi đọc nhiều câu trên backend CPU, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5): cài đặt CUDA thử nghiệm cho Ubuntu/Linux và hỗ trợ Docker, [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

Tên bạn cũng thuộc về nơi này: một kết quả thử nghiệm từ GPU của bạn, một câu cho bộ câu thử nghiệm, một giọng bạn đã
thiết kế, một báo cáo lỗi rõ ràng hay một pull request đều được tính là đóng góp. Cảm ơn tất cả những ai đã dùng thử
và phản hồi.

## Giấy phép và ghi công

Mã nguồn và các giọng đi kèm: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Xây dựng dựa trên VoxCPM2 (OpenBMB,
Apache-2.0), audio.cpp (ShugoAI LLC, Apache-2.0) và bản chuyển đổi GGUF của audio.cpp. Danh sách đầy đủ:
[THIRD_PARTY.md](THIRD_PARTY.md). Không liên kết với OpenBMB, ModelBest hay dự án audio.cpp.
