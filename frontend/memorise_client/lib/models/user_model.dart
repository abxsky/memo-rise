class User {
  String username;
  String password;
  String email;
  String firstName;
  String lastName;

  User({
    required this.username,
    required this.password,
    required this.email,
    required this.firstName,
    required this.lastName,
  });

  Map<String, dynamic> toJson() {
    return {
      'username': username,
      'password': password,
      'email': email,
      'first_name': firstName,
      'last_name': lastName,
    };
  }
}