import SwiftUI

struct FeedView: View {
    @StateObject private var vm = FeedViewModel()

    var body: some View {
        ZStack {
            AppColor.background.ignoresSafeArea()

            VStack(spacing: 0) {
                // Search bar
                HStack {
                    TextField("Поиск", text: $vm.searchText)
                        .font(.system(size: 15))
                        .padding(.horizontal, 16)
                    Image(systemName: "magnifyingglass")
                        .foregroundColor(AppColor.textMuted)
                        .padding(.trailing, 16)
                }
                .frame(height: 48)
                .background(AppColor.white)
                .cornerRadius(50)
                .shadow(color: .black.opacity(0.07), radius: 8, y: 2)
                .padding(.horizontal, 16)
                .padding(.top, 16)
                .padding(.bottom, 12)

                if vm.isLoading && vm.posts.isEmpty {
                    Spacer()
                    ProgressView()
                    Spacer()
                } else {
                    ScrollView {
                        MasonryGrid(posts: vm.filteredPosts, onLoadMore: {
                            Task { await vm.loadMore() }
                        })
                        .padding(.horizontal, 12)
                        .padding(.bottom, 90)
                    }
                }
            }
        }
        .task { await vm.loadFeed() }
    }
}

// MARK: - Masonry Grid (2 columns)
struct MasonryGrid: View {
    let posts: [Post]
    var onLoadMore: () -> Void

    // Split into two columns
    private var leftPosts: [Post] { posts.enumerated().filter { $0.offset % 2 == 0 }.map(\.element) }
    private var rightPosts: [Post] { posts.enumerated().filter { $0.offset % 2 != 0 }.map(\.element) }

    var body: some View {
        HStack(alignment: .top, spacing: 10) {
            column(posts: leftPosts)
            column(posts: rightPosts)
        }
        .onAppear { if posts.count > 10 { onLoadMore() } }
    }

    private func column(posts: [Post]) -> some View {
        LazyVStack(spacing: 10) {
            ForEach(posts) { post in
                FeedCard(post: post)
                    .onAppear {
                        if post.id == posts.last?.id { onLoadMore() }
                    }
            }
        }
    }
}

// MARK: - Feed Card
struct FeedCard: View {
    let post: Post
    // Vary height based on id for natural masonry feel
    private var imageHeight: CGFloat { CGFloat(140 + (post.id * 37) % 100) }

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            PostImageView(urlString: post.imageURL, height: imageHeight)
                .cornerRadius(18, corners: [.topLeft, .topRight])

            HStack {
                Text(post.title)
                    .font(.system(size: 13, weight: .bold))
                    .foregroundColor(AppColor.textPrimary)
                    .lineLimit(2)
                Spacer()
                Image(systemName: post.isLiked ? "heart.fill" : "heart")
                    .font(.system(size: 15))
                    .foregroundColor(post.isLiked ? AppColor.red : AppColor.textPrimary)
            }
            .padding(.horizontal, 10)
            .padding(.vertical, 8)
        }
        .background(AppColor.white)
        .cornerRadius(18)
        .shadow(color: .black.opacity(0.07), radius: 6, y: 2)
    }
}
