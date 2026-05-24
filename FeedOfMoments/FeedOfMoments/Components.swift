import SwiftUI

// MARK: - AsyncImage Wrapper
struct PostImageView: View {
    let urlString: String?
    var height: CGFloat = 220

    var body: some View {
        Group {
            if let urlString, let url = URL(string: urlString) {
                AsyncImage(url: url) { phase in
                    switch phase {
                    case .success(let image):
                        image.resizable().scaledToFill()
                    case .failure:
                        placeholderView
                    case .empty:
                        ProgressView().frame(maxWidth: .infinity, maxHeight: .infinity)
                            .background(AppColor.blue.opacity(0.3))
                    @unknown default:
                        placeholderView
                    }
                }
            } else {
                placeholderView
            }
        }
        .frame(maxWidth: .infinity)
        .frame(height: height)
        .clipped()
    }

    private var placeholderView: some View {
        Rectangle()
            .fill(AppColor.blue.opacity(0.4))
            .overlay(Image(systemName: "photo").font(.largeTitle).foregroundColor(.white.opacity(0.6)))
    }
}

// MARK: - Like Chip
struct LikeChip: View {
    let count: Int
    let isLiked: Bool
    var action: (() -> Void)? = nil

    var body: some View {
        Button(action: { action?() }) {
            HStack(spacing: 3) {
                Image(systemName: isLiked ? "heart.fill" : "heart")
                    .font(.system(size: 12, weight: .bold))
                Text("\(count)")
                    .font(.system(size: 12, weight: .black))
            }
            .foregroundColor(isLiked ? .white : AppColor.textPrimary)
            .padding(.horizontal, 8)
            .frame(height: 30)
            .background(isLiked ? AppColor.red : Color.clear)
            .overlay(
                Capsule().stroke(isLiked ? Color.clear : AppColor.textPrimary, lineWidth: 1.5)
            )
            .clipShape(Capsule())
        }
        .buttonStyle(.plain)
    }
}

// MARK: - Avatar View
struct AvatarView: View {
    let urlString: String?
    var size: CGFloat = 52

    var body: some View {
        Group {
            if let urlString, let url = URL(string: urlString) {
                AsyncImage(url: url) { phase in
                    if case .success(let image) = phase {
                        image.resizable().scaledToFill()
                    } else {
                        defaultAvatar
                    }
                }
            } else {
                defaultAvatar
            }
        }
        .frame(width: size, height: size)
        .clipShape(Circle())
    }

    private var defaultAvatar: some View {
        Circle()
            .fill(AppColor.blue)
            .overlay(
                Image(systemName: "person.fill")
                    .font(.system(size: size * 0.45))
                    .foregroundColor(.white.opacity(0.8))
            )
    }
}

// MARK: - Action Button
struct ProfileActionButton: View {
    let icon: String
    var action: () -> Void = {}

    var body: some View {
        Button(action: action) {
            Image(systemName: icon)
                .font(.system(size: 22, weight: .light))
                .foregroundColor(AppColor.textPrimary)
                .frame(maxWidth: .infinity)
                .frame(height: 70)
                .background(AppColor.white)
                .cornerRadius(18)
                .shadow(color: .black.opacity(0.06), radius: 6, y: 2)
        }
        .buttonStyle(.plain)
    }
}

// MARK: - Post Card
struct PostCard: View {
    let post: Post
    var onLike: () -> Void = {}
    var onShare: () -> Void = {}
    var onEdit: () -> Void = {}

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            PostImageView(urlString: post.imageURL, height: 220)
                .cornerRadius(20, corners: [.topLeft, .topRight])

            VStack(alignment: .leading, spacing: 6) {
                HStack {
                    Spacer()
                    Text(formattedDate(post.createdAt))
                        .font(.system(size: 11, weight: .semibold))
                        .foregroundColor(AppColor.textMuted)
                }

                HStack {
                    Text(post.title)
                        .font(.system(size: 17, weight: .bold))
                        .foregroundColor(AppColor.textPrimary)
                    Spacer()
                    LikeChip(count: post.likesCount, isLiked: post.isLiked, action: onLike)
                    Button(action: onEdit) {
                        Image(systemName: "pencil")
                            .font(.system(size: 16))
                            .foregroundColor(AppColor.textPrimary)
                    }
                    Button(action: onShare) {
                        Image(systemName: "paperplane")
                            .font(.system(size: 16))
                            .foregroundColor(AppColor.textPrimary)
                    }
                }
            }
            .padding(.horizontal, 14)
            .padding(.top, 8)
            .padding(.bottom, 14)
        }
        .background(AppColor.cardBlue)
        .cornerRadius(20)
    }

    private func formattedDate(_ raw: String) -> String {
        let formats = ["yyyy-MM-dd'T'HH:mm:ss", "yyyy-MM-dd'T'HH:mm:ssZ", "yyyy-MM-dd"]
        let out = DateFormatter()
        out.dateFormat = "dd.MM.yyyy"
        for fmt in formats {
            let df = DateFormatter(); df.dateFormat = fmt
            if let d = df.date(from: raw) { return out.string(from: d) }
        }
        return raw
    }
}

// MARK: - Check Item Row
struct CheckItemRow: View {
    let item: ChecklistItem

    var body: some View {
        HStack {
            Image(systemName: item.isCompleted ? "checkmark.circle.fill" : "circle")
                .font(.system(size: 20))
                .foregroundColor(item.isCompleted ? AppColor.textPrimary : AppColor.textMuted)

            Text(item.name)
                .font(.system(size: 16, weight: .bold))
                .foregroundColor(AppColor.textPrimary)

            Spacer()

            VStack(alignment: .trailing, spacing: 4) {
                // date placeholder — item doesn't carry date directly
                LikeChip(count: item.likesCount, isLiked: false)
            }
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 14)
        .background(AppColor.cardYellow)
        .cornerRadius(16)
    }
}
