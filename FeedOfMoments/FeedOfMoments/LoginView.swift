import SwiftUI

struct LoginView: View {
    @EnvironmentObject var authVM: AuthViewModel
    @State private var username = ""
    @State private var password = ""

    var body: some View {
        ZStack {
            AppColor.background.ignoresSafeArea()

            VStack(spacing: 32) {
                Spacer()

                // Logo area
                VStack(spacing: 8) {
                    Image(systemName: "checkmark.circle.fill")
                        .font(.system(size: 64))
                        .foregroundColor(AppColor.textPrimary)
                    Text("BucketList")
                        .font(.system(size: 32, weight: .black))
                    Text("делай то, о чём мечтаешь")
                        .font(.system(size: 14))
                        .foregroundColor(AppColor.textMuted)
                }

                Spacer()

                // Fields
                VStack(spacing: 12) {
                    TextField("Имя пользователя", text: $username)
                        .padding(.horizontal, 18)
                        .frame(height: 52)
                        .background(AppColor.white)
                        .cornerRadius(16)

                    SecureField("Пароль", text: $password)
                        .padding(.horizontal, 18)
                        .frame(height: 52)
                        .background(AppColor.white)
                        .cornerRadius(16)
                }
                .padding(.horizontal, 24)

                if let error = authVM.errorMessage {
                    Text(error)
                        .font(.system(size: 13))
                        .foregroundColor(AppColor.red)
                        .multilineTextAlignment(.center)
                        .padding(.horizontal, 24)
                }

                Button {
                    Task { await authVM.login(username: username, password: password) }
                } label: {
                    Group {
                        if authVM.isLoading {
                            ProgressView().tint(.white)
                        } else {
                            Text("Войти")
                                .font(.system(size: 17, weight: .bold))
                                .foregroundColor(AppColor.textPrimary)
                        }
                    }
                    .frame(maxWidth: .infinity)
                    .frame(height: 54)
                    .background(AppColor.yellow)
                    .cornerRadius(18)
                }
                .padding(.horizontal, 24)
                .disabled(authVM.isLoading)

                Spacer()
            }
        }
    }
}
