import 'package:flutter/material.dart';
import 'package:memorise_client/forms/login_form.dart';
import 'package:memorise_client/forms/register_form.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: Padding(
        padding: EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Center(
                child: Text(
              'memo-rise',
              style: TextStyle(fontSize: 30),
            )),
            Expanded(child: LoginForm()),
          ],
        ),
      ),
    );
  }
}
