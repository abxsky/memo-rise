class Book {
  final int id;
  final String title;
  final double unitPrice;
  final double priceWithTax;
  final int category;
  final double inventory;
  final String description;
  final String? bookImage;

  Book({
    required this.id,
    required this.title,
    required this.unitPrice,
    required this.priceWithTax,
    required this.category,
    required this.inventory,
    required this.description,
    this.bookImage,
  });

  factory Book.fromJson(Map<String, dynamic> json) {
    String? imageUrl = json['bookimage_set'].isNotEmpty
        ? json['bookimage_set'][0]['image']
        : null;

    return Book(
      id: json['id'],
      title: json['title'],
      unitPrice: json['unit_price'],
      priceWithTax: json['price_with_tax'],
      category: json['category'],
      inventory: json['inventory'],
      description: json['description'],
      bookImage: imageUrl,
    );
  }
}
