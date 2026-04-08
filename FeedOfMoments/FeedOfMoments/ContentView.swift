import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack(spacing: 20) {
            Text("Привет, мир! 🌍")
                .font(.largeTitle)
                .fontWeight(.bold)
                .foregroundColor(.blue)
            
            Text("Я сделала своё первое приложение!")
                .font(.title3)
                .foregroundColor(.green)
            
            Image(systemName: "heart.fill")
                .resizable()
                .frame(width: 100, height: 100)
                .foregroundColor(.red)
        }
        .padding()
    }
}

#Preview {
    ContentView()
}
