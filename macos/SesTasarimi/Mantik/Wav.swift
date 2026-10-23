import AVFoundation
import Foundation

/// 16 bit PCM mono WAV okuma/yazma. Motor 48 kHz PCM16 mono yazar; satırlar örnek örnek birleştirilir (ses işlenmez).
/// 16-bit PCM mono WAV I/O. The engine writes 48 kHz PCM16 mono; lines are concatenated sample by sample.
enum Wav {
    struct Ses {
        var ornekler: [Int16]
        var oran: Int
        var saniye: Double { Double(ornekler.count) / Double(oran) }
    }

    /// RIFF INFO etiketleri (ASCII): INAM başlık, ICMT açıklama, ISFT yazılım.
    struct Etiket {
        var baslik: String
        var aciklama: String
        var yazilim = "SesTasarimi (macOS) / voxcpm2-turkce-ses-tasarimi"

        static let okuma = Etiket(baslik: "synthetic speech (AI-generated)",
                                  aciklama: "AI-generated synthetic speech (VoxCPM2 voice design)")
        static let klon = Etiket(baslik: "synthetic speech (AI-generated)",
                                 aciklama: "AI-generated synthetic speech (VoxCPM2 voice cloning)")
    }

    // MARK: - Okuma

    static func oku(_ url: URL) throws -> Ses {
        let veri = try Data(contentsOf: url)
        func u32(_ o: Int) -> Int { Int(veri[o]) | Int(veri[o + 1]) << 8 | Int(veri[o + 2]) << 16 | Int(veri[o + 3]) << 24 }
        func u16(_ o: Int) -> Int { Int(veri[o]) | Int(veri[o + 1]) << 8 }
        guard veri.count >= 12, veri.prefix(4) == Data("RIFF".utf8), veri[8..<12] == Data("WAVE".utf8) else {
            throw SesHatasi("WAV değil: \(url.lastPathComponent)")
        }
        var o = 12
        var oran = 0, kanal = 0, bit = 0, bicim = 0
        while o + 8 <= veri.count {
            let kimlik = String(decoding: veri[o..<o + 4], as: UTF8.self)
            let boy = u32(o + 4)
            let govde = o + 8
            if kimlik == "fmt " {
                bicim = u16(govde); kanal = u16(govde + 2); oran = u32(govde + 4); bit = u16(govde + 14)
            } else if kimlik == "data" {
                guard bicim == 1, kanal == 1, bit == 16 else {
                    throw SesHatasi("beklenmeyen WAV biçimi (biçim \(bicim), \(kanal) kanal, \(bit) bit): \(url.lastPathComponent)")
                }
                let son = min(govde + boy, veri.count)
                let sayi = (son - govde) / 2
                var ornekler = [Int16](repeating: 0, count: sayi)
                _ = ornekler.withUnsafeMutableBytes { veri.copyBytes(to: $0, from: govde..<govde + sayi * 2) }
                return Ses(ornekler: ornekler.map { Int16(littleEndian: $0) }, oran: oran)
            }
            o = govde + boy + (boy & 1)
        }
        throw SesHatasi("WAV veri bölümü yok: \(url.lastPathComponent)")
    }

    // MARK: - Yazma

    static func yaz(_ ses: Ses, _ url: URL, etiket: Etiket? = nil) throws {
        var govde = Data()
        func ekle32(_ v: Int, _ d: inout Data) { withUnsafeBytes(of: UInt32(v).littleEndian) { d.append(contentsOf: $0) } }
        func ekle16(_ v: Int, _ d: inout Data) { withUnsafeBytes(of: UInt16(v).littleEndian) { d.append(contentsOf: $0) } }

        govde.append(contentsOf: Array("WAVE".utf8))
        govde.append(contentsOf: Array("fmt ".utf8)); ekle32(16, &govde)
        ekle16(1, &govde); ekle16(1, &govde); ekle32(ses.oran, &govde); ekle32(ses.oran * 2, &govde)
        ekle16(2, &govde); ekle16(16, &govde)
        if let etiket {
            var info = Data(Array("INFO".utf8))
            for (kimlik, metin) in [("INAM", etiket.baslik), ("ICMT", etiket.aciklama), ("ISFT", etiket.yazilim)] {
                var bayt = Array(metin.unicodeScalars.map { $0.isASCII ? UInt8($0.value) : UInt8(ascii: "?") })
                bayt.append(0)
                info.append(contentsOf: Array(kimlik.utf8)); ekle32(bayt.count, &info)
                info.append(contentsOf: bayt)
                if bayt.count & 1 == 1 { info.append(0) }
            }
            govde.append(contentsOf: Array("LIST".utf8)); ekle32(info.count, &govde); govde.append(info)
        }
        govde.append(contentsOf: Array("data".utf8)); ekle32(ses.ornekler.count * 2, &govde)
        ses.ornekler.map(\.littleEndian).withUnsafeBytes { govde.append(contentsOf: $0) }

        var dosya = Data(Array("RIFF".utf8)); ekle32(govde.count, &dosya); dosya.append(govde)
        try FileManager.default.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)
        let gecici = url.deletingPathExtension().appendingPathExtension("tmp.wav")
        try dosya.write(to: gecici)
        _ = try FileManager.default.replaceItemAt(url, withItemAt: gecici)
    }

    // MARK: - Birleştirme

    static func sessizlik(_ saniye: Double, oran: Int = Motor.ornekleme) -> [Int16] {
        [Int16](repeating: 0, count: Int(saniye * Double(oran)))
    }

    /// Satırları aralarına durak koyarak birleştirir (ses işlenmez). / Concatenate with pauses, no processing.
    static func birlestir(_ sesler: [[Int16]], duraklar: [Double]) -> [Int16] {
        var sonuc: [Int16] = []
        for (sira, ses) in sesler.enumerated() {
            if sira > 0 { sonuc += sessizlik(duraklar[sira - 1]) }
            sonuc += ses
        }
        return sonuc
    }

    // MARK: - Başka biçimler (FLAC, MP3, M4A, AIFF, WAV) → mono PCM16 WAV

    /// Hazır seslerin FLAC referansı: 16 bit FLAC kayıpsız Int16 olarak okunur.
    static func pcm16eCevir(_ kaynak: URL, hedef: URL, enCokSaniye: Double? = nil) throws -> (saniye: Double, ozgunSaniye: Double) {
        let dosya: AVAudioFile
        do {
            dosya = try AVAudioFile(forReading: kaynak, commonFormat: .pcmFormatFloat32, interleaved: false)
        } catch {
            throw SesHatasi("ses dosyası okunamadı; wav, mp3, flac, m4a ya da aiff olmalı (could not decode): \(kaynak.lastPathComponent)")
        }
        let oran = Int(dosya.processingFormat.sampleRate)
        let toplam = Int(dosya.length)
        let alinacak = enCokSaniye.map { min(toplam, Int($0 * Double(oran))) } ?? toplam
        let kanal = Int(dosya.processingFormat.channelCount)
        var ornekler = [Int16]()
        ornekler.reserveCapacity(alinacak)
        if alinacak > 0 {
            // tek kanalda Int16 okunur (16 bit kaynakta birebir); çok kanallıda kanalların ortalaması için float okunur.
            if kanal == 1, let int16 = try? AVAudioFile(forReading: kaynak, commonFormat: .pcmFormatInt16, interleaved: true) {
                let tampon = AVAudioPCMBuffer(pcmFormat: int16.processingFormat, frameCapacity: AVAudioFrameCount(alinacak))!
                try int16.read(into: tampon, frameCount: AVAudioFrameCount(alinacak))
                ornekler = Array(UnsafeBufferPointer(start: tampon.int16ChannelData![0], count: Int(tampon.frameLength)))
            } else {
                let tampon = AVAudioPCMBuffer(pcmFormat: dosya.processingFormat, frameCapacity: AVAudioFrameCount(alinacak))!
                try dosya.read(into: tampon, frameCount: AVAudioFrameCount(alinacak))
                let n = Int(tampon.frameLength)
                for i in 0..<n {
                    var toplamDeger: Float = 0
                    for k in 0..<kanal { toplamDeger += tampon.floatChannelData![k][i] }
                    let ortalama = max(-1, min(1, toplamDeger / Float(kanal)))
                    ornekler.append(Int16((ortalama * 32767).rounded()))
                }
            }
        }
        try yaz(Ses(ornekler: ornekler, oran: oran), hedef)
        return (Double(ornekler.count) / Double(oran), Double(toplam) / Double(oran))
    }
}
