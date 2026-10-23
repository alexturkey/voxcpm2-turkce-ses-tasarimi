import AppKit
import SwiftUI

@main
enum Giris {
    static func main() {
        // komut satırı öz sınaması: SesTasarimi.app/Contents/MacOS/SesTasarimi --oz-sinama <klasör>
        if let sira = CommandLine.arguments.firstIndex(of: "--oz-sinama") {
            let klasor = CommandLine.arguments.dropFirst(sira + 1).first.map { URL(fileURLWithPath: $0) }
                ?? FileManager.default.temporaryDirectory.appendingPathComponent("ses_tasarimi_oz_sinama")
            exit(OzSinama.calistir(klasor))
        }
        SesTasarimiUygulamasi.main()
    }
}

struct SesTasarimiUygulamasi: App {
    @NSApplicationDelegateAdaptor(UygulamaTemsilcisi.self) private var temsilci
    @State private var uygulama = UygulamaDurumu()

    var body: some Scene {
        Window("Ses Tasarımı", id: "ana") {
            AnaGorunum()
                .environment(uygulama)
                .frame(minWidth: 720, minHeight: 560)
        }
        .defaultSize(width: 920, height: 900)
        .commands {
            CommandGroup(after: .appInfo) {
                Button("Veri klasörünü göster") { uygulama.klasoruGoster() }
            }
        }
    }
}

final class UygulamaTemsilcisi: NSObject, NSApplicationDelegate {
    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool { true }

    func applicationWillTerminate(_ notification: Notification) {
        // motor yetim kalmasın / do not orphan the engine
        if let surec = Motor.calisanSurec.deger, surec.isRunning {
            surec.terminate()
            surec.waitUntilExit()
        }
    }
}
