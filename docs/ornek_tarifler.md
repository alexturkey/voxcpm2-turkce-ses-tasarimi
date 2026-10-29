# Example voice prompts / Örnek ses tarifleri

Türkçesi aşağıda. / Turkish below.

144 ready examples: 18 roles × 8 languages (`tr en fr de es ru zh ja`). Each prompt is **English** and says the
speaker's nationality and native accent, the way we designed the Cappadocia narrators. Each example also brings its
**design text** (the text read while the voice is created), written natively in that language and matched to the
role: news text for an anchor, a fairy tale for a grandmother, a goal for a sports commentator. You only pick an
example, listen to the variants and keep the one you like. Change the prompt freely: these are starting points.

```powershell
python -m ses_tasarim.ornekler --dil de          # list the German examples
python -m ses_tasarim.tasarla --ornek de_haber_kadin --cesit 3   # 3 variants, 3 seeds
python -m ses_tasarim.oku --ses de_haber_kadin/2 --metin @text.txt --cikti cikti\de   # read with variant 2
```

Web UI: section 1, pick from *Example prompt* (all 144, grouped by language); the prompt, design text and name fill in.
Source files: `ses_tasarim/ornek_tarifler/roller.json` (English templates) and `<lang>.json` (person, accent,
design texts). A new language = one new `<lang>.json` with the same nine text types; `tests/test_ornekler.py` checks it.

**Not measured yet:** these 144 prompts are new; we tested the pattern with our 8 bundled narrators, not every
example. Some seeds give a weaker variant: design 3 variants and choose by listening to a reading of real text.

Measured once (GTX 1050 Ti 4 GB): `tasarla --ornek en_belgesel_kadin --cesit 2` filled prompt, text and language
by itself and made 2 variants with 15.2 s and 18.7 s references in 110 s, VRAM peak 2815 MB. Not judged by ear yet.

## Roles / Roller

| Role id | Type of design text | Gender | Age | Role |
|---|---|---|---|---|
| `belgesel_erkek` | belgesel | erkek | 50+ | Documentary narrator, male / Belgesel anlatıcısı, erkek |
| `belgesel_kadin` | belgesel | kadın | 50+ | Documentary narrator, female / Belgesel anlatıcısı, kadın |
| `haber_erkek` | haber | erkek | 40+ | News anchor, male / Haber spikeri, erkek |
| `haber_kadin` | haber | kadın | 30+ | News anchor, female / Haber spikeri, kadın |
| `tanitim_erkek` | tanitim | erkek | 30+ | Commercial voice-over, male / Reklam ve tanıtım sesi, erkek |
| `tanitim_kadin` | tanitim | kadın | 20+ | Commercial voice-over, female / Reklam ve tanıtım sesi, kadın |
| `sesli_kitap_kadin` | hikaye | kadın | 40+ | Audiobook narrator, female / Sesli kitap anlatıcısı, kadın |
| `sesli_kitap_erkek` | hikaye | erkek | 40+ | Audiobook narrator, male / Sesli kitap anlatıcısı, erkek |
| `masal_dede` | hikaye | erkek | 70+ | Grandfather storyteller / Masal anlatan dede |
| `masal_nine` | hikaye | kadın | 70+ | Grandmother storyteller / Masal anlatan nine |
| `podcast_erkek` | sohbet | erkek | 20+ | Podcast host, male / Podcast sunucusu, erkek |
| `vlog_kadin` | sohbet | kadın | 20+ | Vlogger, female / Vlog ve sosyal medya sesi, kadın |
| `genc_yayinci` | sohbet | erkek | 18+ | Young gaming streamer, male / Genç oyun yayıncısı, erkek |
| `ogretmen_kadin` | egitim | kadın | 40+ | Teacher, e-learning, female / Öğretmen, eğitim videosu, kadın |
| `kurumsal_erkek` | egitim | erkek | 40+ | Corporate explainer, male / Kurumsal anlatım, erkek |
| `fragman_erkek` | fragman | erkek | 40+ | Movie trailer voice, male / Film fragmanı sesi, erkek |
| `meditasyon_kadin` | meditasyon | kadın | 30+ | Meditation guide, female / Meditasyon rehberi, kadın |
| `spor_erkek` | spor | erkek | 30+ | Sports commentator, male / Spor spikeri, erkek |

## Prompts per language / Dillere göre tarifler

<details><summary><b>de</b> · Deutsch · accent: native German speaker with a clear standard Hochdeutsch accent</summary>

| Id | Prompt |
|---|---|
| `de_belgesel_erkek` | A deep-voiced German man in his fifties, native German speaker with a clear standard Hochdeutsch accent, calm, warm and soulful documentary storytelling, unhurried pace, rich resonant voice, close-mic clean studio recording, no background noise |
| `de_belgesel_kadin` | A mature German woman in her fifties with a deep, rich, warm alto voice, native German speaker with a clear standard Hochdeutsch accent, calm and wise documentary narration, slow unhurried pace, natural pauses between phrases, clean studio recording, no background noise |
| `de_haber_erkek` | A composed German man in his forties, native German speaker with a clear standard Hochdeutsch accent, a seasoned television news anchor, calm, authoritative and trustworthy, clear crisp diction, measured pace, full resonant chest voice, clean studio recording, no background noise |
| `de_haber_kadin` | A confident German woman in her thirties, native German speaker with a clear standard Hochdeutsch accent, an evening news anchor, clear, warm and authoritative voice, crisp diction, steady measured pace, clean studio recording, no background noise |
| `de_tanitim_erkek` | An energetic German man in his thirties, native German speaker with a clear standard Hochdeutsch accent, an upbeat commercial voice-over artist, bright, friendly and persuasive, lively pace with a smile in the voice, clean studio recording, no background noise |
| `de_tanitim_kadin` | A cheerful German woman in her late twenties, native German speaker with a clear standard Hochdeutsch accent, a bright and warm commercial voice-over artist, friendly, confident and inviting, lively pace with a smile in the voice, clean studio recording, no background noise |
| `de_sesli_kitap_kadin` | A gentle German woman in her forties, native German speaker with a clear standard Hochdeutsch accent, an audiobook narrator with a soft, warm and expressive voice, calm storytelling, natural pauses, intimate close-mic studio recording, no background noise |
| `de_sesli_kitap_erkek` | A thoughtful German man in his forties, native German speaker with a clear standard Hochdeutsch accent, an audiobook narrator with a smooth, warm baritone voice, expressive but calm storytelling, natural pauses, intimate close-mic studio recording, no background noise |
| `de_masal_dede` | A kind old German man in his seventies, native German speaker with a clear standard Hochdeutsch accent, a grandfather telling a fairy tale by the fire, warm, slightly husky and gentle voice, slow storytelling pace, clean recording, no background noise |
| `de_masal_nine` | A sweet old German woman in her seventies, native German speaker with a clear standard Hochdeutsch accent, a grandmother telling a bedtime story, soft, warm and tender voice, slow loving pace, clean recording, no background noise |
| `de_podcast_erkek` | A relaxed German man in his late twenties, native German speaker with a clear standard Hochdeutsch accent, a friendly podcast host, casual, natural and conversational, easy-going pace, warm close-mic recording, no background noise |
| `de_vlog_kadin` | A lively German woman in her early twenties, native German speaker with a clear standard Hochdeutsch accent, a friendly social media creator talking to her followers, natural, warm and enthusiastic, conversational pace, clean close-mic recording, no background noise |
| `de_genc_yayinci` | An excited young German man around twenty, native German speaker with a clear standard Hochdeutsch accent, a gaming streamer, youthful, playful and energetic voice, fast conversational pace, clean close-mic recording, no background noise |
| `de_ogretmen_kadin` | A patient German woman in her forties, native German speaker with a clear standard Hochdeutsch accent, a teacher explaining a lesson, clear, kind and encouraging voice, careful articulation, moderate pace, clean studio recording, no background noise |
| `de_kurumsal_erkek` | A professional German man in his forties, native German speaker with a clear standard Hochdeutsch accent, a corporate explainer narrator, clear, confident and reassuring voice, polished diction, moderate pace, clean studio recording, no background noise |
| `de_fragman_erkek` | A commanding German man with an exceptionally deep, powerful voice, native German speaker with a clear standard Hochdeutsch accent, an epic movie trailer narrator, dramatic, intense and cinematic, slow deliberate delivery with strong pauses, clean studio recording, no background noise |
| `de_meditasyon_kadin` | A calm German woman in her thirties, native German speaker with a clear standard Hochdeutsch accent, a meditation guide with a very soft, gentle and soothing voice, slow peaceful pace, long relaxed pauses, intimate clean recording, no background noise |
| `de_spor_erkek` | An excited German man in his thirties, native German speaker with a clear standard Hochdeutsch accent, a passionate sports commentator, fast, loud and thrilling delivery with rising energy, clear diction, clean studio recording, no background noise |

</details>

<details><summary><b>en</b> · English · accent: native English speaker with a natural General American accent</summary>

| Id | Prompt |
|---|---|
| `en_belgesel_erkek` | A deep-voiced American man in his fifties, native English speaker with a natural General American accent, calm, warm and soulful documentary storytelling, unhurried pace, rich resonant voice, close-mic clean studio recording, no background noise |
| `en_belgesel_kadin` | A mature American woman in her fifties with a deep, rich, warm alto voice, native English speaker with a natural General American accent, calm and wise documentary narration, slow unhurried pace, natural pauses between phrases, clean studio recording, no background noise |
| `en_haber_erkek` | A composed American man in his forties, native English speaker with a natural General American accent, a seasoned television news anchor, calm, authoritative and trustworthy, clear crisp diction, measured pace, full resonant chest voice, clean studio recording, no background noise |
| `en_haber_kadin` | A confident American woman in her thirties, native English speaker with a natural General American accent, an evening news anchor, clear, warm and authoritative voice, crisp diction, steady measured pace, clean studio recording, no background noise |
| `en_tanitim_erkek` | An energetic American man in his thirties, native English speaker with a natural General American accent, an upbeat commercial voice-over artist, bright, friendly and persuasive, lively pace with a smile in the voice, clean studio recording, no background noise |
| `en_tanitim_kadin` | A cheerful American woman in her late twenties, native English speaker with a natural General American accent, a bright and warm commercial voice-over artist, friendly, confident and inviting, lively pace with a smile in the voice, clean studio recording, no background noise |
| `en_sesli_kitap_kadin` | A gentle American woman in her forties, native English speaker with a natural General American accent, an audiobook narrator with a soft, warm and expressive voice, calm storytelling, natural pauses, intimate close-mic studio recording, no background noise |
| `en_sesli_kitap_erkek` | A thoughtful American man in his forties, native English speaker with a natural General American accent, an audiobook narrator with a smooth, warm baritone voice, expressive but calm storytelling, natural pauses, intimate close-mic studio recording, no background noise |
| `en_masal_dede` | A kind old American man in his seventies, native English speaker with a natural General American accent, a grandfather telling a fairy tale by the fire, warm, slightly husky and gentle voice, slow storytelling pace, clean recording, no background noise |
| `en_masal_nine` | A sweet old American woman in her seventies, native English speaker with a natural General American accent, a grandmother telling a bedtime story, soft, warm and tender voice, slow loving pace, clean recording, no background noise |
| `en_podcast_erkek` | A relaxed American man in his late twenties, native English speaker with a natural General American accent, a friendly podcast host, casual, natural and conversational, easy-going pace, warm close-mic recording, no background noise |
| `en_vlog_kadin` | A lively American woman in her early twenties, native English speaker with a natural General American accent, a friendly social media creator talking to her followers, natural, warm and enthusiastic, conversational pace, clean close-mic recording, no background noise |
| `en_genc_yayinci` | An excited young American man around twenty, native English speaker with a natural General American accent, a gaming streamer, youthful, playful and energetic voice, fast conversational pace, clean close-mic recording, no background noise |
| `en_ogretmen_kadin` | A patient American woman in her forties, native English speaker with a natural General American accent, a teacher explaining a lesson, clear, kind and encouraging voice, careful articulation, moderate pace, clean studio recording, no background noise |
| `en_kurumsal_erkek` | A professional American man in his forties, native English speaker with a natural General American accent, a corporate explainer narrator, clear, confident and reassuring voice, polished diction, moderate pace, clean studio recording, no background noise |
| `en_fragman_erkek` | A commanding American man with an exceptionally deep, powerful voice, native English speaker with a natural General American accent, an epic movie trailer narrator, dramatic, intense and cinematic, slow deliberate delivery with strong pauses, clean studio recording, no background noise |
| `en_meditasyon_kadin` | A calm American woman in her thirties, native English speaker with a natural General American accent, a meditation guide with a very soft, gentle and soothing voice, slow peaceful pace, long relaxed pauses, intimate clean recording, no background noise |
| `en_spor_erkek` | An excited American man in his thirties, native English speaker with a natural General American accent, a passionate sports commentator, fast, loud and thrilling delivery with rising energy, clear diction, clean studio recording, no background noise |

</details>

<details><summary><b>es</b> · Español · accent: native Spanish speaker from Madrid with a natural Castilian accent</summary>

| Id | Prompt |
|---|---|
| `es_belgesel_erkek` | A deep-voiced Spanish man in his fifties, native Spanish speaker from Madrid with a natural Castilian accent, calm, warm and soulful documentary storytelling, unhurried pace, rich resonant voice, close-mic clean studio recording, no background noise |
| `es_belgesel_kadin` | A mature Spanish woman in her fifties with a deep, rich, warm alto voice, native Spanish speaker from Madrid with a natural Castilian accent, calm and wise documentary narration, slow unhurried pace, natural pauses between phrases, clean studio recording, no background noise |
| `es_haber_erkek` | A composed Spanish man in his forties, native Spanish speaker from Madrid with a natural Castilian accent, a seasoned television news anchor, calm, authoritative and trustworthy, clear crisp diction, measured pace, full resonant chest voice, clean studio recording, no background noise |
| `es_haber_kadin` | A confident Spanish woman in her thirties, native Spanish speaker from Madrid with a natural Castilian accent, an evening news anchor, clear, warm and authoritative voice, crisp diction, steady measured pace, clean studio recording, no background noise |
| `es_tanitim_erkek` | An energetic Spanish man in his thirties, native Spanish speaker from Madrid with a natural Castilian accent, an upbeat commercial voice-over artist, bright, friendly and persuasive, lively pace with a smile in the voice, clean studio recording, no background noise |
| `es_tanitim_kadin` | A cheerful Spanish woman in her late twenties, native Spanish speaker from Madrid with a natural Castilian accent, a bright and warm commercial voice-over artist, friendly, confident and inviting, lively pace with a smile in the voice, clean studio recording, no background noise |
| `es_sesli_kitap_kadin` | A gentle Spanish woman in her forties, native Spanish speaker from Madrid with a natural Castilian accent, an audiobook narrator with a soft, warm and expressive voice, calm storytelling, natural pauses, intimate close-mic studio recording, no background noise |
| `es_sesli_kitap_erkek` | A thoughtful Spanish man in his forties, native Spanish speaker from Madrid with a natural Castilian accent, an audiobook narrator with a smooth, warm baritone voice, expressive but calm storytelling, natural pauses, intimate close-mic studio recording, no background noise |
| `es_masal_dede` | A kind old Spanish man in his seventies, native Spanish speaker from Madrid with a natural Castilian accent, a grandfather telling a fairy tale by the fire, warm, slightly husky and gentle voice, slow storytelling pace, clean recording, no background noise |
| `es_masal_nine` | A sweet old Spanish woman in her seventies, native Spanish speaker from Madrid with a natural Castilian accent, a grandmother telling a bedtime story, soft, warm and tender voice, slow loving pace, clean recording, no background noise |
| `es_podcast_erkek` | A relaxed Spanish man in his late twenties, native Spanish speaker from Madrid with a natural Castilian accent, a friendly podcast host, casual, natural and conversational, easy-going pace, warm close-mic recording, no background noise |
| `es_vlog_kadin` | A lively Spanish woman in her early twenties, native Spanish speaker from Madrid with a natural Castilian accent, a friendly social media creator talking to her followers, natural, warm and enthusiastic, conversational pace, clean close-mic recording, no background noise |
| `es_genc_yayinci` | An excited young Spanish man around twenty, native Spanish speaker from Madrid with a natural Castilian accent, a gaming streamer, youthful, playful and energetic voice, fast conversational pace, clean close-mic recording, no background noise |
| `es_ogretmen_kadin` | A patient Spanish woman in her forties, native Spanish speaker from Madrid with a natural Castilian accent, a teacher explaining a lesson, clear, kind and encouraging voice, careful articulation, moderate pace, clean studio recording, no background noise |
| `es_kurumsal_erkek` | A professional Spanish man in his forties, native Spanish speaker from Madrid with a natural Castilian accent, a corporate explainer narrator, clear, confident and reassuring voice, polished diction, moderate pace, clean studio recording, no background noise |
| `es_fragman_erkek` | A commanding Spanish man with an exceptionally deep, powerful voice, native Spanish speaker from Madrid with a natural Castilian accent, an epic movie trailer narrator, dramatic, intense and cinematic, slow deliberate delivery with strong pauses, clean studio recording, no background noise |
| `es_meditasyon_kadin` | A calm Spanish woman in her thirties, native Spanish speaker from Madrid with a natural Castilian accent, a meditation guide with a very soft, gentle and soothing voice, slow peaceful pace, long relaxed pauses, intimate clean recording, no background noise |
| `es_spor_erkek` | An excited Spanish man in his thirties, native Spanish speaker from Madrid with a natural Castilian accent, a passionate sports commentator, fast, loud and thrilling delivery with rising energy, clear diction, clean studio recording, no background noise |

</details>

<details><summary><b>fr</b> · Français · accent: native French speaker from Paris with a natural Parisian accent</summary>

| Id | Prompt |
|---|---|
| `fr_belgesel_erkek` | A deep-voiced French man in his fifties, native French speaker from Paris with a natural Parisian accent, calm, warm and soulful documentary storytelling, unhurried pace, rich resonant voice, close-mic clean studio recording, no background noise |
| `fr_belgesel_kadin` | A mature French woman in her fifties with a deep, rich, warm alto voice, native French speaker from Paris with a natural Parisian accent, calm and wise documentary narration, slow unhurried pace, natural pauses between phrases, clean studio recording, no background noise |
| `fr_haber_erkek` | A composed French man in his forties, native French speaker from Paris with a natural Parisian accent, a seasoned television news anchor, calm, authoritative and trustworthy, clear crisp diction, measured pace, full resonant chest voice, clean studio recording, no background noise |
| `fr_haber_kadin` | A confident French woman in her thirties, native French speaker from Paris with a natural Parisian accent, an evening news anchor, clear, warm and authoritative voice, crisp diction, steady measured pace, clean studio recording, no background noise |
| `fr_tanitim_erkek` | An energetic French man in his thirties, native French speaker from Paris with a natural Parisian accent, an upbeat commercial voice-over artist, bright, friendly and persuasive, lively pace with a smile in the voice, clean studio recording, no background noise |
| `fr_tanitim_kadin` | A cheerful French woman in her late twenties, native French speaker from Paris with a natural Parisian accent, a bright and warm commercial voice-over artist, friendly, confident and inviting, lively pace with a smile in the voice, clean studio recording, no background noise |
| `fr_sesli_kitap_kadin` | A gentle French woman in her forties, native French speaker from Paris with a natural Parisian accent, an audiobook narrator with a soft, warm and expressive voice, calm storytelling, natural pauses, intimate close-mic studio recording, no background noise |
| `fr_sesli_kitap_erkek` | A thoughtful French man in his forties, native French speaker from Paris with a natural Parisian accent, an audiobook narrator with a smooth, warm baritone voice, expressive but calm storytelling, natural pauses, intimate close-mic studio recording, no background noise |
| `fr_masal_dede` | A kind old French man in his seventies, native French speaker from Paris with a natural Parisian accent, a grandfather telling a fairy tale by the fire, warm, slightly husky and gentle voice, slow storytelling pace, clean recording, no background noise |
| `fr_masal_nine` | A sweet old French woman in her seventies, native French speaker from Paris with a natural Parisian accent, a grandmother telling a bedtime story, soft, warm and tender voice, slow loving pace, clean recording, no background noise |
| `fr_podcast_erkek` | A relaxed French man in his late twenties, native French speaker from Paris with a natural Parisian accent, a friendly podcast host, casual, natural and conversational, easy-going pace, warm close-mic recording, no background noise |
| `fr_vlog_kadin` | A lively French woman in her early twenties, native French speaker from Paris with a natural Parisian accent, a friendly social media creator talking to her followers, natural, warm and enthusiastic, conversational pace, clean close-mic recording, no background noise |
| `fr_genc_yayinci` | An excited young French man around twenty, native French speaker from Paris with a natural Parisian accent, a gaming streamer, youthful, playful and energetic voice, fast conversational pace, clean close-mic recording, no background noise |
| `fr_ogretmen_kadin` | A patient French woman in her forties, native French speaker from Paris with a natural Parisian accent, a teacher explaining a lesson, clear, kind and encouraging voice, careful articulation, moderate pace, clean studio recording, no background noise |
| `fr_kurumsal_erkek` | A professional French man in his forties, native French speaker from Paris with a natural Parisian accent, a corporate explainer narrator, clear, confident and reassuring voice, polished diction, moderate pace, clean studio recording, no background noise |
| `fr_fragman_erkek` | A commanding French man with an exceptionally deep, powerful voice, native French speaker from Paris with a natural Parisian accent, an epic movie trailer narrator, dramatic, intense and cinematic, slow deliberate delivery with strong pauses, clean studio recording, no background noise |
| `fr_meditasyon_kadin` | A calm French woman in her thirties, native French speaker from Paris with a natural Parisian accent, a meditation guide with a very soft, gentle and soothing voice, slow peaceful pace, long relaxed pauses, intimate clean recording, no background noise |
| `fr_spor_erkek` | An excited French man in his thirties, native French speaker from Paris with a natural Parisian accent, a passionate sports commentator, fast, loud and thrilling delivery with rising energy, clear diction, clean studio recording, no background noise |

</details>

<details><summary><b>ja</b> · 日本語 · accent: native Japanese speaker from Tokyo with standard Japanese pronunciation</summary>

| Id | Prompt |
|---|---|
| `ja_belgesel_erkek` | A deep-voiced Japanese man in his fifties, native Japanese speaker from Tokyo with standard Japanese pronunciation, calm, warm and soulful documentary storytelling, unhurried pace, rich resonant voice, close-mic clean studio recording, no background noise |
| `ja_belgesel_kadin` | A mature Japanese woman in her fifties with a deep, rich, warm alto voice, native Japanese speaker from Tokyo with standard Japanese pronunciation, calm and wise documentary narration, slow unhurried pace, natural pauses between phrases, clean studio recording, no background noise |
| `ja_haber_erkek` | A composed Japanese man in his forties, native Japanese speaker from Tokyo with standard Japanese pronunciation, a seasoned television news anchor, calm, authoritative and trustworthy, clear crisp diction, measured pace, full resonant chest voice, clean studio recording, no background noise |
| `ja_haber_kadin` | A confident Japanese woman in her thirties, native Japanese speaker from Tokyo with standard Japanese pronunciation, an evening news anchor, clear, warm and authoritative voice, crisp diction, steady measured pace, clean studio recording, no background noise |
| `ja_tanitim_erkek` | An energetic Japanese man in his thirties, native Japanese speaker from Tokyo with standard Japanese pronunciation, an upbeat commercial voice-over artist, bright, friendly and persuasive, lively pace with a smile in the voice, clean studio recording, no background noise |
| `ja_tanitim_kadin` | A cheerful Japanese woman in her late twenties, native Japanese speaker from Tokyo with standard Japanese pronunciation, a bright and warm commercial voice-over artist, friendly, confident and inviting, lively pace with a smile in the voice, clean studio recording, no background noise |
| `ja_sesli_kitap_kadin` | A gentle Japanese woman in her forties, native Japanese speaker from Tokyo with standard Japanese pronunciation, an audiobook narrator with a soft, warm and expressive voice, calm storytelling, natural pauses, intimate close-mic studio recording, no background noise |
| `ja_sesli_kitap_erkek` | A thoughtful Japanese man in his forties, native Japanese speaker from Tokyo with standard Japanese pronunciation, an audiobook narrator with a smooth, warm baritone voice, expressive but calm storytelling, natural pauses, intimate close-mic studio recording, no background noise |
| `ja_masal_dede` | A kind old Japanese man in his seventies, native Japanese speaker from Tokyo with standard Japanese pronunciation, a grandfather telling a fairy tale by the fire, warm, slightly husky and gentle voice, slow storytelling pace, clean recording, no background noise |
| `ja_masal_nine` | A sweet old Japanese woman in her seventies, native Japanese speaker from Tokyo with standard Japanese pronunciation, a grandmother telling a bedtime story, soft, warm and tender voice, slow loving pace, clean recording, no background noise |
| `ja_podcast_erkek` | A relaxed Japanese man in his late twenties, native Japanese speaker from Tokyo with standard Japanese pronunciation, a friendly podcast host, casual, natural and conversational, easy-going pace, warm close-mic recording, no background noise |
| `ja_vlog_kadin` | A lively Japanese woman in her early twenties, native Japanese speaker from Tokyo with standard Japanese pronunciation, a friendly social media creator talking to her followers, natural, warm and enthusiastic, conversational pace, clean close-mic recording, no background noise |
| `ja_genc_yayinci` | An excited young Japanese man around twenty, native Japanese speaker from Tokyo with standard Japanese pronunciation, a gaming streamer, youthful, playful and energetic voice, fast conversational pace, clean close-mic recording, no background noise |
| `ja_ogretmen_kadin` | A patient Japanese woman in her forties, native Japanese speaker from Tokyo with standard Japanese pronunciation, a teacher explaining a lesson, clear, kind and encouraging voice, careful articulation, moderate pace, clean studio recording, no background noise |
| `ja_kurumsal_erkek` | A professional Japanese man in his forties, native Japanese speaker from Tokyo with standard Japanese pronunciation, a corporate explainer narrator, clear, confident and reassuring voice, polished diction, moderate pace, clean studio recording, no background noise |
| `ja_fragman_erkek` | A commanding Japanese man with an exceptionally deep, powerful voice, native Japanese speaker from Tokyo with standard Japanese pronunciation, an epic movie trailer narrator, dramatic, intense and cinematic, slow deliberate delivery with strong pauses, clean studio recording, no background noise |
| `ja_meditasyon_kadin` | A calm Japanese woman in her thirties, native Japanese speaker from Tokyo with standard Japanese pronunciation, a meditation guide with a very soft, gentle and soothing voice, slow peaceful pace, long relaxed pauses, intimate clean recording, no background noise |
| `ja_spor_erkek` | An excited Japanese man in his thirties, native Japanese speaker from Tokyo with standard Japanese pronunciation, a passionate sports commentator, fast, loud and thrilling delivery with rising energy, clear diction, clean studio recording, no background noise |

</details>

<details><summary><b>ru</b> · Русский · accent: native Russian speaker from Moscow with a natural Russian accent</summary>

| Id | Prompt |
|---|---|
| `ru_belgesel_erkek` | A deep-voiced Russian man in his fifties, native Russian speaker from Moscow with a natural Russian accent, calm, warm and soulful documentary storytelling, unhurried pace, rich resonant voice, close-mic clean studio recording, no background noise |
| `ru_belgesel_kadin` | A mature Russian woman in her fifties with a deep, rich, warm alto voice, native Russian speaker from Moscow with a natural Russian accent, calm and wise documentary narration, slow unhurried pace, natural pauses between phrases, clean studio recording, no background noise |
| `ru_haber_erkek` | A composed Russian man in his forties, native Russian speaker from Moscow with a natural Russian accent, a seasoned television news anchor, calm, authoritative and trustworthy, clear crisp diction, measured pace, full resonant chest voice, clean studio recording, no background noise |
| `ru_haber_kadin` | A confident Russian woman in her thirties, native Russian speaker from Moscow with a natural Russian accent, an evening news anchor, clear, warm and authoritative voice, crisp diction, steady measured pace, clean studio recording, no background noise |
| `ru_tanitim_erkek` | An energetic Russian man in his thirties, native Russian speaker from Moscow with a natural Russian accent, an upbeat commercial voice-over artist, bright, friendly and persuasive, lively pace with a smile in the voice, clean studio recording, no background noise |
| `ru_tanitim_kadin` | A cheerful Russian woman in her late twenties, native Russian speaker from Moscow with a natural Russian accent, a bright and warm commercial voice-over artist, friendly, confident and inviting, lively pace with a smile in the voice, clean studio recording, no background noise |
| `ru_sesli_kitap_kadin` | A gentle Russian woman in her forties, native Russian speaker from Moscow with a natural Russian accent, an audiobook narrator with a soft, warm and expressive voice, calm storytelling, natural pauses, intimate close-mic studio recording, no background noise |
| `ru_sesli_kitap_erkek` | A thoughtful Russian man in his forties, native Russian speaker from Moscow with a natural Russian accent, an audiobook narrator with a smooth, warm baritone voice, expressive but calm storytelling, natural pauses, intimate close-mic studio recording, no background noise |
| `ru_masal_dede` | A kind old Russian man in his seventies, native Russian speaker from Moscow with a natural Russian accent, a grandfather telling a fairy tale by the fire, warm, slightly husky and gentle voice, slow storytelling pace, clean recording, no background noise |
| `ru_masal_nine` | A sweet old Russian woman in her seventies, native Russian speaker from Moscow with a natural Russian accent, a grandmother telling a bedtime story, soft, warm and tender voice, slow loving pace, clean recording, no background noise |
| `ru_podcast_erkek` | A relaxed Russian man in his late twenties, native Russian speaker from Moscow with a natural Russian accent, a friendly podcast host, casual, natural and conversational, easy-going pace, warm close-mic recording, no background noise |
| `ru_vlog_kadin` | A lively Russian woman in her early twenties, native Russian speaker from Moscow with a natural Russian accent, a friendly social media creator talking to her followers, natural, warm and enthusiastic, conversational pace, clean close-mic recording, no background noise |
| `ru_genc_yayinci` | An excited young Russian man around twenty, native Russian speaker from Moscow with a natural Russian accent, a gaming streamer, youthful, playful and energetic voice, fast conversational pace, clean close-mic recording, no background noise |
| `ru_ogretmen_kadin` | A patient Russian woman in her forties, native Russian speaker from Moscow with a natural Russian accent, a teacher explaining a lesson, clear, kind and encouraging voice, careful articulation, moderate pace, clean studio recording, no background noise |
| `ru_kurumsal_erkek` | A professional Russian man in his forties, native Russian speaker from Moscow with a natural Russian accent, a corporate explainer narrator, clear, confident and reassuring voice, polished diction, moderate pace, clean studio recording, no background noise |
| `ru_fragman_erkek` | A commanding Russian man with an exceptionally deep, powerful voice, native Russian speaker from Moscow with a natural Russian accent, an epic movie trailer narrator, dramatic, intense and cinematic, slow deliberate delivery with strong pauses, clean studio recording, no background noise |
| `ru_meditasyon_kadin` | A calm Russian woman in her thirties, native Russian speaker from Moscow with a natural Russian accent, a meditation guide with a very soft, gentle and soothing voice, slow peaceful pace, long relaxed pauses, intimate clean recording, no background noise |
| `ru_spor_erkek` | An excited Russian man in his thirties, native Russian speaker from Moscow with a natural Russian accent, a passionate sports commentator, fast, loud and thrilling delivery with rising energy, clear diction, clean studio recording, no background noise |

</details>

<details><summary><b>tr</b> · Türkçe / Turkish · accent: native Turkish speaker from Istanbul with clear standard Turkish diction</summary>

| Id | Prompt |
|---|---|
| `tr_belgesel_erkek` | A deep-voiced Turkish man in his fifties, native Turkish speaker from Istanbul with clear standard Turkish diction, calm, warm and soulful documentary storytelling, unhurried pace, rich resonant voice, close-mic clean studio recording, no background noise |
| `tr_belgesel_kadin` | A mature Turkish woman in her fifties with a deep, rich, warm alto voice, native Turkish speaker from Istanbul with clear standard Turkish diction, calm and wise documentary narration, slow unhurried pace, natural pauses between phrases, clean studio recording, no background noise |
| `tr_haber_erkek` | A composed Turkish man in his forties, native Turkish speaker from Istanbul with clear standard Turkish diction, a seasoned television news anchor, calm, authoritative and trustworthy, clear crisp diction, measured pace, full resonant chest voice, clean studio recording, no background noise |
| `tr_haber_kadin` | A confident Turkish woman in her thirties, native Turkish speaker from Istanbul with clear standard Turkish diction, an evening news anchor, clear, warm and authoritative voice, crisp diction, steady measured pace, clean studio recording, no background noise |
| `tr_tanitim_erkek` | An energetic Turkish man in his thirties, native Turkish speaker from Istanbul with clear standard Turkish diction, an upbeat commercial voice-over artist, bright, friendly and persuasive, lively pace with a smile in the voice, clean studio recording, no background noise |
| `tr_tanitim_kadin` | A cheerful Turkish woman in her late twenties, native Turkish speaker from Istanbul with clear standard Turkish diction, a bright and warm commercial voice-over artist, friendly, confident and inviting, lively pace with a smile in the voice, clean studio recording, no background noise |
| `tr_sesli_kitap_kadin` | A gentle Turkish woman in her forties, native Turkish speaker from Istanbul with clear standard Turkish diction, an audiobook narrator with a soft, warm and expressive voice, calm storytelling, natural pauses, intimate close-mic studio recording, no background noise |
| `tr_sesli_kitap_erkek` | A thoughtful Turkish man in his forties, native Turkish speaker from Istanbul with clear standard Turkish diction, an audiobook narrator with a smooth, warm baritone voice, expressive but calm storytelling, natural pauses, intimate close-mic studio recording, no background noise |
| `tr_masal_dede` | A kind old Turkish man in his seventies, native Turkish speaker from Istanbul with clear standard Turkish diction, a grandfather telling a fairy tale by the fire, warm, slightly husky and gentle voice, slow storytelling pace, clean recording, no background noise |
| `tr_masal_nine` | A sweet old Turkish woman in her seventies, native Turkish speaker from Istanbul with clear standard Turkish diction, a grandmother telling a bedtime story, soft, warm and tender voice, slow loving pace, clean recording, no background noise |
| `tr_podcast_erkek` | A relaxed Turkish man in his late twenties, native Turkish speaker from Istanbul with clear standard Turkish diction, a friendly podcast host, casual, natural and conversational, easy-going pace, warm close-mic recording, no background noise |
| `tr_vlog_kadin` | A lively Turkish woman in her early twenties, native Turkish speaker from Istanbul with clear standard Turkish diction, a friendly social media creator talking to her followers, natural, warm and enthusiastic, conversational pace, clean close-mic recording, no background noise |
| `tr_genc_yayinci` | An excited young Turkish man around twenty, native Turkish speaker from Istanbul with clear standard Turkish diction, a gaming streamer, youthful, playful and energetic voice, fast conversational pace, clean close-mic recording, no background noise |
| `tr_ogretmen_kadin` | A patient Turkish woman in her forties, native Turkish speaker from Istanbul with clear standard Turkish diction, a teacher explaining a lesson, clear, kind and encouraging voice, careful articulation, moderate pace, clean studio recording, no background noise |
| `tr_kurumsal_erkek` | A professional Turkish man in his forties, native Turkish speaker from Istanbul with clear standard Turkish diction, a corporate explainer narrator, clear, confident and reassuring voice, polished diction, moderate pace, clean studio recording, no background noise |
| `tr_fragman_erkek` | A commanding Turkish man with an exceptionally deep, powerful voice, native Turkish speaker from Istanbul with clear standard Turkish diction, an epic movie trailer narrator, dramatic, intense and cinematic, slow deliberate delivery with strong pauses, clean studio recording, no background noise |
| `tr_meditasyon_kadin` | A calm Turkish woman in her thirties, native Turkish speaker from Istanbul with clear standard Turkish diction, a meditation guide with a very soft, gentle and soothing voice, slow peaceful pace, long relaxed pauses, intimate clean recording, no background noise |
| `tr_spor_erkek` | An excited Turkish man in his thirties, native Turkish speaker from Istanbul with clear standard Turkish diction, a passionate sports commentator, fast, loud and thrilling delivery with rising energy, clear diction, clean studio recording, no background noise |

</details>

<details><summary><b>zh</b> · 中文 (普通话) · accent: native Mandarin speaker from Beijing with standard Putonghua pronunciation</summary>

| Id | Prompt |
|---|---|
| `zh_belgesel_erkek` | A deep-voiced Chinese man in his fifties, native Mandarin speaker from Beijing with standard Putonghua pronunciation, calm, warm and soulful documentary storytelling, unhurried pace, rich resonant voice, close-mic clean studio recording, no background noise |
| `zh_belgesel_kadin` | A mature Chinese woman in her fifties with a deep, rich, warm alto voice, native Mandarin speaker from Beijing with standard Putonghua pronunciation, calm and wise documentary narration, slow unhurried pace, natural pauses between phrases, clean studio recording, no background noise |
| `zh_haber_erkek` | A composed Chinese man in his forties, native Mandarin speaker from Beijing with standard Putonghua pronunciation, a seasoned television news anchor, calm, authoritative and trustworthy, clear crisp diction, measured pace, full resonant chest voice, clean studio recording, no background noise |
| `zh_haber_kadin` | A confident Chinese woman in her thirties, native Mandarin speaker from Beijing with standard Putonghua pronunciation, an evening news anchor, clear, warm and authoritative voice, crisp diction, steady measured pace, clean studio recording, no background noise |
| `zh_tanitim_erkek` | An energetic Chinese man in his thirties, native Mandarin speaker from Beijing with standard Putonghua pronunciation, an upbeat commercial voice-over artist, bright, friendly and persuasive, lively pace with a smile in the voice, clean studio recording, no background noise |
| `zh_tanitim_kadin` | A cheerful Chinese woman in her late twenties, native Mandarin speaker from Beijing with standard Putonghua pronunciation, a bright and warm commercial voice-over artist, friendly, confident and inviting, lively pace with a smile in the voice, clean studio recording, no background noise |
| `zh_sesli_kitap_kadin` | A gentle Chinese woman in her forties, native Mandarin speaker from Beijing with standard Putonghua pronunciation, an audiobook narrator with a soft, warm and expressive voice, calm storytelling, natural pauses, intimate close-mic studio recording, no background noise |
| `zh_sesli_kitap_erkek` | A thoughtful Chinese man in his forties, native Mandarin speaker from Beijing with standard Putonghua pronunciation, an audiobook narrator with a smooth, warm baritone voice, expressive but calm storytelling, natural pauses, intimate close-mic studio recording, no background noise |
| `zh_masal_dede` | A kind old Chinese man in his seventies, native Mandarin speaker from Beijing with standard Putonghua pronunciation, a grandfather telling a fairy tale by the fire, warm, slightly husky and gentle voice, slow storytelling pace, clean recording, no background noise |
| `zh_masal_nine` | A sweet old Chinese woman in her seventies, native Mandarin speaker from Beijing with standard Putonghua pronunciation, a grandmother telling a bedtime story, soft, warm and tender voice, slow loving pace, clean recording, no background noise |
| `zh_podcast_erkek` | A relaxed Chinese man in his late twenties, native Mandarin speaker from Beijing with standard Putonghua pronunciation, a friendly podcast host, casual, natural and conversational, easy-going pace, warm close-mic recording, no background noise |
| `zh_vlog_kadin` | A lively Chinese woman in her early twenties, native Mandarin speaker from Beijing with standard Putonghua pronunciation, a friendly social media creator talking to her followers, natural, warm and enthusiastic, conversational pace, clean close-mic recording, no background noise |
| `zh_genc_yayinci` | An excited young Chinese man around twenty, native Mandarin speaker from Beijing with standard Putonghua pronunciation, a gaming streamer, youthful, playful and energetic voice, fast conversational pace, clean close-mic recording, no background noise |
| `zh_ogretmen_kadin` | A patient Chinese woman in her forties, native Mandarin speaker from Beijing with standard Putonghua pronunciation, a teacher explaining a lesson, clear, kind and encouraging voice, careful articulation, moderate pace, clean studio recording, no background noise |
| `zh_kurumsal_erkek` | A professional Chinese man in his forties, native Mandarin speaker from Beijing with standard Putonghua pronunciation, a corporate explainer narrator, clear, confident and reassuring voice, polished diction, moderate pace, clean studio recording, no background noise |
| `zh_fragman_erkek` | A commanding Chinese man with an exceptionally deep, powerful voice, native Mandarin speaker from Beijing with standard Putonghua pronunciation, an epic movie trailer narrator, dramatic, intense and cinematic, slow deliberate delivery with strong pauses, clean studio recording, no background noise |
| `zh_meditasyon_kadin` | A calm Chinese woman in her thirties, native Mandarin speaker from Beijing with standard Putonghua pronunciation, a meditation guide with a very soft, gentle and soothing voice, slow peaceful pace, long relaxed pauses, intimate clean recording, no background noise |
| `zh_spor_erkek` | An excited Chinese man in his thirties, native Mandarin speaker from Beijing with standard Putonghua pronunciation, a passionate sports commentator, fast, loud and thrilling delivery with rising energy, clear diction, clean studio recording, no background noise |

</details>

---

## Türkçe

144 hazır örnek: 18 rol × 8 dil. Tarif her zaman **İngilizce**dir ve içinde konuşanın milliyeti ile yerli aksanı
geçer (Kapadokya anlatıcılarını böyle tasarladık). Her örnek, rolüne uygun ve o dilde yazılmış **tasarım metnini**
(ses yaratılırken okutulan metin) de getirir: spikere haber, nineye masal, spor spikerine gol. Örneği seç, çeşitleri
dinle, beğendiğini tut. Tarifi dilediğin gibi değiştir; bunlar başlangıç noktasıdır.

```powershell
python -m ses_tasarim.ornekler --dil tr --tam      # Türkçe örnekler, tarif ve metinleriyle
python -m ses_tasarim.tasarla --ornek tr_masal_nine --cesit 3
python -m ses_tasarim.oku --ses tr_masal_nine/1 --metin @masal.txt --cikti cikti\masal
```

Arayüz: 1. bölümde *Örnek tarif* kutusundan seç (144 tarifin hepsi, dile göre gruplu); tarif, metin ve ad kendiliğinden dolar.
**Henüz ölçülmedi:** bu 144 tarif yeni; kalıbı 8 hazır anlatıcımızla denedik, her örneği tek tek değil. Bazı tohumlar
zayıf çeşit verir: 3 çeşit tasarla, gerçek metinden okutup dinleyerek seç.

Bir kez ölçüldü (GTX 1050 Ti 4 GB): `tasarla --ornek en_belgesel_kadin --cesit 2` tarifi, metni ve dili kendisi
doldurdu; 110 sn'de 15.2 sn ve 18.7 sn referanslı 2 çeşit üretti, VRAM tepe 2815 MB. Kulakla henüz değerlendirilmedi.
