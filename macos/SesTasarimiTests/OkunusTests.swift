import XCTest
@testable import SesTasarimi

/// `ses_tasarim/okunus.py` ile aynı davranış. / Same behaviour as the Python module.
final class OkunusTests: XCTestCase {
    let kurallar = try! Okunus.kurallariOku("""
        # yorum
        www\tdabılyu dabılyu dabılyu
        GitHub\tGit Hab
        PDF\tpe de ef
        VoxCPM\tVoks si pi em
        """)

    func testRakamVeTirnakReddedilir() {
        XCTAssertEqual(Okunus.sorunlar("Bugün 3 elma.").count, 1)
        XCTAssertEqual(Okunus.sorunlar("Ali'nin kitabı.").count, 1)
        XCTAssertEqual(Okunus.sorunlar("“Merhaba” dedi.").count, 1)
        XCTAssertTrue(Okunus.sorunlar("Bugün üç elma.").isEmpty)
        XCTAssertEqual(Okunus.sorunlar("   \n "), ["metin: boş"])
    }

    func testSatirVeDurak() throws {
        let satirlar = try Okunus.satirlar("Birinci cümle.\n\nİkinci cümle. || paragraf\r\nÜçüncü. || agir")
        XCTAssertEqual(satirlar, [.init(metin: "Birinci cümle.", durakSn: 0.35),
                                  .init(metin: "İkinci cümle.", durakSn: 1.0),
                                  .init(metin: "Üçüncü.", durakSn: 1.5)])
        XCTAssertThrowsError(try Okunus.satirlar("Bir. || uzun"))
        XCTAssertFalse(Okunus.sorunlar("Bir. || uzun").isEmpty)
    }

    func testUzunSatir() {
        XCTAssertEqual(Okunus.sorunlar(String(repeating: "a", count: 2001)).count, 1)
        XCTAssertTrue(Okunus.sorunlar(String(repeating: "a", count: 2000)).isEmpty)
    }

    func testSozlukTamKelimeVeBuyukKucuk() {
        XCTAssertEqual(Okunus.sozlukUygula("GitHUB ve github, githubcı değil.", kurallar),
                       "Git Hab ve Git Hab, githubcı değil.")
        XCTAssertEqual(Okunus.sozlukUygula("Bir PDF ve VoxCPM.", kurallar), "Bir pe de ef ve Voks si pi em.")
        XCTAssertEqual(Okunus.sozlukUygula("İstanbul www", kurallar), "İstanbul dabılyu dabılyu dabılyu")
    }

    func testTurkceKucukHarf() {
        XCTAssertEqual(Okunus.turkceKucuk("IŞIK İzmir"), "ışık izmir")
    }

    func testSozlukHatalari() {
        XCTAssertThrowsError(try Okunus.kurallariOku("a b"))
        XCTAssertThrowsError(try Okunus.kurallariOku("PDF\tx\npdf\ty"))
    }

    func testTirnakTemizligi() {
        // Python okunus.strip_quotes ile aynı: satır içi boşluk tek boşluk olur, satır sonu korunur
        XCTAssertEqual(Okunus.tirnaklariAt("  \"Merhaba\"   dünya  "), "Merhaba dünya")
        XCTAssertEqual(Okunus.tirnaklariAt("A.\n\nB."), "A.\n\nB.")
        XCTAssertEqual(Okunus.tirnaklariAt("A. \r\n  B."), "A.\nB.")
    }

    func testBosSatirCumleSiniri() throws {
        // Boş satır iki cümleyi birleştirmez (PR #10 bulgusu) / A blank line no longer merges two sentences
        XCTAssertEqual(try Okunus.satirlar(Okunus.tirnaklariAt("A.\n\nB.")).map(\.metin), ["A.", "B."])
    }

    func testKisaAdVeTasarimDenetimi() {
        XCTAssertEqual(Islemler.kisaAd("Deniz Feneri Şöförü!"), "deniz_feneri_soforu")
        XCTAssertEqual(Islemler.kisaAd("!!!"), "ses")
        XCTAssertTrue(Islemler.tasarimDenetle(ad: "a", tarif: "A calm voice (soft)", metin: "Merhaba.")
            .contains { $0.contains("parantez") })
    }

    func testKlonOnayKapisi() {
        let sorunlar = Klon.denetle(kayitMetni: "Bu benim sesimin kaydıdır.", metin: "Merhaba.", onay: false)
        XCTAssertTrue(sorunlar.contains { $0.contains("izin onayı yok") })
        XCTAssertTrue(Klon.denetle(kayitMetni: "Bu benim sesimin kaydıdır.", metin: "Merhaba.", onay: true).isEmpty)
    }

    func testIstekJSON() {
        let istek = Motor.tasarimIstegi("t_7", tarif: " Calm. ", metin: "Merhaba.", tohum: 7)
        XCTAssertEqual(istek.metin, "(Calm.)Merhaba.")
        XCTAssertEqual(istek.json["max_tokens"] as? Int, 80 + Int(Double(15) * 1.2))
        XCTAssertEqual(istek.json["num_inference_steps"] as? Int, 16)
        XCTAssertEqual(istek.json["guidance_scale"] as? Double, 2.0)
    }

    func testEOSIzleyici() throws {
        let log = FileManager.default.temporaryDirectory.appendingPathComponent("eos_\(UUID().uuidString).log")
        try """
            x voxcpm2.probe.eos_accepted_at_patch 76
            y voxcpm2.toplu_coz.deferred 1
            z voxcpm2.toplu_coz.deferred 1
            w voxcpm2.probe.eos_accepted_at_patch 9
            """.write(to: log, atomically: true, encoding: .utf8)
        var izleyici = Motor.EOSIzleyici(sayi: 3)
        izleyici.bitir(log)
        XCTAssertEqual(izleyici.tamam, [true, false, true])
    }

    func testWavGidisDonus() throws {
        let url = FileManager.default.temporaryDirectory.appendingPathComponent("t_\(UUID().uuidString).wav")
        let ses = Wav.Ses(ornekler: [0, 1, -1, 32767, -32768], oran: 48000)
        try Wav.yaz(ses, url, etiket: .okuma)
        let geri = try Wav.oku(url)
        XCTAssertEqual(geri.ornekler, ses.ornekler)
        XCTAssertEqual(geri.oran, 48000)
        let veri = try Data(contentsOf: url)
        XCTAssertNotNil(veri.range(of: Data("AI-generated synthetic speech".utf8)))
        XCTAssertEqual(Wav.birlestir([[1], [2]], duraklar: [0.0001]).count, 2 + 4)
    }
}
