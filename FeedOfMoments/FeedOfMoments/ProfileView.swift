import SwiftUI

struct ProfileView: View {
    @StateObject private var vm = ProfileViewModel()
    @EnvironmentObject var authVM: AuthViewModel
    @State private var selectedTab: ProfileTab = .posts

    enum ProfileTab { case posts, check }

    var body: some View {
        ZStack(alignment: .bottom) {
            AppColor.background.ignoresSafeArea()

            VStack(spacing: 0) {
                // ── Header ──────────────────────────────────────
                HStack {
                    AvatarView(urlString: vm.user?.avatarURL)
                    VStack(alignment: .leading, spacing: 2) {
                        Text(vm.user?.fullName ?? vm.user?.username ?? "Загрузка...")
                            .font(.system(size: 17, weight: .black))
                        Text("@\(vm.user?.username ?? "")")
                            .font(.system(size: 13, weight: .semibold))
                            .foregroundColor(AppColor.textMuted)
                    }
                    Spacer()
                    Menu {
                        Button("Выйти", role: .destructive) { authVM.logout() }
                    } label: {
                        Image(systemName: "line.3.horizontal")
                            .font(.system(size: 22))
                            .foregroundColor(AppColor.textPrimary)
                    }
                }
                .padding(.horizontal, 20)
                .padding(.bottom, 16)

                // ── Action Buttons ───────────────────────────────
                HStack(spacing: 10) {
                    ProfileActionButton(icon: "heart")
                    ProfileActionButton(icon: "person.2")
                    ProfileActionButton(icon: "plus")
                }
                .padding(.horizontal, 20)
                .padding(.bottom, 20)

                // ── Tab Selector ─────────────────────────────────
                tabSelector

                // ── Content ──────────────────────────────────────
                TabContent(selectedTab: selectedTab, vm: vm)
            }
        }
        .task { await vm.loadProfile() }
    }

    // MARK: - Tab Selector
    private var tabSelector: some View {
        HStack(spacing: 0) {
            Button { withAnimation(.easeInOut(duration: 0.2)) { selectedTab = .posts } } label: {
                Text("POSTS")
                    .font(.system(size: 15, weight: .black))
                    .tracking(1)
                    .foregroundColor(AppColor.textPrimary)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 14)
                    .background(selectedTab == .posts ? AppColor.blue : AppColor.yellow)
                    .cornerRadius(20, corners: [.topLeft, .topRight])
            }
            .zIndex(selectedTab == .posts ? 1 : 0)

            Button { withAnimation(.easeInOut(duration: 0.2)) { selectedTab = .check } } label: {
                Text("CHECK")
                    .font(.system(size: 15, weight: .black))
                    .tracking(1)
                    .foregroundColor(AppColor.textPrimary)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 14)
                    .background(selectedTab == .check ? AppColor.yellow : AppColor.blue)
                    .cornerRadius(20, corners: [.topLeft, .topRight])
            }
            .zIndex(selectedTab == .check ? 1 : 0)
        }
        .padding(.horizontal, 16)
    }
}

// MARK: - Tab Content
private struct TabContent: View {
    let selectedTab: ProfileView.ProfileTab
    @ObservedObject var vm: ProfileViewModel

    var body: some View {
        ZStack(alignment: .top) {
            // Posts tab
            if selectedTab == .posts {
                ScrollView {
                    LazyVStack(spacing: 16) {
                        if vm.isLoading {
                            ProgressView().padding(.top, 40)
                        } else if vm.posts.isEmpty {
                            emptyState(text: "Нет постов", icon: "photo.on.rectangle")
                        } else {
                            ForEach(vm.posts) { post in
                                PostCard(post: post, onLike: {
                                    Task { await vm.likePost(post.id) }
                                })
                            }
                        }
                    }
                    .padding(16)
                    .padding(.bottom, 90)
                }
                .background(AppColor.blue)
                .cornerRadius(20, corners: [.topRight])
            }

            // Check tab
            if selectedTab == .check {
                ScrollView {
                    LazyVStack(spacing: 12) {
                        if vm.isLoading {
                            ProgressView().padding(.top, 40)
                        } else if vm.checklistItems.isEmpty {
                            emptyState(text: "Нет пунктов", icon: "checkmark.circle")
                        } else {
                            ForEach(vm.checklistItems) { item in
                                CheckItemRow(item: item)
                            }
                        }
                    }
                    .padding(16)
                    .padding(.bottom, 90)
                }
                .background(AppColor.yellow)
                .cornerRadius(20, corners: [.topLeft])
            }
        }
    }

    private func emptyState(text: String, icon: String) -> some View {
        VStack(spacing: 12) {
            Image(systemName: icon)
                .font(.system(size: 44))
                .foregroundColor(AppColor.textMuted)
            Text(text)
                .font(.system(size: 16))
                .foregroundColor(AppColor.textMuted)
        }
        .frame(maxWidth: .infinity)
        .padding(.top, 60)
    }
}
