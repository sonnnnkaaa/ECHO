import Foundation

enum APIError: Error, LocalizedError {
    case invalidURL
    case unauthorized
    case serverError(Int)
    case decodingError(Error)
    case networkError(Error)
    case unknown

    var errorDescription: String? {
        switch self {
        case .invalidURL: return "Неверный URL"
        case .unauthorized: return "Необходима авторизация"
        case .serverError(let code): return "Ошибка сервера: \(code)"
        case .decodingError(let e): return "Ошибка данных: \(e.localizedDescription)"
        case .networkError(let e): return "Ошибка сети: \(e.localizedDescription)"
        case .unknown: return "Неизвестная ошибка"
        }
    }
}

final class APIService {
    static let shared = APIService()

    private let baseURL = "http://10.10.2.116:8000"
    private let session = URLSession.shared

    // MARK: - Token Management
    var accessToken: String? {
        get { UserDefaults.standard.string(forKey: "access_token") }
        set { UserDefaults.standard.set(newValue, forKey: "access_token") }
    }

    private func makeURL(_ path: String) throws -> URL {
        guard let url = URL(string: baseURL + path) else { throw APIError.invalidURL }
        return url
    }

    private func authorizedRequest(_ url: URL, method: String = "GET") -> URLRequest {
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        if let token = accessToken {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }
        return request
    }

    private func perform<T: Decodable>(_ request: URLRequest) async throws -> T {
        do {
            let (data, response) = try await session.data(for: request)
            guard let http = response as? HTTPURLResponse else { throw APIError.unknown }
            switch http.statusCode {
            case 200...299:
                do {
                    let decoder = JSONDecoder()
                    return try decoder.decode(T.self, from: data)
                } catch {
                    throw APIError.decodingError(error)
                }
            case 401:
                throw APIError.unauthorized
            default:
                throw APIError.serverError(http.statusCode)
            }
        } catch let error as APIError {
            throw error
        } catch {
            throw APIError.networkError(error)
        }
    }

    // MARK: - Auth
    func login(username: String, password: String) async throws -> TokenResponse {
        let url = try makeURL("/auth/login")
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        // OAuth2PasswordRequestForm — form-encoded
        request.setValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")
        let body = "username=\(username)&password=\(password)"
        request.httpBody = body.data(using: .utf8)
        return try await perform(request)
    }

    // MARK: - User
    func getCurrentUser() async throws -> User {
        let url = try makeURL("/users/me")
        let request = authorizedRequest(url)
        return try await perform(request)
    }

    // MARK: - Posts
    func getPosts(page: Int = 1, size: Int = 20) async throws -> PaginatedPosts {
        let url = try makeURL("/posts?page=\(page)&size=\(size)")
        let request = authorizedRequest(url)
        return try await perform(request)
    }

    func getUserPosts(userId: Int, page: Int = 1) async throws -> PaginatedPosts {
        let url = try makeURL("/posts?user_id=\(userId)&page=\(page)&size=20")
        let request = authorizedRequest(url)
        return try await perform(request)
    }

    func likePost(postId: Int) async throws {
        let url = try makeURL("/likes/post/\(postId)")
        var request = authorizedRequest(url, method: "POST")
        request.httpBody = Data()
        let _: [String: Bool] = try await perform(request)
    }

    // MARK: - Checklists
    func getUserChecklists() async throws -> [Checklist] {
        let url = try makeURL("/checklists/me")
        let request = authorizedRequest(url)
        return try await perform(request)
    }

    func getChecklistItems(checklistId: Int) async throws -> [ChecklistItem] {
        let url = try makeURL("/checklist-items?checklist_id=\(checklistId)")
        let request = authorizedRequest(url)
        return try await perform(request)
    }

    // MARK: - Favorites
    func addFavorite(postId: Int) async throws {
        let url = try makeURL("/favorites/\(postId)")
        var request = authorizedRequest(url, method: "POST")
        request.httpBody = Data()
        let _: [String: Bool] = try await perform(request)
    }
}
