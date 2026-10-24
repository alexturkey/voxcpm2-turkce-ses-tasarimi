import Foundation
import IOKit

/// GPU'nun kullandığı bellek: IOAccelerator `PerformanceStatistics` → "In use system memory" (birleşik bellek,
/// `ioreg -r -d 1 -c IOAccelerator` ile aynı değer, sudo gerekmez). Windows'taki nvidia-smi'nin karşılığı.
/// GPU memory in use, the same value `ioreg` shows; the counterpart of nvidia-smi on Windows.
enum GPUBellek {
    static func istatistik() -> [String: Any]? {
        var yineleyici: io_iterator_t = 0
        guard IOServiceGetMatchingServices(kIOMainPortDefault, IOServiceMatching("IOAccelerator"), &yineleyici) == KERN_SUCCESS
        else { return nil }
        defer { IOObjectRelease(yineleyici) }
        while case let kayit = IOIteratorNext(yineleyici), kayit != 0 {
            defer { IOObjectRelease(kayit) }
            if let deger = IORegistryEntryCreateCFProperty(kayit, "PerformanceStatistics" as CFString, kCFAllocatorDefault, 0)?
                .takeRetainedValue() as? [String: Any] {
                return deger
            }
        }
        return nil
    }

    static func kullanilanMB() -> Int? {
        (istatistik()?["In use system memory"] as? Int).map { $0 / (1024 * 1024) }
    }
}
