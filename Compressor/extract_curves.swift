import Foundation

// Extracts one representative attack + release gain-reduction curve from a
// .slrun archive (binary plist) and writes them as compact JSON, since the
// batch's lightweight per-point JSON summaries deliberately stripped the
// raw per-sample traces to avoid 175MB+ files (see CompressorBatchCapture.swift).

let args = CommandLine.arguments
guard args.count >= 3 else {
    FileHandle.standardError.write("usage: extract_curves <path.slrun> <label>\n".data(using: .utf8)!)
    exit(1)
}
let path = args[1]
let label = args[2]

let data = try! Data(contentsOf: URL(fileURLWithPath: path))
var format = PropertyListSerialization.PropertyListFormat.binary
let plist = try! PropertyListSerialization.propertyList(from: data, options: [], format: &format) as! [String: Any]
let observations = plist["observations"] as! [[String: Any]]

// A single observation's gainReduction trace spans the WHOLE test-point
// capture (multiple bursts/repetitions), not just one isolated transition
// -- taking the array's first sample as "time zero" can land on a silent
// gap between bursts instead of the actual attack/release edge, producing
// a flat/meaningless curve. Use the trace's own precomputed marker time
// (attackMarkerTimeSeconds/releaseMarkerTimeSeconds -- exactly the onset
// CompressorTraceAnalyzer already found) as the reference instead, and
// window a fixed span around it.
func bestCurve(family: String, windowBeforeSeconds: Double, windowAfterSeconds: Double) -> [[String: Double]]? {
    let markerKey = family == "attack" ? "attackMarkerTimeSeconds" : "releaseMarkerTimeSeconds"
    // Rank by (fit quality, then transition depth) rather than fit alone --
    // a well-fit but near-silent point (e.g. a low-level interaction step)
    // produces a technically-clean but visually meaningless flat curve.
    var best: (fit: Double, depth: Double, samples: [[String: Double]])? = nil
    for obs in observations {
        guard let testPoint = obs["testPoint"] as? [String: Any],
              testPoint["family"] as? String == family,
              let traceResult = obs["traceResult"] as? [String: Any],
              let curve = traceResult[family] as? [String: Any],
              let fit = curve["singleExponentialFit"] as? Double, fit >= 0.7,
              let marker = traceResult[markerKey] as? Double,
              let gainReduction = traceResult["gainReduction"] as? [[String: Any]]
        else { continue }
        let windowed = gainReduction.compactMap { sample -> (Double, Double)? in
            guard let t = sample["timeSeconds"] as? Double, let db = sample["gainReductionDB"] as? Double else { return nil }
            let rel = t - marker
            guard rel >= -windowBeforeSeconds, rel <= windowAfterSeconds else { return nil }
            return (rel, db)
        }
        guard windowed.count > 10 else { continue }
        let depth = (windowed.map(\.1).max() ?? 0) - (windowed.map(\.1).min() ?? 0)
        if best == nil || depth > best!.depth {
            best = (fit, depth, windowed.map { ["t": $0.0, "db": $0.1] })
        }
    }
    return best?.samples
}

var result: [String: Any] = ["label": label]
if let attack = bestCurve(family: "attack", windowBeforeSeconds: 0.02, windowAfterSeconds: 0.3) { result["attack"] = attack }
if let release = bestCurve(family: "release", windowBeforeSeconds: 0.05, windowAfterSeconds: 1.0) { result["release"] = release }

let outData = try! JSONSerialization.data(withJSONObject: result)
let outPath = "/private/tmp/claude-501/-Users-richard-Developer-sysex-MotifEditorApp/62f30f13-0da7-4fc3-a41f-bb6173284061/scratchpad/curve_\(label).json"
try! outData.write(to: URL(fileURLWithPath: outPath))
print("wrote \(outPath) (attack=\(result["attack"] != nil), release=\(result["release"] != nil))")
