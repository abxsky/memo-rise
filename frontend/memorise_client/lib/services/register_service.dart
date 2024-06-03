import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:memorise_client/models/user_model.dart';

class AuthService {
  final String baseUrl = 'http://localhost:8000/auth/';

  Future<void> registerUser(User user) async {
    final response = await http.post(
      Uri.parse('${baseUrl}users/'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(user.toJson()),
    );

    if (response.statusCode != 201) {
      throw Exception('Failed to register user');
    }
  }
}