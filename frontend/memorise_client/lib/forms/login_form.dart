import 'package:flutter/material.dart';
import 'package:memorise_client/screens/book_screen.dart'; // Import the book page widget

class LoginForm extends StatefulWidget {
  @override
  _LoginFormState createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: [
          TextFormField(
            // Username field
          ),
          TextFormField(
            // Password field
          ),
          ElevatedButton(
            onPressed: () {
              if (_formKey.currentState!.validate()) {
                // Perform authentication logic
                final String username = ''; // Get the username
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(
                    builder: (context) => BookGridView(username: username), // Pass the username to the book page
                  ),
                );
              }
            },
            child: Text('Login'),
          ),
        ],
      ),
    );
  }
}