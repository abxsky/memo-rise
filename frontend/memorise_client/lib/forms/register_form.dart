import 'package:flutter/material.dart';
import 'package:memorise_client/services/register_service.dart';
import 'package:memorise_client/models/user_model.dart';

class RegistrationForm extends StatefulWidget {
  const RegistrationForm({super.key});

  @override
  _RegistrationFormState createState() => _RegistrationFormState();
}

class _RegistrationFormState extends State<RegistrationForm> {
  final _formKey = GlobalKey<FormState>();
  final _user =
      User(username: '', password: '', email: '', firstName: '', lastName: '');

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Center(child: Text('Inscription')),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: SingleChildScrollView(
            child: Center(
              child: LayoutBuilder(
                builder: (context, constraints) {
                  double width = constraints.maxWidth;
                  if (width >= 600) {
                    // (PC or large tablet)
                    width = 300;
                  }
                  return SizedBox(
                    width: width,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Form(
                          key: _formKey,
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.stretch,
                            children: [
                              TextFormField(
                                decoration: const InputDecoration(
                                  labelText: "Nom d'utilisateur",
                                  border: OutlineInputBorder(),
                                ),
                                style: const TextStyle(fontSize: 16.0),
                                validator: (value) {
                                  if (value == null || value.isEmpty) {
                                    return 'Please enter a username';
                                  }
                                  return null;
                                },
                                onChanged: (value) {
                                  setState(() {
                                    _user.username = value;
                                  });
                                },
                              ),
                              const SizedBox(height: 10),
                              TextFormField(
                                decoration: const InputDecoration(
                                  labelText: 'Mot de Passe',
                                  border: OutlineInputBorder(),
                                ),
                                style: const TextStyle(fontSize: 16.0),
                                obscureText: true,
                                validator: (value) {
                                  if (value == null || value.isEmpty) {
                                    return 'Veuillez entrez un mot de pass valid';
                                  }
                                  return null;
                                },
                                onChanged: (value) {
                                  setState(() {
                                    _user.password = value;
                                  });
                                },
                              ),
                              const SizedBox(height: 10),
                              TextFormField(
                                decoration: const InputDecoration(
                                  labelText: 'Email',
                                  border: OutlineInputBorder(),
                                ),
                                style: const TextStyle(fontSize: 16.0),
                                validator: (value) {
                                  if (value == null || value.isEmpty) {
                                    return 'Veuillez entrez un email valid';
                                  }
                                  return null;
                                },
                                onChanged: (value) {
                                  setState(() {
                                    _user.email = value;
                                  });
                                },
                              ),
                              const SizedBox(height: 10),
                              TextFormField(
                                decoration: const InputDecoration(
                                  labelText: 'Prenom',
                                  border: OutlineInputBorder(),
                                ),
                                style: const TextStyle(fontSize: 16.0),
                                validator: (value) {
                                  if (value == null || value.isEmpty) {
                                    return 'Veuillez entrez un prenom valid';
                                  }
                                  return null;
                                },
                                onChanged: (value) {
                                  setState(() {
                                    _user.firstName = value;
                                  });
                                },
                              ),
                              const SizedBox(height: 10),
                              TextFormField(
                                decoration: const InputDecoration(
                                  labelText: 'Nom de famille',
                                  border: OutlineInputBorder(),
                                ),
                                style: const TextStyle(fontSize: 16.0),
                                validator: (value) {
                                  if (value == null || value.isEmpty) {
                                    return 'Veuillez entrez un prenom valid';
                                  }
                                  return null;
                                },
                                onChanged: (value) {
                                  setState(() {
                                    _user.lastName = value;
                                  });
                                },
                              ),
                              const SizedBox(height: 20),
                              ElevatedButton(
                                onPressed: () {
                                  if (_formKey.currentState!.validate()) {
                                    AuthService().registerUser(_user);
                                    Navigator.pushReplacementNamed(
                                        context, '/home');
                                    ScaffoldMessenger.of(context).showSnackBar(
                                        const SnackBar(
                                            content: Text(
                                                'Vous vous etes bien inscrit sur memo-rise')));
                                  }
                                },
                                child: const Text('M\'inscrire'),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
          ),
        ),
      ),
    );
  }
}
