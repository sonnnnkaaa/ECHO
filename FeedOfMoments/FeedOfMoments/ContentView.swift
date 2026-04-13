import SwiftUI

struct Post: Identifiable, Codable {
    let id: UUID
    let user_id: UUID
    let item_id: UUID
    let image_url: String      // пока будет имя локального файла, потом URL
    let caption: String
    let likes_count: Int
    let comments_count: Int
    let created_at: Date
}

// 2. Мок-данные (правильные)
extension Post {
    static let mockPosts: [Post] = [
        Post(
            id: UUID(),
            user_id: UUID(),
            item_id: UUID(),
            image_url: "на речке",
            caption: "Отдых у реки. Прекрасный день на природе!",
            likes_count: 15,
            comments_count: 3,
            created_at: Calendar.current.date(byAdding: .day, value: -2, to: Date())!
        ),
        Post(
            id: UUID(),
            user_id: UUID(),
            item_id: UUID(),
            image_url: "пикник",
            caption: "Пикник с друзьями. Вкусная еда и отличная компания.",
            likes_count: 42,
            comments_count: 7,
            created_at: Calendar.current.date(byAdding: .day, value: -3, to: Date())!
        ),
        Post(
            id: UUID(),
            user_id: UUID(),
            item_id: UUID(),
            image_url: "лебеди",
            caption: "Грациозные лебеди на озере",
            likes_count: 8,
            comments_count: 1,
            created_at: Calendar.current.date(byAdding: .day, value: -7, to: Date())!
        ),
        Post(
            id: UUID(),
            user_id: UUID(),
            item_id: UUID(),
            image_url: "алтай",
            caption: "Путешествие на Алтай. Горы и чистейший воздух.",
            likes_count: 27,
            comments_count: 5,
            created_at: Calendar.current.date(byAdding: .day, value: -14, to: Date())!
        ),
        Post(
            id: UUID(),
            user_id: UUID(),
            item_id: UUID(),
            image_url: "трейлер",
            caption: "Дом на колёсах — мечта!",
            likes_count: 11,
            comments_count: 2,
            created_at: Calendar.current.date(byAdding: .day, value: -30, to: Date())!
        ),
        Post(
            id: UUID(),
            user_id: UUID(),
            item_id: UUID(),
            image_url: "монополия",
            caption: "Вечер настолок с семьёй",
            likes_count: 19,
            comments_count: 4,
            created_at: Calendar.current.date(byAdding: .day, value: -5, to: Date())!
        )
    ]
}

// 3. Сетка
struct FeedGridView: View {
    let posts = Post.mockPosts
    
    let columns = [
        GridItem(.flexible(), spacing: 25),
        GridItem(.flexible(), spacing: 25)
    ]
    
    var body: some View {
        NavigationStack {
            ScrollView {
                LazyVGrid(columns: columns, spacing: 16) {
                    ForEach(posts) { post in
                        NavigationLink(destination: PostDetailView(post: post)) {
                            VStack(spacing: 8) {
                                // Используем image_url, а не imageName
                                Image(post.image_url)
                                    .resizable()
                                    .scaledToFill()
                                    .frame(width: 185, height: 185)
                                    .clipped()
                                    .cornerRadius(10)
                                Text(post.caption)
                                    .font(.caption)
                                    .lineLimit(1)
                                    .foregroundColor(.primary)
                                    .frame(maxWidth: .infinity, alignment: .leading)
                                    .multilineTextAlignment(.leading)
                            }
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(.horizontal, 20)
            }
            .navigationTitle("Feed of Moments")
            
            
        }
    }
}

// 4. Детальный экран
struct PostDetailView: View {
    let post: Post
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Изображение
                Image(post.image_url)
                    .resizable()
                    .scaledToFit()
                    .cornerRadius(20)
                
                // Текст (caption)
                Text(post.caption)
                    .font(.title2)
                    .fontWeight(.semibold)
                // Статистика (лайки, комментарии, дата)
                HStack {
                    Label("\(post.likes_count)", systemImage: "heart")
                    Label("\(post.comments_count)", systemImage: "message")
                    Spacer()
                    /*Text(post.created_at)
                        .font(.caption)
                        .foregroundColor(.gray)*/
                }
                .font(.subheadline)
                
                // Опционально: id автора (user_id)
                Text("Автор: \(post.user_id.uuidString.prefix(8))...")
                    .font(.footnote)
                    .foregroundColor(.secondary)
                
                Spacer()
            }
            .padding()
        }
        .navigationTitle(post.image_url)
        .font(.title)
        //.navigationBarTitleDisplayMode(.inline)
    }
}







/*

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
*/
#Preview {
    //ContentView()
    //TwoColumnGridView()
    FeedGridView()
}
