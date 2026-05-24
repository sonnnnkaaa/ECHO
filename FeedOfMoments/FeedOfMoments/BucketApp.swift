import SwiftUI

@main
struct BucketApp: App {
    @StateObject private var authVM = AuthViewModel()

    var body: some Scene {
        WindowGroup {
            /*
            if authVM.isLoggedIn {
                MainTabView()
                    .environmentObject(authVM)
            } else {
                LoginView()
                    .environmentObject(authVM)
            }*/
            MainTabView()
                .environmentObject(authVM)
        }
    }
}
