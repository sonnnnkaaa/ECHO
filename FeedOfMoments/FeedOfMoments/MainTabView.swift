import SwiftUI

struct MainTabView: View {
    @State private var selected = 0

    var body: some View {
        ZStack(alignment: .bottom) {
            TabView(selection: $selected) {
                FeedView()
                    .tag(0)
                FeedView() // placeholder for explore
                    .tag(1)
                ProfileView()
                    .tag(2)
            }
            .tabViewStyle(.page(indexDisplayMode: .never))

            // Custom Bottom Nav
            CustomTabBar(selected: $selected)
        }
        .ignoresSafeArea(edges: .bottom)
    }
}

struct CustomTabBar: View {
    @Binding var selected: Int

    private let items: [(icon: String, tag: Int)] = [
        ("house.fill", 0),
        ("magnifyingglass", 1),
        ("person.fill", 2),
    ]

    var body: some View {
        HStack {
            ForEach(items, id: \.tag) { item in
                Spacer()
                Button {
                    withAnimation(.easeInOut(duration: 0.15)) { selected = item.tag }
                } label: {
                    Image(systemName: item.icon)
                        .font(.system(size: 22, weight: selected == item.tag ? .bold : .regular))
                        .foregroundColor(selected == item.tag ? AppColor.textPrimary : AppColor.textMuted)
                        .frame(width: 48, height: 48)
                        .scaleEffect(selected == item.tag ? 1.1 : 1.0)
                        .animation(.spring(response: 0.3, dampingFraction: 0.6), value: selected)
                }
                Spacer()
            }
        }
        .frame(height: 56)
        .background(
            AppColor.background
                .shadow(color: .black.opacity(0.06), radius: 0, x: 0, y: -1)
        )
        .overlay(alignment: .top) {
            Divider().opacity(0.3)
        }
        .padding(.bottom, 24) // safe area
    }
}
