import SwiftUI

struct TwoColumnGridView: View {
    // Массив имён изображений из Assets
    let imageNames = ["на речке", "пикник1", "лебеди", "алтай", "трейлер", "монополия"]
    
    // Настройка двух гибких столбцов одинаковой ширины
    let columns = [
        GridItem(.flexible(), spacing: 25),
        GridItem(.flexible(), spacing: 25)
    ]
    
    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 16) {
                ForEach(imageNames, id: \.self) { name in VStack(spacing: 4) {
                    Image(name)
                        .resizable()
                        .scaledToFill()       // сохраняет пропорции, не растягивает
                        .frame(width: 185, height: 185) // квадрат, размер задаёте сами
                        .clipped()           // обрезает лишнее, если изображение выходит за границы (опционально)
                        .cornerRadius(10)    // для красоты (можно убрать)
                    Text(name)
                        .font(.caption)
                        .lineLimit(1)
                        .frame(maxWidth: .infinity, alignment: .leading)
                    }
                }
            }
            .padding(.horizontal, 20)
        }
    }
}
/*
struct TwoColumnGridView_Previews: PreviewProvider {
    static var previews: some View {
        TwoColumnGridView()
    }
}*/


struct ContentView: View {
    var body: some View {
        VStack(spacing: 20) {
            Text("FEED OF MOMENTS")
                .font(.largeTitle)
                .fontWeight(.bold)
        }
        .padding()
    }
}

#Preview {
    ContentView()
    TwoColumnGridView()
}
