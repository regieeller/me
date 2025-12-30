import 'dart:io';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/database.dart';

class EntryCard extends StatelessWidget {
  final LogEntry entry;
  final VoidCallback onTap;

  const EntryCard({
    super.key,
    required this.entry,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Photo thumbnail
            AspectRatio(
              aspectRatio: 16 / 9,
              child: Image.file(
                File(entry.photoPath),
                fit: BoxFit.cover,
                errorBuilder: (context, error, stackTrace) {
                  return Container(
                    color: Colors.grey[800],
                    child: const Icon(Icons.broken_image, size: 48),
                  );
                },
              ),
            ),

            // Entry info
            Padding(
              padding: const EdgeInsets.all(12.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Timestamp and lock badge
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          _formatTimestamp(entry.timestampUtc),
                          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                                fontWeight: FontWeight.bold,
                              ),
                        ),
                      ),
                      if (entry.isLocked)
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 8,
                            vertical: 4,
                          ),
                          decoration: BoxDecoration(
                            color: Theme.of(context).colorScheme.primary.withOpacity(0.2),
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(
                              color: Theme.of(context).colorScheme.primary,
                              width: 1,
                            ),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(
                                Icons.lock,
                                size: 12,
                                color: Theme.of(context).colorScheme.primary,
                              ),
                              const SizedBox(width: 4),
                              Text(
                                'LOCKED',
                                style: TextStyle(
                                  color: Theme.of(context).colorScheme.primary,
                                  fontSize: 10,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                        ),
                    ],
                  ),
                  const SizedBox(height: 8),

                  // GPS coordinates
                  Row(
                    children: [
                      Icon(
                        Icons.location_on,
                        size: 16,
                        color: Theme.of(context).colorScheme.primary,
                      ),
                      const SizedBox(width: 4),
                      Text(
                        '${entry.lat.toStringAsFixed(6)}, ${entry.long.toStringAsFixed(6)}',
                        style: Theme.of(context).textTheme.bodyMedium,
                      ),
                    ],
                  ),

                  // Accuracy indicator
                  if (entry.accuracyMeters != null) ...[
                    const SizedBox(height: 4),
                    Row(
                      children: [
                        Icon(
                          _getAccuracyIcon(entry.accuracyMeters!),
                          size: 16,
                          color: _getAccuracyColor(entry.accuracyMeters!, context),
                        ),
                        const SizedBox(width: 4),
                        Text(
                          '±${entry.accuracyMeters!.toStringAsFixed(1)}m',
                          style: Theme.of(context).textTheme.bodySmall,
                        ),
                      ],
                    ),
                  ],

                  // Address (if enriched)
                  if (entry.reverseGeo != null) ...[
                    const SizedBox(height: 8),
                    const Divider(height: 1),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        Icon(
                          Icons.place,
                          size: 16,
                          color: Theme.of(context).colorScheme.primary,
                        ),
                        const SizedBox(width: 4),
                        Expanded(
                          child: Text(
                            entry.reverseGeo!,
                            style: Theme.of(context).textTheme.bodySmall,
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                      ],
                    ),
                  ],
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  String _formatTimestamp(DateTime timestamp) {
    final local = timestamp.toLocal();
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);
    final yesterday = today.subtract(const Duration(days: 1));
    final entryDate = DateTime(local.year, local.month, local.day);

    final timeFormat = DateFormat('h:mm a');

    if (entryDate == today) {
      return 'Today at ${timeFormat.format(local)}';
    } else if (entryDate == yesterday) {
      return 'Yesterday at ${timeFormat.format(local)}';
    } else {
      final dateFormat = DateFormat('MMM d, yyyy');
      return '${dateFormat.format(local)} at ${timeFormat.format(local)}';
    }
  }

  IconData _getAccuracyIcon(double accuracy) {
    if (accuracy <= 5) return Icons.gps_fixed;
    if (accuracy <= 20) return Icons.gps_not_fixed;
    return Icons.gps_off;
  }

  Color _getAccuracyColor(double accuracy, BuildContext context) {
    if (accuracy <= 5) return Colors.green;
    if (accuracy <= 20) return Colors.orange;
    return Colors.red;
  }
}
