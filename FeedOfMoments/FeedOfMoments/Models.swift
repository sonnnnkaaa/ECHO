import Foundation

// MARK: - User
struct User: Codable, Identifiable {
    let id: Int
    let username: String
    let email: String
    let fullName: String?
    let avatarURL: String?

    enum CodingKeys: String, CodingKey {
        case id, username, email
        case fullName = "full_name"
        case avatarURL = "avatar_url"
    }
}

// MARK: - Post
struct Post: Codable, Identifiable {
    let id: Int
    let title: String
    let imageURL: String?
    let createdAt: String
    let likesCount: Int
    let isLiked: Bool

    enum CodingKeys: String, CodingKey {
        case id, title
        case imageURL = "image_url"
        case createdAt = "created_at"
        case likesCount = "likes_count"
        case isLiked = "is_liked"
    }
}

// MARK: - Checklist
struct Checklist: Codable, Identifiable {
    let id: Int
    let title: String
    let description: String?
    let items: [ChecklistItem]?
}

struct ChecklistItem: Codable, Identifiable {
    let id: Int
    let name: String
    let isCompleted: Bool
    let checklistId: Int
    let likesCount: Int

    enum CodingKeys: String, CodingKey {
        case id, name
        case isCompleted = "is_completed"
        case checklistId = "checklist_id"
        case likesCount = "likes_count"
    }
}

// MARK: - UserProgress
struct UserProgress: Codable, Identifiable {
    let id: Int
    let userId: Int
    let userName: String
    let itemId: Int
    let itemName: String
    let postId: Int
    let postURL: String
    let checklistId: Int
    let isCompleted: Bool
    let completedAt: String?

    enum CodingKeys: String, CodingKey {
        case id
        case userId = "user_id"
        case userName = "user_name"
        case itemId = "item_id"
        case itemName = "item_name"
        case postId = "post_id"
        case postURL = "post_url"
        case checklistId = "checklist_id"
        case isCompleted = "is_completed"
        case completedAt = "completed_at"
    }
}

// MARK: - Auth
struct TokenResponse: Codable {
    let accessToken: String
    let refreshToken: String
    let tokenType: String

    enum CodingKeys: String, CodingKey {
        case accessToken = "access_token"
        case refreshToken = "refresh_token"
        case tokenType = "token_type"
    }
}

struct LoginRequest: Codable {
    let username: String
    let password: String
}

// MARK: - Pagination
struct PaginatedPosts: Codable {
    let posts: [Post]
    let total: Int
    let page: Int
    let size: Int
    let hasPrev: Bool
    let hasNext: Bool

    enum CodingKeys: String, CodingKey {
        case posts, total, page, size
        case hasPrev = "has_prev"
        case hasNext = "has_next"
    }
}
