import 'dart:io';
import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;

part 'database.g.dart';

/// Core data table for all log entries
class LogEntries extends Table {
  TextColumn get uuid => text()();
  DateTimeColumn get timestampUtc => dateTime()();
  TextColumn get localTimezone => text()();

  // Location data
  RealColumn get lat => real()();
  RealColumn get long => real()();
  RealColumn get altitude => real().nullable()();
  RealColumn get accuracyMeters => real().nullable()();

  // Media references
  TextColumn get photoPath => text()();
  TextColumn get audioPath => text().nullable()();
  TextColumn get textNote => text().nullable()();

  // Enrichment data (populated asynchronously)
  TextColumn get reverseGeo => text().nullable()();
  TextColumn get weatherSummary => text().nullable()();
  RealColumn get pressureInhg => real().nullable()();
  TextColumn get moonPhase => text().nullable()();
  RealColumn get sunAzimuth => real().nullable()();

  // Metadata
  TextColumn get tags => text().nullable()(); // JSON array stored as string
  BoolColumn get isLocked => boolean().withDefault(const Constant(false))();

  @override
  Set<Column> get primaryKey => {uuid};
}

@DriftDatabase(tables: [LogEntries])
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 1;

  // CRUD Operations

  /// Insert a new log entry
  Future<int> insertEntry(LogEntriesCompanion entry) {
    return into(logEntries).insert(entry);
  }

  /// Get all entries, newest first
  Future<List<LogEntry>> getAllEntries() {
    return (select(logEntries)
          ..orderBy([
            (t) => OrderingTerm(expression: t.timestampUtc, mode: OrderingMode.desc)
          ]))
        .get();
  }

  /// Get a single entry by UUID
  Future<LogEntry?> getEntryByUuid(String uuid) {
    return (select(logEntries)..where((t) => t.uuid.equals(uuid))).getSingleOrNull();
  }

  /// Update an entry (only if not locked)
  Future<bool> updateEntry(LogEntry entry) async {
    if (entry.isLocked) {
      return false; // Cannot update locked entries
    }
    return update(logEntries).replace(entry);
  }

  /// Delete an entry (only if not locked)
  Future<int> deleteEntry(String uuid) async {
    final entry = await getEntryByUuid(uuid);
    if (entry?.isLocked ?? false) {
      return 0; // Cannot delete locked entries
    }
    return (delete(logEntries)..where((t) => t.uuid.equals(uuid))).go();
  }

  /// Lock an entry (make it immutable)
  Future<bool> lockEntry(String uuid) {
    return (update(logEntries)..where((t) => t.uuid.equals(uuid)))
        .write(const LogEntriesCompanion(isLocked: Value(true)));
  }

  /// Get entries by date range
  Future<List<LogEntry>> getEntriesInRange(DateTime start, DateTime end) {
    return (select(logEntries)
          ..where((t) => t.timestampUtc.isBetweenValues(start, end))
          ..orderBy([
            (t) => OrderingTerm(expression: t.timestampUtc, mode: OrderingMode.desc)
          ]))
        .get();
  }
}

/// Opens the SQLite database connection
LazyDatabase _openConnection() {
  return LazyDatabase(() async {
    final dbFolder = await getApplicationDocumentsDirectory();
    final file = File(p.join(dbFolder.path, 'atomic_logger.db'));
    return NativeDatabase(file);
  });
}
