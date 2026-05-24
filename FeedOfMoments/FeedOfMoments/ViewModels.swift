import Foundation
import SwiftUI
import Combine

// MARK: - AuthViewModel
@MainActor
final class AuthViewModel: ObservableObject {
    @Published var isLoggedIn = false
    @Published var isLoading = false
    @Published var errorMessage: String?

    private let api = APIService.shared

    init() {
        isLoggedIn = api.accessToken != nil
    }

    func login(username: String, password: String) async {
        isLoading = true
        errorMessage = nil
        do {
            let tokens = try await api.login(username: username, password: password)
            api.accessToken = tokens.accessToken
            isLoggedIn = true
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }

    func logout() {
        api.accessToken = nil
        isLoggedIn = false
    }
}

// MARK: - ProfileViewModel
@MainActor
final class ProfileViewModel: ObservableObject {
    @Published var user: User?
    @Published var posts: [Post] = []
    @Published var checklistItems: [ChecklistItem] = []
    @Published var isLoading = false
    @Published var errorMessage: String?

    private let api = APIService.shared

    func loadProfile() async {
        isLoading = true
        do {
            async let userTask = api.getCurrentUser()
            let user = try await userTask
            self.user = user

            let paginatedPosts = try await api.getUserPosts(userId: user.id)
            self.posts = paginatedPosts.posts

            let checklists = try await api.getUserChecklists()
            var allItems: [ChecklistItem] = []
            for checklist in checklists {
                let items = try await api.getChecklistItems(checklistId: checklist.id)
                allItems.append(contentsOf: items)
            }
            self.checklistItems = allItems
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }

    func likePost(_ postId: Int) async {
        do {
            try await api.likePost(postId: postId)
            // optimistic update
            if let idx = posts.firstIndex(where: { $0.id == postId }) {
                let p = posts[idx]
                // SwiftUI structs are immutable — rebuild
                posts[idx] = Post(
                    id: p.id, title: p.title, imageURL: p.imageURL,
                    createdAt: p.createdAt,
                    likesCount: p.isLiked ? p.likesCount - 1 : p.likesCount + 1,
                    isLiked: !p.isLiked
                )
            }
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}

// MARK: - FeedViewModel
@MainActor
final class FeedViewModel: ObservableObject {
    @Published var posts: [Post] = []
    @Published var isLoading = false
    @Published var searchText = ""
    @Published var currentPage = 1
    @Published var hasNext = false

    private let api = APIService.shared

    var filteredPosts: [Post] {
        guard !searchText.isEmpty else { return posts }
        return posts.filter { $0.title.localizedCaseInsensitiveContains(searchText) }
    }

    func loadFeed() async {
        isLoading = true
        do {
            let result = try await api.getPosts(page: 1)
            posts = result.posts
            hasNext = result.hasNext
            currentPage = 1
        } catch {
            print("Feed error: \(error)")
        }
        isLoading = false
    }

    func loadMore() async {
        guard hasNext else { return }
        do {
            let result = try await api.getPosts(page: currentPage + 1)
            posts.append(contentsOf: result.posts)
            hasNext = result.hasNext
            currentPage += 1
        } catch {
            print("Load more error: \(error)")
        }
    }
}
