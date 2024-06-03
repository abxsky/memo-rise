import 'package:flutter/material.dart';
import 'package:memorise_client/models/book_model.dart';
import 'package:memorise_client/services/book_service.dart';

class BookGridView extends StatefulWidget {
  final String username; // Add a username property

  const BookGridView({required this.username});

  @override
  _BookGridViewState createState() => _BookGridViewState();
}

class _BookGridViewState extends State<BookGridView> {
  final BookService _bookService = BookService();
  List<Book> _books = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchBooks();
  }

  Future<void> _fetchBooks() async {
    try {
      final books = await _bookService.fetchBooks();
      setState(() {
        _books = books;
        _isLoading = false;
      });
    } catch (e) {
      print('Failed to load books: $e');
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
            'Welcome, ${widget.username}'), // Display the username in the app bar title
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : GridView.builder(
              padding: const EdgeInsets.all(10.0),
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: MediaQuery.of(context).size.width > 600 ? 4 : 2,
                childAspectRatio: 2 / 3,
                mainAxisSpacing: 10.0,
                crossAxisSpacing: 10.0,
              ),
              itemCount: _books.length,
              itemBuilder: (ctx, i) => BookItem(_books[i]),
            ),
    );
  }
}

class BookItem extends StatelessWidget {
  final Book book;

  BookItem(this.book, {super.key});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 8,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      margin: const EdgeInsets.only(top: 8),
      clipBehavior: Clip.hardEdge,
      child: InkWell(
        onTap: () {
          // Navigate to book details screen if needed
        },
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Expanded(
              child: AspectRatio(
                aspectRatio: 16 / 9, // Adjust aspect ratio as needed
                child: book.bookImage != null
                    ? Image.network(
                        book.bookImage!,
                        fit: BoxFit
                            .cover, // Stretch the image to cover the available space
                      )
                    : Container(
                        color: Colors.grey,
                        child: const Center(
                          child: Icon(
                            Icons.image,
                            size: 48,
                            color: Colors.white,
                          ),
                        ),
                      ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                book.title,
                style: const TextStyle(
                  fontSize: 15,
                  overflow: TextOverflow.ellipsis,
                  color: Colors.black,
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
