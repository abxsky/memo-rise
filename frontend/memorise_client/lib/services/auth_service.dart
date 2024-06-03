import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AuthService {
  final String baseUrl = 'http://localhost:8000/auth/';

  Future<void> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('${baseUrl}jwt/create/'),
      body: jsonEncode({'username': username, 'password': password}),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      final token = jsonDecode(response.body)['access'];
      print('Token: $token');
    } else {
      throw Exception('Failed to login');
    }
  }
}

class TokenStorage {
  final _storage = const FlutterSecureStorage();

  Future<void> saveToken(String token) async {
    await _storage.write(key: 'jwt_token', value: token);
  }

  Future<String?> getToken() async {
    return await _storage.read(key: 'jwt_token');
  }

  Future<void> deleteToken() async {
    await _storage.delete(key: 'jwt_token');
  }
}

class ApiService {
  final String baseUrl = 'http://localhost:8000/';

  Future<String?> getToken() async {
    return await TokenStorage().getToken();
  }

  Future<void> fetchData() async {
    final token = await getToken();
    final response = await http.get(
      Uri.parse('${baseUrl}your_api_endpoint/'),
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      print('user loggedin');
    } else {
      print('user failed to login');
      throw Exception('Failed to fetch data');
    }
  }
}
