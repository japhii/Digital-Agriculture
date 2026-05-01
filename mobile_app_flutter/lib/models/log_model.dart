import 'package:flutter/material.dart';

enum LogLevel { info, warning, error }

class LogModel {
  final String id;
  final String type;
  final LogLevel level;
  final String shortDescription;
  final dynamic input;
  final dynamic result;
  final DateTime timestamp;

  LogModel({
    required this.id,
    required this.type,
    required this.level,
    required this.shortDescription,
    required this.input,
    required this.result,
    required this.timestamp,
  });

  factory LogModel.fromJson(Map<String, dynamic> json) {
    LogLevel derivedLevel = LogLevel.info;
    final typeStr = json['type']?.toString().toLowerCase() ?? 'unknown';
    final res = json['result'];
    final resStr = res?.toString() ?? '';
    if (typeStr == 'disease') {
      if (resStr.contains('Healthy')) {
        derivedLevel = LogLevel.info;
      } else {
        derivedLevel = LogLevel.error;
      }
    } else if (typeStr == 'suitability') {
      if (resStr.contains('Low suitability')) {
        derivedLevel = LogLevel.error;
      } else if (resStr.contains('Moderate')) {
        derivedLevel = LogLevel.warning;
      }
    }

    return LogModel(
      id: UniqueKey().toString(),
      type: typeStr,
      level: derivedLevel,
      shortDescription: json['short'] ?? resStr,
      input: json['input'] ?? '',
      result: res,
      timestamp: DateTime.tryParse(json['timestamp'] ?? '') ?? DateTime.now(),
    );
  }
}