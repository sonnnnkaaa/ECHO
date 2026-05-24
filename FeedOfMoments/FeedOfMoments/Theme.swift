import SwiftUI
import UIKit

enum AppColor {
    static let background    = Color(hex: "F0EDE4")
    static let blue          = Color(hex: "C8DCE8")
    static let yellow        = Color(hex: "F0E49A")
    static let cardBlue      = Color(hex: "D8E8F0")
    static let cardYellow    = Color(hex: "FAEEA0")
    static let red           = Color(hex: "C0392B")
    static let textPrimary   = Color(hex: "1A1A1A")
    static let textMuted     = Color(hex: "888888")
    static let white         = Color.white
}

extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: .alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let r = Double((int >> 16) & 0xFF) / 255
        let g = Double((int >> 8) & 0xFF) / 255
        let b = Double(int & 0xFF) / 255
        self.init(red: r, green: g, blue: b)
    }
}

// Rounded corner helper
extension View {
    func cornerRadius(_ radius: CGFloat, corners: UIRectCorner) -> some View {
        clipShape(RoundedCorner(radius: radius, corners: corners))
    }
}

struct RoundedCorner: Shape {
    var radius: CGFloat
    var corners: UIRectCorner

    func path(in rect: CGRect) -> Path {
        let path = UIBezierPath(
            roundedRect: rect,
            byRoundingCorners: corners,
            cornerRadii: CGSize(width: radius, height: radius)
        )
        return Path(path.cgPath)
    }
}
