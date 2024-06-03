import 'package:flutter/material.dart';
import 'package:memorise_client/forms/register_form.dart';

class RegisterScreen extends StatelessWidget {
  const RegisterScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: const Padding(
        padding: EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Center(
                child: Text(
              'memo-rise',
              style: TextStyle(fontSize: 30),
            )),
            Expanded(child: RegistrationForm()),
          ],
        ),
      ),
    );
  }
}
