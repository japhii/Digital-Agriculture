class UserModel {
  final String id;
  final String username;
  final String email;
  final String firstName;
  final String lastName;

  UserModel({
    required this.id,
    required this.username,
    required this.email,
    required this.firstName,
    required this.lastName,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id']?.toString() ?? '',
      username: json['username'] ?? '',
      email: json['email'] ?? '',
      firstName: json['first'] ?? '',
      lastName: json['last'] ?? '',
    );
  }
}