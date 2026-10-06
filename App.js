import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, FlatList, SafeAreaView, TouchableOpacity, ActivityIndicator } from 'react-native';

export default function App() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);

  // Replace with your local machine network IP when testing on physical mobile device
  const API_URL = 'http://127.0.0.1:5000/api/scans';

  const fetchHistory = async () => {
    try {
      setLoading(true);
      let response = await fetch(API_URL);
      let data = await response.json();
      if (data.status === 'success') {
        setScans(data.scans);
      }
    } catch (error) {
      console.error("Error fetching scan logs:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.brand}>🌿 Jaketron AgLab</Text>
        <Text style={styles.title}>Field Scan History</Text>
      </View>

      {loading ? (
        <ActivityIndicator size="large" color="#16a34a" style={{marginTop: 40}} />
      ) : (
        <FlatList
          data={scans}
          keyExtractor={(item) => item.id.toString()}
          contentContainerStyle={styles.listContainer}
          renderItem={({ item }) => (
            <View style={styles.card}>
              <View style={styles.cardHeader}>
                <Text style={styles.soilBadge}>{item.soil_name} Soil</Text>
                <Text style={styles.dateText}>{item.timestamp}</Text>
              </View>
              <Text style={styles.metricText}>Ideal pH: <Text style={styles.bold}>{item.ph}</Text></Text>
              <Text style={styles.metricText}>Organic Matter: <Text style={styles.bold}>{item.organic_matter}</Text></Text>
            </View>
          )}
          ListEmptyComponent={
            <Text style={styles.emptyText}>No field scans recorded yet. Run a scan on your web portal!</Text>
          }
        />
      )}

      <TouchableOpacity style={styles.refreshButton} onPress={fetchHistory}>
        <Text style={styles.refreshText}>🔄 Refresh Field Logs</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f0fdf4',
    paddingHorizontal: 16,
    paddingTop: 40,
  },
  header: {
    marginBottom: 16,
    paddingHorizontal: 4,
  },
  brand: {
    fontSize: 14,
    fontWeight: '700',
    color: '#15803d',
    marginBottom: 4,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#14532d',
  },
  listContainer: {
    paddingBottom: 20,
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 14:
    padding: 14,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#bbf7d0',
    shadowColor: '#15803d',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  soilBadge: {
    backgroundColor: '#dcfce7',
    color: '#166534',
    paddingVertical: 3,
    paddingHorizontal: 10,
    borderRadius: 20,
    fontWeight: '700',
    fontSize: 12,
  },
  dateText: {
    fontSize: 11,
    color: '#64748b',
  },
  metricText: {
    fontSize: 12.5,
    color: '#475569',
    marginTop: 2,
  },
  bold: {
    color: '#0f172a',
    fontWeight: '600',
  },
  emptyText: {
    textAlign: 'center',
    color: '#64748b',
    marginTop: 40,
    fontSize: 13,
  },
  refreshButton: {
    backgroundColor: '#16a34a',
    padding: 14,
    borderRadius: 14,
    alignItems: 'center',
    marginVertical: 16,
    shadowColor: '#16a34a',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.25,
    shadowRadius: 8,
  },
  refreshText: {
    color: '#ffffff',
    fontWeight: 'bold',
    fontSize: 15,
  },
});