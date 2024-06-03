import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:memorise_client/models/book_model.dart';

class BookService {
  final String baseUrl = 'http://localhost:8000/store/books/';

  Future<List<Book>> fetchBooks() async {
    final response = await http.get(Uri.parse(baseUrl));
    if (response.statusCode == 200) {
      List<dynamic> jsonData = jsonDecode(response.body)['results'];
      return jsonData.map((json) => Book.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load books');
    }
  }
}